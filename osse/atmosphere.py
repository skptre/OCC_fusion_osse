import math 
import os 
import numpy as np 

from osse.params import value 


def ref_ap_profile(lag, cap):
    n = (value("NDAY") + 3) * 8
    hrs = (np.arange(n) - 24) * 3.0
    ap = np.full(n, value("REF_AP_QUIET"))
    for i, h in enumerate(hrs):
        for start, ap_value in value("REF_AP_STEPS"):
            if h >= start:
                ap[i] = ap_value
    if lag:
        ap = np.concatenate([np.full(lag, value("REF_AP_QUIET")), ap[:-lag]])
    if cap is not None:
        ap = np.minimum(ap, cap)
    return hrs, ap


def ap_array(t, ap3_hrs, ap3):
    idx = np.searchsorted(ap3_hrs, t / 3600.0, side="right") - 1
    out = np.zeros((len(t), 7))
    for k, i in enumerate(idx):
        day0 = int((i // 8) * 8)
        out[k, 0] = ap3[day0:day0 + 8].mean()
        out[k, 1:5] = ap3[i], ap3[i - 1], ap3[i - 2], ap3[i - 3]
        out[k, 5] = ap3[i - 11:i - 3].mean()
        out[k, 6] = ap3[i - 19:i - 11].mean()
    return out


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
    o = msis.calculate(dates, lon, lat, np.full(n, float(alt_km)), np.full(n, f107), np.full(n, f107a),
                       aps, geomagnetic_activity=value("GEOMAG_MODE"), version=value("MSIS_VERSION"))
    o = np.nan_to_num(o, nan=0.0)
    cols = {"N2": o[:, 1], "O2": o[:, 2], "O": o[:, 3] + o[:, 8], "He": o[:, 4], "H": o[:, 5],
            "Ar": o[:, 6], "N": o[:, 7]}
    return np.stack([cols[s] for s in value("SPECIES")], axis=1)


def build_tables(alt_km, n_phases, cache_dir="cache"):
    nday = value("NDAY")
    path = os.path.join(cache_dir, f"msis_ref_{alt_km}km_{n_phases}ph_{nday}d.npz")
    if os.path.exists(path):
        d = np.load(path)
        return d["truth"], d["prior"], int(d["nper"])
    t = np.arange(0, nday * 86400, value("DT"))
    dates = np.datetime64(value("T0")) + (t * 1e3).astype("timedelta64[ms]")
    hrs, ap_true = ref_ap_profile(0, None)
    _, ap_prior = ref_ap_profile(value("REF_PRIOR_LAG"), value("REF_PRIOR_CAP"))
    aps_truth = ap_array(t, hrs, ap_true)
    aps_prior = ap_array(t, hrs, ap_prior)
    truth = np.zeros((n_phases, len(t), len(value("SPECIES"))))
    prior = np.zeros_like(truth)
    period = 0.0
    for j in range(n_phases):
        lat, lon, period = orbit(t, alt_km, 2 * math.pi * j / n_phases)
        truth[j] = run_msis(dates, lat, lon, alt_km, value("REF_F107_TRUTH"), value("REF_F107A"), aps_truth)
        prior[j] = run_msis(dates, lat, lon, alt_km, value("REF_F107_PRIOR"), value("REF_F107A"), aps_prior)
    nper = int(round(period / value("DT")))
    os.makedirs(cache_dir, exist_ok=True)
    np.savez_compressed(path, truth=truth, prior=prior, nper=nper)
    return truth, prior, nper