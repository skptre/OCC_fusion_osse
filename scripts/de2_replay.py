import argparse
import sys
from pathlib import Path

import numpy as np
import simt
import torch
import ast

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from osse.de2 import DE2Replay


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("window")
    ap.add_argument("--prior", default="2.1")
    ap.add_argument("--runs", type=int, default=200)
    ap.add_argument("--set", nargs="*", default=[], help='overrides, e.g. "P0_MSIS_SD=(0.2,0.35,0.2)"')
    args = ap.parse_args()
    over = {k: ast.literal_eval(v) for k, v in (kv.split("=", 1) for kv in args.set)}
    s = DE2Replay(args.window, prior=args.prior, **over)
    r, sec = simt.run(s, args.runs, s.n_steps, seed=1, dtype=torch.float64)
    print(f"{args.window}, prior MSIS {args.prior}, {args.runs} runs ({sec:.0f} s); MAE p50 (bias p50)")
    for w in s._windows():
        cells = []
        for q in ("rho", "O", "N2"):
            med = lambda key: float(np.nanmedian(r[f"{w}_{q}_{key}"].numpy()))
            cells.append(f"{q} model {med('prior_mae'):.3f} ({med('prior_bias'):+.3f}) -> ours "
                         f"{med('fused_mae'):.3f} ({med('fused_bias'):+.3f})")
        print(f"  {w}: " + " | ".join(cells))
    print(f"  NEES p50 {float(np.nanmedian(r['nees'].numpy())):.2f}")


if __name__ == "__main__":
    main()