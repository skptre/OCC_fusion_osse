"""Stage 4d altitude grid (C6, quick version): the frozen architecture on the harsh truth at 250-500 km, May 2024
(high solar activity; solar-minimum cases need other dates + forecasts = later work).
Drag noise scales ~1/rho (W3 research): per-orbit single-frequency 15% at 300 km; above ~350 km per-orbit is not
usable, so daily drag is used with the error scaled from the 300 km value (labelled derived assumptions).
Usage: python scripts/alt_grid.py [--runs 2000]   Output: out/alt_grid/<alt>km.csv (metric,p10,p50,p90). Resumable."""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import simt
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from osse.scenario import OSSE

OUT = Path(__file__).resolve().parents[1] / "out" / "alt_grid"
HARSH = {"TRUTH_KIND": "perturbed", "TRUTH_MSIS_VERSION": 0}
GRID = {
    250: {"DRAG_WINDOW": 5430.0, "DRAG_NOISE": 0.05},
    300: {"DRAG_WINDOW": 5430.0, "DRAG_NOISE": 0.15},
    350: {"DRAG_WINDOW": 5430.0, "DRAG_NOISE": 0.30},
    400: {"DRAG_WINDOW": 86400.0, "DRAG_NOISE": 0.10},
    450: {"DRAG_WINDOW": 86400.0, "DRAG_NOISE": 0.15},
    500: {"DRAG_WINDOW": 86400.0, "DRAG_NOISE": 0.20},
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", type=int, default=2000)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for alt, drag in GRID.items():
        path = OUT / f"{alt}km.csv"
        if path.exists():
            print(f"skip {alt} km (done)")
            continue
        s = OSSE(alt_km=alt, **HARSH, **drag)
        r, sec = simt.run(s, args.runs, s.n_steps, seed=1, device=args.device, dtype=torch.float64)
        rows = []
        for k in r.metric_names:
            v = r[k].cpu().numpy().astype(float)
            v = v[np.isfinite(v)]
            if v.size:
                rows.append((k, *np.percentile(v, [10, 50, 90])))
        with open(path, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["metric", "p10", "p50", "p90"])
            w.writerows(rows)
        m = {k: b for k, a, b, c in rows}
        print(f"\n=== {alt} km ({sec:.0f} s) NEES {m['nees']:.2f}")
        for w in ("quiet", "storm", "recovery"):
            print(f"  {w:<9}" + "".join(f" | {q} ours {m[f'{w}_{q}_fused_mae']:.3f} model {m[f'{w}_{q}_prior_mae']:.3f}"
                                         for q in ("rho", "O", "N2")), flush=True)


if __name__ == "__main__":
    main()
