"""Prepare the GRACE-FO May 2024 real-density replay window (held-out validation, run once after the freeze).

Source: ESA Swarm DISC / TOLEOS GRACE-FO-1 accelerometer density, product GF_OPER_DNS1ACC_2_ v0003 (10 s, ~490 km;
swarm-diss.eo.esa.int /Multimission/GRACE-FO/DNS/Sat_1; Siemes et al. 2023). Same window as the OSSE (T0, NDAY), so
the quiet/storm/recovery scoring windows apply unchanged.
Output data/de2/gracefo_2024-05.npz, same layout as scripts/de2_prep.py:
  truth  = MSIS 2.1 on the real drivers at GRACE-FO positions, all species scaled by rho_GRACE-FO / rho_MSIS
           (measured density, model composition: density is what this window validates);
  prior21 = MSIS 2.1 on the NOAA forecast drivers (the OSSE's operational prior), PRIOR_F107A.
Usage: python scripts/gracefo_prep.py <dir with GF_OPER_DNS1ACC_2_ CDF files>
"""
import glob
import sys
from pathlib import Path

import cdflib
import numpy as np
import pymsis
from pymsis.utils import get_f107_ap, use_space_weather_file

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from osse.forecasts import prior_ap_array
from osse.params import value


def msis(dates, lon, lat, alt, f107, f107a, aps):
    o = pymsis.calculate(dates, lon, lat, alt, f107, f107a, aps, version=value("MSIS_VERSION"),
                         geomagnetic_activity=value("GEOMAG_MODE"))
    o = np.nan_to_num(o, nan=0.0)
    V = pymsis.Variable
    cols = {"N2": o[:, V.N2], "O2": o[:, V.O2], "O": o[:, V.O] + o[:, V.ANOMALOUS_O], "He": o[:, V.HE],
            "H": o[:, V.H], "Ar": o[:, V.AR], "N": o[:, V.N]}
    return np.stack([cols[s] for s in value("SPECIES")], axis=1)


def main():
    files = sorted(glob.glob(str(Path(sys.argv[1]) / "GF_OPER_DNS1ACC_2_*.cdf")))
    parts = {k: [] for k in ("t", "alt", "lat", "lon", "lst", "rho", "ok")}
    for f in files:
        c = cdflib.CDF(f)
        parts["t"].append(cdflib.cdfepoch.to_datetime(c.varget("time")))
        parts["alt"].append(c.varget("altitude") / 1e3)
        parts["lat"].append(c.varget("latitude"))
        parts["lon"].append(c.varget("longitude"))
        parts["lst"].append(c.varget("local_solar_time"))
        parts["rho"].append(c.varget("density"))
        parts["ok"].append(c.varget("validity_flag") == 0)
    a = {k: np.concatenate(v) for k, v in parts.items()}
    t0 = np.datetime64(value("T0"))
    sec = (a["t"].astype("datetime64[ms]") - t0).astype("timedelta64[ms]").astype(float) / 1e3
    dt, nday = value("DT"), value("NDAY")
    K = int(nday * 86400 / dt)
    b = (sec // dt).astype(int)
    good = a["ok"] & (b >= 0) & (b < K) & (a["rho"] > 0)
    b = b[good]
    cnt = np.bincount(b, minlength=K)
    cover = cnt >= 2

    def bin_mean(v):
        return np.where(cnt > 0, np.bincount(b, weights=v[good], minlength=K) / np.maximum(cnt, 1), np.nan)

    lonr = np.radians(a["lon"])
    lon = np.degrees(np.arctan2(bin_mean(np.sin(lonr)), bin_mean(np.cos(lonr))))
    lstr = a["lst"] * 2 * np.pi / 24
    lst = (np.degrees(np.arctan2(bin_mean(np.sin(lstr)), bin_mean(np.cos(lstr)))) / 15) % 24
    alt, lat, rho = bin_mean(a["alt"]), bin_mean(a["lat"]), bin_mean(a["rho"])

    t = np.arange(K) * dt
    idx = np.where(cover)[0]
    dates = t0 + (t[idx] * 1e3).astype("timedelta64[ms]")
    use_space_weather_file(str(REPO / value("SW_FILE")))
    f107, f107a, aps_real = get_f107_ap(dates)
    aps_prior = prior_ap_array(t)[idx]
    real = msis(dates, lon[idx], lat[idx], alt[idx], f107, f107a, aps_real)
    prior = msis(dates, lon[idx], lat[idx], alt[idx], f107, np.full(len(idx), value("PRIOR_F107A")), aps_prior)
    mass = np.array(value("MASS"))
    amu = value("AMU")
    rho_real = (real * mass).sum(1) * amu
    S = len(value("SPECIES"))
    truth = np.full((K, S), np.nan)
    prior21 = np.full((K, S), np.nan)
    truth[idx] = real * (rho[idx] / rho_real)[:, None]
    prior21[idx] = prior

    out = REPO / "data" / "de2"
    out.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out / "gracefo_2024-05.npz", t=t, cover=cover, alt=alt, lat=lat, lon=lon, lst=lst,
                        truth=truth, prior21=prior21, prior00=prior21, n_samples=cnt, start=str(value("T0"))[:10],
                        n_days=nday)
    rho_prior = (prior * mass).sum(1) * amu
    hours = t[idx] / 3600
    print(f"gracefo_2024-05: {K} bins, covered {cover.sum()} ({cover.mean():.1%}), alt {np.nanmin(alt[cover]):.0f}-"
          f"{np.nanmax(alt[cover]):.0f} km")
    for w in ("quiet", "storm", "recovery"):
        h0, h1 = value(f"{w.upper()}_HOURS")
        m = (hours >= h0) & (hours < h1)
        e = rho_prior[m] / rho[idx][m] - 1
        print(f"  {w:<9} forecast-driven MSIS 2.1 vs GRACE-FO: median {100 * np.median(e):+.1f}%  "
              f"MAE {100 * np.median(np.abs(e)):.1f}%")


if __name__ == "__main__":
    main()
