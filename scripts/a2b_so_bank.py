"""A2b: can the atomic-O gauge factor S_O be measured in flight? (multiple-model likelihood bank)

The truth uses one S_O (unknown to the filters). A bank of GM filters, each assuming a different
S_O, runs on exactly the same simulated data (same seed, so same truth, noise, gains and drifts).
Each filter is scored by its innovation negative log-likelihood (how well it predicted the sensors):
    NLL = sum over all accepted updates of 0.5 * (ln S + nu^2 / S)
The likelihood-weighted S_O (weights exp(-NLL), per run) is the in-flight estimate.
Method: multiple-model adaptive estimation (Magill 1965), equivalent to a profile likelihood on a grid.

Usage (from the repo root):
    python scripts/a2b_so_bank.py                       # truths 0.56 0.66 0.77, 200 runs, current params
    python scripts/a2b_so_bank.py --truths 0.70 --runs 100 --set O_DRIFT_MEAN=0 O_DRIFT_SD=1e-6
Output: out/a2b/<tag>.csv, one row per run and truth (estimate, best grid point, N2/O/rho errors).

This script does not change the osse package. It wraps kf_update_scalar and the Scorer inside this
process only, to add up ln S + NIS per run.
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
import simt
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import osse.scenario as scen
from osse.metrics import Scorer
from osse.params import value
from osse.scenario import OSSE

OUT = Path("out/a2b")
SPECIES = value("SPECIES")
O = SPECIES.index("O")
GRID = (0.45, 0.50, 0.56, 0.63, 0.70, 0.77, 0.85)
DEFAULT_SO = value("R_FILT")[O]
KEYS = [f"{w}_{q}_fused_mae" for w in ("quiet", "storm", "recovery") for q in ("rho", "O", "N2")] + ["nees"]

# ---- NLL bookkeeping (this process only) ----
_last = {}
_update = scen.kf_update_scalar


def update_with_log_s(x, P, H, z, h, r2, **kw):
    Hb = H.expand(x.shape[0], -1) if H.dim() == 1 else H
    S = (Hb * (P @ Hb.unsqueeze(-1)).squeeze(-1)).sum(1) + r2
    _last["log_s"] = torch.log(S)
    return _update(x, P, H, z, h, r2, **kw)


class BankScorer(Scorer):
    def __init__(self, n, device, dtype):
        super().__init__(n, device, dtype)
        self.nll = torch.zeros(n, device=device, dtype=dtype)

    def add_nis(self, sensor, info):
        super().add_nis(sensor, info)
        term = 0.5 * (_last["log_s"] + info["nis"])
        self.nll = self.nll + torch.where(info["accepted"], term, torch.zeros_like(term))

    def summary(self):
        out = super().summary()
        out["nll"] = self.nll
        return out


scen.kf_update_scalar = update_with_log_s
scen.Scorer = BankScorer


# ---- bank ----
def with_so(so):
    r = list(value("R_TRUE"))
    r[O] = so
    return tuple(r)


def parse_set(items):
    out = {}
    for item in items:
        k, v = item.split("=")
        out[k] = float(v)
    return out


def run_bank(truth_so, runs, device, extra):
    nll, metrics = [], []
    for so in GRID:
        s = OSSE(R_TRUE=with_so(truth_so), R_FILT=with_so(so), **extra)
        r, sec = simt.run(s, runs, s.n_steps, seed=1, device=device, dtype=torch.float64)
        nll.append(r["nll"].cpu().numpy())
        metrics.append({k: r[k].cpu().numpy() for k in KEYS})
        print(f"    filter S_O {so:.2f}: mean NLL {nll[-1].mean():12.1f}   quiet N2 MAE p50 "
              f"{np.median(metrics[-1]['quiet_N2_fused_mae']):.3f}   NEES p50 {np.median(metrics[-1]['nees']):.2f}"
              f"   ({sec:.0f} s)", flush=True)
    nll = np.stack(nll)                        # (grid, runs)
    w = np.exp(-(nll - nll.min(0)))
    w /= w.sum(0)
    grid = np.array(GRID)
    est = (w * grid[:, None]).sum(0)
    best = nll.argmin(0)
    picked = {k: np.stack([m[k] for m in metrics])[best, np.arange(runs)] for k in KEYS}
    fixed = metrics[GRID.index(DEFAULT_SO)]
    oracle = metrics[GRID.index(truth_so)] if truth_so in GRID else None
    return est, best, w, picked, fixed, oracle


def pct(a):
    return f"p10 {np.percentile(a, 10):.3f}  p50 {np.median(a):.3f}  p90 {np.percentile(a, 90):.3f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--truths", type=float, nargs="+", default=[0.56, 0.66, 0.77])
    ap.add_argument("--runs", type=int, default=200)
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--set", nargs="*", default=[], help="param overrides, e.g. O_DRIFT_MEAN=0")
    ap.add_argument("--tag", default="default")
    args = ap.parse_args()
    extra = parse_set(args.set)

    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    print(f"grid {GRID}, filter default S_O {DEFAULT_SO}, overrides {extra or 'none'}, {args.runs} runs")
    for t in args.truths:
        print(f"\n=== truth S_O {t:.2f} ===", flush=True)
        est, best, w, picked, fixed, oracle = run_bank(t, args.runs, args.device, extra)
        print(f"  estimate          {pct(est)}   (truth {t:.2f})")
        print(f"  estimate - truth  mean {np.mean(est - t):+.3f}  rms {np.sqrt(np.mean((est - t) ** 2)):.3f}")
        counts = np.bincount(best, minlength=len(GRID)) / len(best)
        print("  best grid point   " + "  ".join(f"{g:.2f}:{c:.0%}" for g, c in zip(GRID, counts)))
        print("  p50 errors        fixed 0.56 filter | bank-picked filter" + (" | true-S_O filter" if oracle else ""))
        for k in KEYS:
            line = f"    {k:<24} {np.median(fixed[k]):.4f} | {np.median(picked[k]):.4f}"
            if oracle:
                line += f" | {np.median(oracle[k]):.4f}"
            print(line)
        for i in range(len(est)):
            row = {"truth_so": t, "run": i, "estimate": est[i], "best": GRID[best[i]]}
            row.update({f"w_{g:.2f}": w[j, i] for j, g in enumerate(GRID)})
            row.update({f"picked_{k}": picked[k][i] for k in KEYS})
            row.update({f"fixed_{k}": fixed[k][i] for k in KEYS})
            rows.append(row)

    path = OUT / f"{args.tag}.csv"
    with open(path, "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0]))
        wr.writeheader()
        wr.writerows(rows)
    print(f"\nwrote {path}")


if __name__ == "__main__":
    main()
