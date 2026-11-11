import math
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from pymsis.utils import get_f107_ap, use_space_weather_file
from osse.atmosphere import orbit, run_msis, truth_errors
from osse.params import value

PHASES = 4
CANDIDATES = [(0.12, 0.40)]

t = np.arange(0, value("NDAY") * 86400, value("DT"))
dates = np.datetime64(value("T0")) + (t * 1e3).astype("timedelta64[ms]")
use_space_weather_file(str(REPO / value("SW_FILE")))
f107, f107a, aps = get_f107_ap(dates)
mass = np.array(value("MASS"))
sp = value("SPECIES")
o, n2 = sp.index("O"), sp.index("N2")
hours = t / 3600
win = {w: (hours >= value(f"{w.upper()}_HOURS")[0]) & (hours < value(f"{w.upper()}_HOURS")[1])
       for w in ("quiet", "storm", "recovery")}
alt, ver = value("ALT_KM"), value("TRUTH_MSIS_VERSION")

plain = []
for j in range(PHASES):
    lat, lon, _ = orbit(t, alt, 2 * math.pi * j / PHASES)
    plain.append((lat, lon, run_msis(dates, lat, lon, alt, f107, f107a, aps, ver)))

for f_sd, ap_sd in CANDIDATES:
    out = {w: {"rho": [], "O": [], "N2": []} for w in win}
    for j, (lat, lon, base) in enumerate(plain):
        e_f, e_ap, e_o = truth_errors(len(t), j, f_sd, ap_sd, value("TRUTH_O_SD"))
        pert = run_msis(dates, lat, lon, alt, f107 * np.exp(e_f), f107a, aps * np.exp(e_ap)[:, None], ver)
        pert[:, o] *= np.exp(e_o)
        lr = {"rho": np.log((pert * mass).sum(1) / (base * mass).sum(1)),
              "O": np.log(pert[:, o] / base[:, o]), "N2": np.log(pert[:, n2] / base[:, n2])}
        for w, m in win.items():
            for q in lr:
                out[w][q].append(lr[q][m])
    print(f"F10.7 sd {f_sd}, ap sd {ap_sd}: " + " | ".join(
        f"{w} " + " ".join(f"{q} {np.concatenate(v).std():.3f}" for q, v in out[w].items()) for w in win))