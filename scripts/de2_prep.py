"""Prepare DE-2 NACS replay windows: real in-situ composition (1981-83) on the OSSE's 30 s grid.

For each window this writes data/de2/<name>.npz with, per 30 s bin:
  t (s from window start), cover (bin has >= MIN_SAMPLES valid 1-s NACS samples below MAX_ALT),
  alt, lat, lon, lst (bin means), truth (K, 7 species, m^-3), prior21 / prior00 (MSIS 2.1 / NRLMSISE-00 on the
  measured 1981-83 drivers at the same positions), n_samples.
Species order follows osse/params.py SPECIES (N2, O2, O, He, H, Ar, N).
Truth: N2, O, He, Ar from NACS (Carignan et al. 1981; cm^-3 -> m^-3); O2, H, N are not usable in the NACS files
(no O2/H columns, N mostly empty), so they are filled from MSIS 2.1 (minor species; labelled).
NACS ASCII files carry wrong-day positions after a UT midnight wrap inside a file (found Nov 10): those records are dropped.
Drivers: OMNI2 hourly ap and daily F10.7 (previous day), 81-day centred F10.7A, MSIS storm-time ap array.

Usage: python scripts/de2_prep.py <nacs_dir> <omni_dir> <name> <first_day YYYY-MM-DD> <n_days> [max_alt_km=350]
Coverage below 350 / 450 km in Sep 1982: 7.1% / 10.9% of 30 s bins (DE-2 is elliptical; data near perigee only).
"""
import datetime as dt
import glob
import os
import sys
from pathlib import Path

import numpy as np
import pymsis

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
from osse.params import value

MAX_ALT = 350.0
MIN_SAMPLES = 10
COLS = "ut_ms O O_err N2 N2_err He He_err N N_err Ar Ar_err orbit alt lat lon lst lmt L invlat sza".split()
EPOCH = dt.datetime(1981, 1, 1)


def read_nacs(nacs_dir, first, n_days):
    keep = {(first + dt.timedelta(days=d)).strftime("%Y%j") for d in range(n_days)}
    rows = []
    for f in sorted(glob.glob(os.path.join(nacs_dir, "*.ASC"))):
        b = os.path.basename(f)
        if b[:7] not in keep:
            continue
        a = np.loadtxt(f, skiprows=2, ndmin=2)
        wrap = np.where(np.diff(a[:, 0]) < 0)[0]
        if len(wrap):
            a = a[:wrap[0] + 1]
        day0 = dt.datetime(int(b[:4]), 1, 1) + dt.timedelta(days=int(b[4:7]) - 1)
        rows.append(np.column_stack([(day0 - EPOCH).total_seconds() + a[:, 0] / 1000.0, a]))
    A = np.vstack(rows)
    A = A[np.argsort(A[:, 0])]
    return {k: A[:, i] for i, k in enumerate(["t"] + COLS)}


def drivers(omni_dir):
    o = np.vstack([np.loadtxt(os.path.join(omni_dir, f"omni2_{y}.dat")) for y in (1981, 1982, 1983)])
    ot = np.array([(dt.datetime(int(r[0]), 1, 1) + dt.timedelta(days=int(r[1]) - 1, hours=int(r[2])) - EPOCH)
                   .total_seconds() for r in o])
    ap_h = o[:, 49]
    f_h = np.where(o[:, 50] > 900, np.nan, o[:, 50])
    nd = int(ot[-1] // 86400) + 1
    day_f = np.array([np.nanmean(f_h[(ot >= d * 86400) & (ot < (d + 1) * 86400)]) for d in range(nd)])

    def ap_at(t):
        return ap_h[np.searchsorted(ot, t, side="right") - 1]

    def ap7(t):
        d = int(t // 86400)
        th = lambda h: ap_at(t - h * 3600)
        return [np.mean(ap_h[(ot >= d * 86400) & (ot < (d + 1) * 86400)]), th(0), th(3), th(6), th(9),
                np.mean([th(h) for h in range(12, 34, 3)]), np.mean([th(h) for h in range(36, 58, 3)])]

    def at(t):
        d = (t // 86400).astype(int)
        f107 = day_f[d - 1]
        f107a = np.array([np.nanmean(day_f[i - 40:i + 41]) for i in d])
        aps = np.array([ap7(x) for x in t])
        return f107, f107a, aps

    return at


def msis(dates, lon, lat, alt, f107, f107a, aps, version):
    o = pymsis.calculate(dates, lon, lat, alt, f107, f107a, aps, version=version, geomagnetic_activity=-1)
    o = np.nan_to_num(o, nan=0.0)
    V = pymsis.Variable
    cols = {"N2": o[:, V.N2], "O2": o[:, V.O2], "O": o[:, V.O] + o[:, V.ANOMALOUS_O], "He": o[:, V.HE],
            "H": o[:, V.H], "Ar": o[:, V.AR], "N": o[:, V.N]}
    return np.stack([cols[s] for s in value("SPECIES")], axis=1)


def main():
    global MAX_ALT
    nacs_dir, omni_dir, name, first, n_days = sys.argv[1:6]
    if len(sys.argv) > 6:
        MAX_ALT = float(sys.argv[6])
    first, n_days = dt.datetime.fromisoformat(first), int(n_days)
    dtg = value("DT")
    c = read_nacs(nacs_dir, first, n_days)
    t0 = (first - EPOCH).total_seconds()
    K = int(n_days * 86400 / dtg)
    good = (c["alt"] < MAX_ALT) & (c["O"] > 0) & (c["N2"] > 0) & (c["He"] > 0)
    b = ((c["t"] - t0) // dtg).astype(int)
    good &= (b >= 0) & (b < K)
    b = b[good]
    cnt = np.bincount(b, minlength=K)
    cover = cnt >= MIN_SAMPLES

    def bin_mean(v):
        s = np.bincount(b, weights=v[good], minlength=K)
        return np.where(cnt > 0, s / np.maximum(cnt, 1), np.nan)

    lonr = np.radians(c["lon"])
    lon = np.degrees(np.arctan2(bin_mean(np.sin(lonr)), bin_mean(np.cos(lonr))))
    lstr = c["lst"] * 2 * np.pi / 24
    lst = (np.degrees(np.arctan2(bin_mean(np.sin(lstr)), bin_mean(np.cos(lstr)))) / 15) % 24
    alt, lat = bin_mean(c["alt"]), bin_mean(c["lat"])
    nacs = {k: 1e6 * bin_mean(np.clip(c[k], 0, None)) for k in ("O", "N2", "He", "Ar")}

    t = np.arange(K) * dtg
    idx = np.where(cover)[0]
    dates = np.datetime64(first) + (t[idx] * 1e3).astype("timedelta64[ms]")
    f107, f107a, aps = drivers(omni_dir)(t0 + t[idx])
    S = len(value("SPECIES"))
    truth = np.full((K, S), np.nan)
    prior21 = np.full((K, S), np.nan)
    prior00 = np.full((K, S), np.nan)
    p21 = msis(dates, lon[idx], lat[idx], alt[idx], f107, f107a, aps, 2.1)
    p00 = msis(dates, lon[idx], lat[idx], alt[idx], f107, f107a, aps, 0)
    tr = p21.copy()
    sp = value("SPECIES")
    for k in ("O", "N2", "He", "Ar"):
        tr[:, sp.index(k)] = nacs[k][idx]
    truth[idx], prior21[idx], prior00[idx] = tr, p21, p00

    out = REPO / "data" / "de2"
    out.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out / f"{name}.npz", t=t, cover=cover, alt=alt, lat=lat, lon=lon, lst=lst, truth=truth,
                        prior21=prior21, prior00=prior00, n_samples=cnt, start=str(first.date()), n_days=n_days)

    mass = np.array(value("MASS"))
    print(f"{name}: {K} bins, covered {cover.sum()} ({cover.mean():.1%}), alt {np.nanmin(alt[cover]):.0f}-"
          f"{np.nanmax(alt[cover]):.0f} km")
    for d in range(n_days):
        m = idx[(idx >= d * 2880) & (idx < (d + 1) * 2880)]
        if not len(m):
            continue
        r = lambda q: 100 * (np.exp(np.median(np.log(truth[m, sp.index(q)] / prior21[m, sp.index(q)]))) - 1)
        rho = 100 * (np.exp(np.median(np.log((truth[m] * mass).sum(1) / (prior21[m] * mass).sum(1)))) - 1)
        print(f"  {(first + dt.timedelta(days=d)).date()} n={len(m):4d}  NACS/MSIS2.1-1: O {r('O'):+6.1f}%  "
              f"N2 {r('N2'):+6.1f}%  He {r('He'):+6.1f}%  rho {rho:+6.1f}%")


if __name__ == "__main__":
    main()
