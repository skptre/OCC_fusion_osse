import csv
import datetime as dt
import glob
import os
import re

import numpy as np

from osse.params import value

MONTHS = {m: i for i, m in enumerate(
    ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"), start=1)}
N_HIST = 24  # 3 days of 3-hour blocks before T0: MSIS storm mode looks back 57 h


def kp_to_ap(kp):
    return float(value("KP_TO_AP")[int(round(kp * 3))])


def read_3day_forecast(path):
    with open(path) as f:
        lines = f.read().splitlines()
    issued = None
    for i, line in enumerate(lines):
        if line.startswith(":Issued:"):
            year, mon, day, hhmm = line.split()[1:5]
            issued = dt.datetime(int(year), MONTHS[mon], int(day), int(hhmm[:2]), int(hhmm[2:]))
        elif line.startswith("NOAA Kp index breakdown"):
            year = int(line.split()[-1])
            days = [dt.datetime(year, MONTHS[m], int(d)) for m, d in re.findall(r"([A-Z][a-z]{2}) (\d{2})", lines[i + 2])]
            kp = {}
            for row in lines[i + 3:i + 11]:
                hour = int(row[:2])
                for day, val in zip(days, re.findall(r"\d+\.\d+", row)):
                    kp[day + dt.timedelta(hours=hour)] = float(val)
            if issued is None or len(kp) != 24:
                raise ValueError(f"unexpected format in {path}")
            return issued, kp
    raise ValueError(f"no Kp table in {path}")


def load_forecasts():
    paths = glob.glob(os.path.join(value("FORECAST_DIR"), "*three_day_forecast.txt"))
    return sorted((read_3day_forecast(p) for p in paths), key=lambda fc: fc[0])


def latest_before(forecasts, now):
    best = None
    for issued, kp in forecasts:
        if issued <= now:
            best = kp
    if best is None:
        raise ValueError(f"no forecast issued before {now}")
    return best


def measured_ap3(start, n_blocks):
    by_date = {}
    with open(value("SW_FILE"), newline="") as f:
        for row in csv.DictReader(f):
            if not row["AP1"]:
                continue
            by_date[row["DATE"]] = [float(row[f"AP{j}"]) for j in range(1, 9)]
    ap3 = np.zeros(n_blocks)
    for b in range(n_blocks):
        when = start + dt.timedelta(hours=3 * b)
        ap3[b] = by_date[when.strftime("%Y-%m-%d")][when.hour // 3]
    return ap3


def prior_ap_array(t):
    t0 = dt.datetime.fromisoformat(value("T0"))
    start = t0 - dt.timedelta(hours=3 * N_HIST)
    measured = measured_ap3(start, N_HIST + value("NDAY") * 8)
    forecasts = load_forecasts()
    out = np.zeros((len(t), 7))
    for k, tk in enumerate(t):
        now = t0 + dt.timedelta(seconds=float(tk))
        i = N_HIST + int(tk // 10800)
        day0 = (i // 8) * 8
        kp = latest_before(forecasts, now)
        ap3 = measured.copy()
        for b in range(i, day0 + 8):
            ap3[b] = kp_to_ap(kp[start + dt.timedelta(hours=3 * b)])
        out[k, 0] = ap3[day0:day0 + 8].mean()
        out[k, 1:5] = ap3[i], ap3[i - 1], ap3[i - 2], ap3[i - 3]
        out[k, 5] = ap3[i - 11:i - 3].mean()
        out[k, 6] = ap3[i - 19:i - 11].mean()
    return out