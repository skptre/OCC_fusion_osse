import math 
import os 
import numpy as np 

from pymsis.utils import get_f107_ap, use_space_weather_file
from osse.forecasts import prior_ap_array

from osse.params import value 

def orbit(t, alt_km, raan0):
    r = value("RE") + alt_km * 1e3
    n = math.sqrt(value("MU") / r ** 3)
    u = n * t
    inc = math.radians(value("INC_DEG"))
    lat = np.degrees(np.arcsin(np.sin(inc) * np.sin(u)))
    lon_in = np.arctan2(np.cos(inc) * np.sin(u), np.cos(u)) + raan0
    lon = np.degrees((lon_in - value("WE") * t + np.pi) % (2 * np.pi) - np.pi)
    return lat, lon, 2 * math.pi / n


def run_msis(dates, lat, lon, alt_km, f107, f107a, aps):
    from pymsis import msis
    n = len(dates)
    o = msis.calculate(dates, lon, lat, np.full(n, float(alt_km)), np.broadcast_to(f107, (n,)), np.broadcast_to(f107a, (n,)),
                       aps, geomagnetic_activity=value("GEOMAG_MODE"), version=value("MSIS_VERSION"))
    o = np.nan_to_num(o, nan=0.0)
    cols = {"N2": o[:, 1], "O2": o[:, 2], "O": o[:, 3] + o[:, 8], "He": o[:, 4], "H": o[:, 5],
            "Ar": o[:, 6], "N": o[:, 7]}
    return np.stack([cols[s] for s in value("SPECIES")], axis=1)


def build_tables(alt_km, n_phases, cache_dir="cache"):
    nday = value("NDAY")
    path = os.path.join(cache_dir, f"msis_real_{alt_km}km_{n_phases}ph_{nday}d.npz")
    if os.path.exists(path):
        d = np.load(path)
        return d["truth"], d["prior"], int(d["nper"])
    t = np.arange(0, nday * 86400, value("DT"))
    dates = np.datetime64(value("T0")) + (t * 1e3).astype("timedelta64[ms]")
    use_space_weather_file(value("SW_FILE"))
    f107, f107a, aps_truth = get_f107_ap(dates)
    aps_prior = prior_ap_array(t)
    truth = np.zeros((n_phases, len(t), len(value("SPECIES"))))
    prior = np.zeros_like(truth)
    period = 0.0
    for j in range(n_phases):
        lat, lon, period = orbit(t, alt_km, 2 * math.pi * j / n_phases)
        truth[j] = run_msis(dates, lat, lon, alt_km, f107, f107a, aps_truth)
        prior[j] = run_msis(dates, lat, lon, alt_km, f107, value("PRIOR_F107A"), aps_prior)
    nper = int(round(period / value("DT")))
    os.makedirs(cache_dir, exist_ok=True)
    np.savez_compressed(path, truth=truth, prior=prior, nper=nper)
    return truth, prior, nper