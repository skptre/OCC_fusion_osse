"""Phase A sweeps: turn each unknown into a requirement curve.

Usage (from the repo root):
    python scripts/phase_a.py A1              # 200 runs per config, CPU, resumable
    python scripts/phase_a.py A3 --runs 10000 # e.g. on Colab GPU
    python scripts/phase_a.py all
Output: out/phase_a/<sweep>.csv (one row per config, p10/p50/p90 of every metric).
"""
import argparse
import sys
from pathlib import Path

import simt
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from osse.params import value
from osse.scenario import OSSE

OUT = Path("out/phase_a")
SPECIES = value("SPECIES")


def r_true_with_so(so):
    r = list(value("R_TRUE"))
    r[SPECIES.index("O")] = so
    return tuple(r)


def drift_pairs(means):
    return [{"O_DRIFT_MEAN": m, "O_DRIFT_SD": max(m / 3, 1e-6)} for m in means]


SWEEPS = {
    "A1": ("drag realism: day-averaged drag error (Lowe 2026: 5/9/16%) and C_D uncertainty (5-15%)",
           simt.one_at_a_time({}, DRAG_NOISE=[0.05, 0.09, 0.16], CD_SD=[0.05, 0.15])),
    "A2": ("S_O mismatch: true atomic-O gauge sensitivity vs the filter's 0.56 (physical bracket ~0.5-0.77)",
           [{}] + [{"R_TRUE": r_true_with_so(so)} for so in (0.45, 0.50, 0.63, 0.70, 0.77)]),
    "A3": ("FIPEX one-sided drift (mean, sd = mean/3), ln units per day",
           [{}] + drift_pairs([0.0, 0.003, 0.01, 0.06])),
    "A4": ("CCG: drift per day, noise per 30 s, unit-to-unit gain spread",
           simt.one_at_a_time({}, GAUGE_DRIFT_SD=[0.001, 0.005, 0.05], GAUGE_NOISE=[0.005, 0.03],
                              GAUGE_GAIN_SD=[0.05, 0.10])),
    "A5": ("absolute/relative calibration: gauge and FIPEX gain priors tightened together (ground calibration)",
           [{}] + [{"GAUGE_GAIN_SD": g, "O_GAIN_SD": g} for g in (0.10, 0.05, 0.02)]),
}

SHOW = [f"{w}_{q}" for w in ("quiet", "storm", "recovery") for q in
        ("rho_fused_mae", "O_fused_mae", "N2_fused_mae")] + ["nees"]


def summary(rows):
    for row in rows:
        cfg = {k: row[k] for k in row if k.isupper()}
        print(f"\n{cfg or 'baseline'}")
        for name in SHOW:
            p50, p90 = row.get(f"{name}_p50"), row.get(f"{name}_p90")
            if p50 not in (None, ""):
                print(f"  {name:<22} p50 {float(p50):.4f}   p90 {float(p90):.4f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sweep", choices=list(SWEEPS) + ["all"])
    ap.add_argument("--runs", type=int, default=200)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = ap.parse_args()

    names = list(SWEEPS) if args.sweep == "all" else [args.sweep]
    for name in names:
        about, configs = SWEEPS[name]
        print(f"=== {name}: {about} ({len(configs)} configs, {args.runs} runs each) ===", flush=True)
        rows = simt.sweep(lambda **cfg: OSSE(**cfg), configs, args.runs, seed=1, device=args.device,
                          dtype=torch.float64, csv_path=str(OUT / f"{name}.csv"), resume=True)
        summary(rows)


if __name__ == "__main__":
    main()
