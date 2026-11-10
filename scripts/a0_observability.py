import sys
from pathlib import Path

import numpy as np
import simt
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from osse.filter import STATES
from osse.params import value
from osse.scenario import OSSE

N_RUNS = 4
EVERY = 120
WINDOWS = ("QUIET_HOURS", "STORM_HOURS", "RECOVERY_HOURS")


def record(**ov):
    s = OSSE(**ov)
    r, _ = simt.run(s, N_RUNS, s.n_steps, seed=1, dtype=torch.float64,
                    record_runs=N_RUNS, record_every=EVERY)
    return s, r.series


def masks(hours):
    out = {}
    for w in WINDOWS:
        h0, h1 = value(w)
        out[w.split("_")[0].lower()] = (hours >= h0) & (hours < h1)
    return out


def main():
    s, ser = record()
    _, ser0 = record(USE_SENSORS=())
    hours = ser["step"].numpy() * value("DT") / 3600
    P, P0 = ser["P"].numpy(), ser0["P"].numpy()
    win = masks(hours)

    print("1) uncertainty remaining vs prior-only (sd ratio %, mean over window and runs)")
    print(f"{'state':<12}" + "".join(f"{w:>11}" for w in win))
    for i, name in enumerate(STATES):
        ratio = np.sqrt(P[:, :, i, i] / P0[:, :, i, i])
        print(f"{name:<12}" + "".join(f"{100 * ratio[m].mean():>10.1f}%" for m in win.values()))

    print("\n2) least-observed directions at mid-window (run 0); 1 = unobserved, 0 = fully observed")
    for w, m in win.items():
        ks = np.flatnonzero(m)
        k = ks[len(ks) // 2]
        sl = [STATES.index(n) for n in ("gap_O", "gap_N2", "gap_He", "gauge_gain", "o_gain", "cd_bias")]
        Pk, P0k = P[k, 0][np.ix_(sl, sl)], P0[k, 0][np.ix_(sl, sl)]
        L = np.linalg.cholesky(P0k)
        Li = np.linalg.inv(L)
        lam, V = np.linalg.eigh(Li @ Pk @ Li.T)
        print(f"  {w}: largest remaining fractions {np.round(lam[::-1][:4], 3)}")
        for j in (1, 2):
            v = L @ V[:, -j]
            v = v / np.abs(v).max()
            top = np.argsort(-np.abs(v))[:4]
            print(f"     direction {j}: " + ", ".join(f"{STATES[sl[t]]} {v[t]:+.2f}" for t in top))

    print("\n3) Fisher check: within-orbit variation of each group's share of the gauge signal")
    R = np.array(value("R_FILT"))
    G = np.eye(3)[list(value("GROUP"))]
    terms = s.prior_np * R
    share = (terms / terms.sum(-1, keepdims=True)) @ G
    h_all = np.arange(share.shape[1]) * value("DT") / 3600
    for w in WINDOWS:
        h0, h1 = value(w)
        sh = share[:, (h_all >= h0) & (h_all < h1)]
        n_orb = sh.shape[1] // s.nper
        sh = sh[:, :n_orb * s.nper].reshape(sh.shape[0], n_orb, s.nper, 3)
        mean, sd = sh.mean((0, 1, 2)), sh.std(2).mean((0, 1))
        print(f"  {w.split('_')[0].lower():<9}" + "  ".join(
            f"{g}: share {mean[i]:.2f} +- {sd[i]:.3f}" for i, g in enumerate(("O", "N2", "He"))))


if __name__ == "__main__":
    main()