import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import simt
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from osse.params import value
from osse.scenario import OSSE

N_RUNS = 4
RECORD_EVERY = 10
OUT = Path("out/timeseries_n2.png")


def shade(ax):
    for name, color in (("QUIET_HOURS", "tab:green"), ("STORM_HOURS", "tab:red")):
        h0, h1 = value(name)
        ax.axvspan(h0, h1, color=color, alpha=0.08)
    ax.axhline(0, color="k", lw=0.6)
    ax.grid(alpha=0.3)


def main():
    s = OSSE(O_DRIFT_MEAN=0.0)
    r, _ = simt.run(s, N_RUNS, s.n_steps, seed=1, dtype=torch.float64,
                    record_runs=N_RUNS, record_every=RECORD_EVERY)
    ser = {k: v.numpy() for k, v in r.series.items()}
    hours = ser["step"] * value("DT") / 3600

    fig, ax = plt.subplots(4, 1, figsize=(11, 13), sharex=True)
    for j in range(N_RUNS):
        c = f"C{j}"
        for row, gas in ((0, "N2"), (1, "O")):
            ax[row].plot(hours, ser[f"{gas}_fused"][:, j] / ser[f"{gas}_truth"][:, j] - 1, c, lw=1)
            ax[row].plot(hours, ser[f"{gas}_prior"][:, j] / ser[f"{gas}_truth"][:, j] - 1, c, lw=1, ls=":")
        ax[2].plot(hours, ser["gauge_gain_est"][:, j] - ser["gauge_gain_true"][:, j], c, lw=1)
        ax[3].plot(hours, ser["o_gain_est"][:, j] - ser["o_gain_true"][:, j], c, lw=1)

    err0 = np.log(ser["N2_fused"][:, 0] / ser["N2_truth"][:, 0])
    sd0 = ser["N2_sd"][:, 0]
    ax[0].fill_between(hours, np.exp(err0 - sd0) - 1, np.exp(err0 + sd0) - 1, color="C0", alpha=0.15)

    ax[0].set_ylabel("N2 error (est/truth - 1)")
    ax[1].set_ylabel("O error (est/truth - 1)")
    ax[2].set_ylabel("gauge gain error (ln)")
    ax[3].set_ylabel("O gain error (ln)")
    ax[3].set_xlabel("hours after T0 (2024-05-09 00 UTC)")
    ax[0].set_title("solid = fused, dotted = prior (NOAA-forecast MSIS); band = run 0 filter +-1 sigma; "
                    "green = quiet window, red = storm window")
    for a in ax:
        shade(a)
    fig.tight_layout()
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=130)
    print("saved", OUT)


if __name__ == "__main__":
    main()