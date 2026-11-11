"""Stage 4a headline (C5 + C9) on the frozen architecture (freeze-v1 register defaults).
Per case: accuracy = bias, precision = 1-sigma scatter of the 30 s errors (std), MAE p50/p90, model (prior) error
alongside; p10/p50/p90 of every metric saved, plus 3 recorded runs (every 2 steps) for the time-series figures.
Usage: python scripts/headline.py [--runs 2000] [--only harsh,twin]
Output: out/headline/<case>.csv (metric,p10,p50,p90) and out/headline/<case>_series.pt. Resumable (skips done cases)."""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import simt
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from osse.params import value
from osse.scenario import OSSE

OUT = Path(__file__).resolve().parents[1] / "out" / "headline"
HARSH = {"TRUTH_KIND": "perturbed", "TRUTH_MSIS_VERSION": 0}
CASES = {
    "harsh": HARSH,                                                   # THE headline truth
    "driver_error": {"TRUTH_KIND": "perturbed"},                      # MSIS 2.1 + calibrated driver errors
    "msise00": {"TRUTH_MSIS_VERSION": 0},                             # independent empirical model
    "twin": {"TRUTH_MSIS_VERSION": 2.1},                              # sensor-limited (identical twin)
    "harsh_uncalibrated": {**HARSH, "SO_MODE": "consider", "SO_SD": value("SO_BRACKET_SD"),
                           "SO_TRUTH_SD": value("SO_BRACKET_SD"), "USE_SENSORS": ("gauge", "o", "drag")},
    "harsh_c9_best_estimate": {**HARSH, "O_DRIFT_MEAN": 0.01, "O_DRIFT_SD": 0.0033, "GAUGE_DRIFT_SD": 0.005,
                               "CD_SD": 0.05},
    "harsh_dual_gps": {**HARSH, "DRAG_NOISE": 0.05},
    "harsh_drag_only": {**HARSH, "USE_SENSORS": ("drag",)},           # ablation: host GPS drag alone
    "harsh_gauge_drag": {**HARSH, "USE_SENSORS": ("gauge", "drag", "leak")},  # ablation: no FIPEX
}
KEEP_SERIES = ("N2_truth", "N2_prior", "N2_fused", "O_truth", "O_prior", "O_fused", "rho_truth", "N2_sd",
               "gauge_gain_est", "gauge_gain_true", "o_gain_est", "o_gain_true", "x", "P", "step")


def summarize(name, r):
    rows = []
    for k in r.metric_names:
        v = r[k].cpu().numpy().astype(float)
        v = v[np.isfinite(v)]
        if v.size:
            rows.append((k, *np.percentile(v, [10, 50, 90])))
    with open(OUT / f"{name}.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["metric", "p10", "p50", "p90"])
        w.writerows(rows)
    return {k: (a, b, c) for k, a, b, c in rows}


def show(name, m):
    print(f"\n=== {name} ===  NEES p50 {m['nees'][1]:.2f}")
    for w in ("quiet", "storm", "recovery"):
        line = f"  {w:<9}"
        for q in ("rho", "O", "N2"):
            line += (f" | {q}: acc {m[f'{w}_{q}_fused_bias'][1]:+.3f} prec {m[f'{w}_{q}_fused_std'][1]:.3f} "
                     f"mae {m[f'{w}_{q}_fused_mae'][1]:.3f}/{m[f'{w}_{q}_fused_mae'][2]:.3f} "
                     f"model {m[f'{w}_{q}_prior_mae'][1]:.3f}")
        print(line, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=2000)
    ap.add_argument("--only", default="")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    names = [n for n in CASES if not args.only or n in args.only.split(",")]
    for name in names:
        if (OUT / f"{name}.csv").exists():
            print(f"skip {name} (done)")
            continue
        s = OSSE(**CASES[name])
        r, sec = simt.run(s, args.runs, s.n_steps, seed=1, device=args.device, dtype=torch.float64,
                          record_runs=3, record_every=4)
        keep = {k: v for k, v in r.series.items() if k in KEEP_SERIES}
        keep["phase"] = r["phase"][:3].cpu()
        keep["case"] = CASES[name]
        torch.save(keep, OUT / f"{name}_series.pt")
        show(name, summarize(name, r))
        print(f"  ({sec:.0f} s)", flush=True)


if __name__ == "__main__":
    main()
