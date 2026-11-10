import sys
from pathlib import Path

import numpy as np
import simt
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from osse.filter import correction
from osse.params import value
from osse.scenario import OSSE
from osse.smoother import rts

WINDOWS = ("quiet", "storm", "recovery")


def products(x, s, phase):
    K, N, _ = x.shape
    e = torch.exp(correction(x.reshape(K * N, -1))[:, s.gidx]).reshape(K, N, -1)
    n = s.prior[phase].transpose(0, 1) * e
    return {"rho": (n * s.mass).sum(-1) * value("AMU"), "O": n[..., s.o_idx], "N2": n[..., s.n2_idx]}


def mae(est, truth, hours, w):
    h0, h1 = value(f"{w.upper()}_HOURS")
    m = (hours >= h0) & (hours < h1)
    return (est[m] / truth[m] - 1).abs().mean(0)


def main():
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    tv = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    sensors = ("gauge", "o", "drag", "leak") if "leak" in sys.argv[3:] else ("gauge", "o", "drag")
    s = OSSE(TRUTH_MSIS_VERSION=tv, USE_SENSORS=sensors)
    r, sec = simt.run(s, runs, s.n_steps, seed=1, dtype=torch.float64, record_runs=runs)
    ser = r.series
    phase = r["phase"][:runs]
    truth = {"rho": ser["rho_truth"], "O": ser["O_truth"], "N2": ser["N2_truth"]}
    hours = torch.arange(ser["x"].shape[0], dtype=torch.float64) * s.dt / 3600
    xs, _ = rts(ser["x"], ser["P"], s.F, s.Qd)
    filt, smooth = products(ser["x"], s, phase), products(xs, s, phase)
    print(f"truth v{tv:g}, sensors {sensors}, {runs} runs ({sec:.0f} s)")
    print("self-check (must match): scorer quiet rho MAE p50",
          f"{np.median(r['quiet_rho_fused_mae'][:runs].numpy()):.4f}",
          f"vs recomputed {mae(filt['rho'], truth['rho'], hours, 'quiet').median():.4f}")
    for w in WINDOWS:
        line = f"  {w:<9}"
        for q in ("rho", "O", "N2"):
            f = mae(filt[q], truth[q], hours, w).quantile(0.5)
            sm = mae(smooth[q], truth[q], hours, w).quantile(0.5)
            line += f"  {q} {f:.3f} -> {sm:.3f}"
        print(line)


if __name__ == "__main__":
    main()