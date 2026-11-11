import argparse
import sys
from pathlib import Path

import simt
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from osse.params import value
from osse.scenario import OSSE

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "out" / "phase_a3"
SPECIES = value("SPECIES")
# final Phase A (freeze-v1): register defaults = frozen architecture; truth = harsh (NRLMSISE-00 + driver errors)
BASE = {"TRUTH_KIND": "perturbed", "TRUTH_MSIS_VERSION": 0}
BRACKET = value("SO_BRACKET_SD")


def r_true(**scale):
    r = list(value("R_TRUE"))
    for gas, f in scale.items():
        if gas == "non_O":
            r = [x if SPECIES[i] == "O" else x * f for i, x in enumerate(r)]
        else:
            r[SPECIES.index(gas)] *= f
    return tuple(r)


def each(name, values):
    return [{**BASE, name: v} for v in values]


def drift_pairs(means):
    return [{**BASE, "O_DRIFT_MEAN": m, "O_DRIFT_SD": max(m / 3, 1e-6)} for m in means]


LEAK = ("gauge", "o", "drag", "leak")

SWEEPS = {
    # the baseline runs once (A1); the other sweeps compare against it
    "A1": ("drag: per-orbit noise (dual 0.05 .. poor 0.25), C_D prior (known host 0.05 .. unknown 0.25), daily fallback",
           [BASE] + each("DRAG_NOISE", [0.05, 0.25]) + each("CD_SD", [0.05, 0.15, 0.25])
           + [{**BASE, "DRAG_WINDOW": 86400.0, "DRAG_NOISE": 0.06}]),
    "A2": ("S_O: ground calibration quality (filter knows), uncalibrated (consider, bracket), filter fooled",
           [{**BASE, "SO_SD": v, "SO_TRUTH_SD": v} for v in (0.03, 0.10)]
           + [{**BASE, "SO_MODE": "consider", "SO_SD": BRACKET, "SO_TRUTH_SD": BRACKET},
              {**BASE, "SO_TRUTH_SD": 0.10}]),
    "A3": ("FIPEX: one-sided drift (ln/day), gain prior (unit-to-unit), noise, outages",
           drift_pairs([0.0, 0.01, 0.06]) + each("O_GAIN_SD", [0.05, 0.12])
           + each("O_NOISE", [0.02, 0.10]) + [{**BASE, "O_GAP_EVERY": 21600.0, "O_GAP_LEN": 3600.0}]),
    "A4": ("CCG: drift, noise (0.05 = datasheet repeatability), outages",
           each("GAUGE_DRIFT_SD", [0.005, 0.05]) + each("GAUGE_NOISE", [0.005, 0.05])
           + [{**BASE, "GAUGE_GAP_EVERY": 21600.0, "GAUGE_GAP_LEN": 1800.0}]),
    "A5": ("calibration: leak accuracy, no leak, both gains ground-calibrated",
           each("LEAK_NOISE", [0.03, 0.10]) + [{**BASE, "USE_SENSORS": ("gauge", "o", "drag")}]
           + [{**BASE, "GAUGE_GAIN_SD": 0.05, "O_GAIN_SD": 0.05}]),
    "A6": ("gas factors, filter fooled: truth He/N/all-non-O off by their source spread",
           [{**BASE, "R_TRUE": r_true(**{g: f})} for g, f in
            (("He", 1.25), ("He", 0.75), ("N", 1.10), ("N", 0.90), ("non_O", 1.05), ("non_O", 0.95))]),
}

SHOW = [f"{w}_{q}" for w in ("quiet", "storm", "recovery") for q in
        ("rho_fused_mae", "O_fused_mae", "N2_fused_mae")] + ["nees"]


def summary(rows):
    for row in rows:
        cfg = {k: row[k] for k in row if k.isupper() and k != "TRUTH_MSIS_VERSION"}
        print(f"\n{cfg or 'baseline'}")
        for name in SHOW:
            p50, p90 = row.get(f"{name}_p50"), row.get(f"{name}_p90")
            if p50 not in (None, ""):
                print(f"  {name:<22} p50 {float(p50):.4f}   p90 {float(p90):.4f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sweep", choices=list(SWEEPS) + ["all"])
    ap.add_argument("--runs", type=int, default=2000)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for name in (list(SWEEPS) if args.sweep == "all" else [args.sweep]):
        about, configs = SWEEPS[name]
        print(f"=== {name}: {about} ({len(configs)} configs, {args.runs} runs each) ===", flush=True)
        rows = simt.sweep(lambda **cfg: OSSE(**cfg), configs, args.runs, seed=1, device=args.device,
                          dtype=torch.float64, csv_path=str(OUT / f"{name}.csv"), resume=True)
        summary(rows)


if __name__ == "__main__":
    main()