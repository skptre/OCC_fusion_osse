"""GRACE-FO May 2024 superstorm figure (held-out real data): forecast-driven NRLMSIS 2.1 vs our fused density
(baseline hardware, no leak) vs GRACE-FO accelerometer density (TOLEOS v0003). Orbit-averaged for readability.
Run from the repo root (CPU, ~1 min):  python scripts/fig_gracefo.py
Writes out/figures/fig_gracefo.png and out/figures/gracefo_series.csv."""
import csv
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import simt
import torch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from osse.de2 import DE2Replay
from osse.filter import correction
from osse.params import value

OUT = REPO / "out" / "figures"
ORBIT_S = 5640.0  # ~94 min GRACE-FO period
C_MODEL, C_OURS, C_TRUTH = "#9aa4ad", "#0b6e8a", "#222222"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})


def fused_density(s, x, steps):
    """x: (K, N, S) recorded states -> fused and prior density (K, N)."""
    K, N, _ = x.shape
    dz = torch.as_tensor(((s._altitude() - s.alt_km) / 100.0)[0, steps], dtype=x.dtype)
    dz = dz[:, None].expand(K, N).reshape(-1)
    gidx = torch.as_tensor(value("GROUP"))
    e = torch.exp(correction(x.reshape(K * N, -1), None, dz)[:, gidx]).reshape(K, N, -1)
    prior = torch.as_tensor(s.prior_np[0, steps], dtype=x.dtype)[:, None, :]
    mass = torch.as_tensor(value("MASS"), dtype=x.dtype)
    rho = lambda n: (n * mass).sum(-1) * value("AMU")
    return rho(prior * e), rho(prior.expand(K, N, -1))


def orbit_mean(t, y, ok):
    b = np.floor(t / ORBIT_S).astype(int)
    tt, yy = [], []
    for k in np.unique(b[ok]):
        m = ok & (b == k)
        tt.append(t[m].mean())
        yy.append(np.exp(np.log(y[m]).mean()))
    return np.array(tt), np.array(yy)


def main():
    s = DE2Replay("gracefo_2024-05", prior="2.1", USE_SENSORS=("gauge", "o", "drag"))
    r, sec = simt.run(s, 50, s.n_steps, seed=1, dtype=torch.float64, record_runs=1, record_every=2)
    steps = r.series["step"].long().numpy()
    x = r.series["x"]
    rho_f, rho_p = fused_density(s, x, steps)
    rho_f, rho_p = rho_f[:, 0].numpy(), rho_p[:, 0].numpy()
    truth = r.series["rho_truth"][:, 0].numpy()
    ok = s.cover_np[0, steps].astype(bool) & np.isfinite(truth) & (truth > 0)
    hours = steps * s.dt / 3600
    t = steps * s.dt
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "gracefo_series.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["hours", "rho_gracefo", "rho_model", "rho_fused", "covered"])
        w.writerows(zip(hours, truth, rho_p, rho_f, ok.astype(int)))
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
    for y, col, lab in ((rho_p, C_MODEL, "NRLMSIS 2.1, forecast drivers"), (truth, C_TRUTH, "GRACE-FO (held out)"),
                        (rho_f, C_OURS, "Aether fused (baseline, simulated sensors)")):
        tt, yy = orbit_mean(t, y, ok)
        a1.plot(tt / 3600, yy, color=col, lw=1.6 if col == C_OURS else 1.1, label=lab)
    a1.set_yscale("log")
    a1.set_ylabel("Mass density (kg m$^{-3}$)")
    a1.legend(frameon=False, fontsize=8)
    for y, col, lab in ((rho_p, C_MODEL, "Model"), (rho_f, C_OURS, "Aether")):
        tt, yy = orbit_mean(t, y / truth, ok)
        a2.plot(tt / 3600, 100 * (yy - 1), color=col, lw=1.3, label=lab)
    a2.axhspan(-20, 20, color="#b3261e", alpha=0.07, lw=0)
    a2.axhline(0, color="#999", lw=0.5)
    a2.set_ylabel("Error vs GRACE-FO (%)")
    a2.set_xlabel("Hours after 2024-05-09 00:00 UT (shaded top: storm; band: 20% benchmark)")
    for ax in (a1, a2):
        ax.axvspan(*value("STORM_HOURS"), color="#f2d7d5", alpha=0.35, lw=0) if ax is a1 else None
    a2.legend(frameon=False, fontsize=8)
    fig.savefig(OUT / "fig_gracefo.png", dpi=300, bbox_inches="tight")
    print("wrote", OUT / "fig_gracefo.png", f"({sec:.0f} s)")
    for wn, (h0, h1) in s._windows().items():
        m = ok & (hours >= h0) & (hours < h1)
        print(f"  {wn}: model {100*np.mean(np.abs(rho_p[m]/truth[m]-1)):.1f}%  ours {100*np.mean(np.abs(rho_f[m]/truth[m]-1)):.1f}% (recorded run)")


if __name__ == "__main__":
    main()
