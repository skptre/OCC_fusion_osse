import sys
from pathlib import Path

import numpy as np
import simt
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from osse.filter import IDX, WC, HARM, correction, group_H
from osse.params import value
from osse.scenario import OSSE
from osse.smoother import rts

WINDOWS = ("quiet", "storm", "recovery")
DELTA = 0.01
E = IDX["ln_so"]


def products(x, s, phase):
    K, N, _ = x.shape
    b = s.basis_t[phase].transpose(0, 1).reshape(K * N, -1) if s.harm_on else None
    e = torch.exp(correction(x.reshape(K * N, -1), b)[:, s.gidx]).reshape(K, N, -1)
    n = s.prior[phase].transpose(0, 1) * e
    return {"rho": (n * s.mass).sum(-1) * value("AMU"), "O": n[..., s.o_idx], "N2": n[..., s.n2_idx]}


def mae(est, truth, hours, w):
    h0, h1 = value(f"{w.upper()}_HOURS")
    m = (hours >= h0) & (hours < h1)
    return (est[m] / truth[m] - 1).abs().mean(0)


def log_sd(x, P, s, phase):
    K, N, ns = x.shape
    xf = x.reshape(K * N, ns)
    b = s.basis_t[phase].transpose(0, 1).reshape(K * N, -1) if s.harm_on else None
    d = s.dz_t[phase].transpose(0, 1).reshape(K * N)
    n = s.prior[phase].transpose(0, 1).reshape(K * N, -1) * torch.exp(correction(xf, b, d)[:, s.gidx])
    a_rho, _ = group_H(n * s.mass, s.G, IDX["cd_bias"], b, d)
    a_rho[:, IDX["cd_bias"]] = 0.0
    grads = {"rho": a_rho[:, :ns]}
    for g in ("O", "N2"):
        a = torch.zeros_like(xf)
        a[:, [IDX[f"gap_{g}"], WC, IDX[f"w_{g}"]]] = 1.0
        if g == "N2" and b is not None:
            a[:, HARM] = b
        a[:, IDX[f"dz_{g}"]] = d
        grads[g] = a
    Pf = P.reshape(K * N, ns, ns)
    return {q: torch.einsum("bi,bij,bj->b", a, Pf, a).clamp(min=0).sqrt().reshape(K, N) for q, a in grads.items()}


def zstats(est, truth, sd, hours, w):
    h0, h1 = value(f"{w.upper()}_HOURS")
    m = (hours >= h0) & (hours < h1)
    z = torch.log(est[m] / truth[m]) / sd[m]
    return z.pow(2).mean().sqrt().item(), (z.abs() < 1).double().mean().item()


def run(runs, overrides):
    s = OSSE(**overrides)
    r, sec = simt.run(s, runs, s.n_steps, seed=1, dtype=torch.float64, record_runs=runs)
    return s, r, sec


def smooth(ser, s):
    return rts(ser["x"][..., :E], ser["P"][..., :E, :E], s.F[:E, :E], s.Qd[:E, :E])


def main():
    runs = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    tv = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    sensors = ("gauge", "o", "drag", "leak") if "leak" in sys.argv[3:] else ("gauge", "o", "drag")
    base = dict(TRUTH_MSIS_VERSION=tv, USE_SENSORS=sensors, SO_MODE="off", SO_TRUTH_SD=value("SO_SD"))
    s, r, sec = run(runs, base)
    _, r2, _ = run(runs, {**base, "SO_TRUTH_OFFSET": DELTA})
    ser, ser2 = r.series, r2.series
    phase = r["phase"][:runs]
    truth = {"rho": ser["rho_truth"], "O": ser["O_truth"], "N2": ser["N2_truth"]}
    hours = torch.arange(ser["x"].shape[0], dtype=torch.float64) * s.dt / 3600

    xs, Ps = smooth(ser, s)
    xs2, _ = smooth(ser2, s)
    xf, Pf = ser["x"][..., :E], ser["P"][..., :E, :E]
    filt, smoo = products(xf, s, phase), products(xs, s, phase)
    filt2, smoo2 = products(ser2["x"][..., :E], s, phase), products(xs2, s, phase)
    so2 = value("SO_SD") ** 2
    sd_f = {q: (v ** 2 + so2 * (torch.log(filt2[q] / filt[q]) / DELTA) ** 2).sqrt()
            for q, v in log_sd(xf, Pf, s, phase).items()}
    sd_s = {q: (v ** 2 + so2 * (torch.log(smoo2[q] / smoo[q]) / DELTA) ** 2).sqrt()
            for q, v in log_sd(xs, Ps, s, phase).items()}

    print(f"truth v{tv:g}, sensors {sensors}, {runs} runs, true S_O drawn (sd {value('SO_SD')}) ({sec:.0f} s per run)")
    print("self-check (must match): scorer quiet rho MAE p50",
          f"{np.median(r['quiet_rho_fused_mae'][:runs].numpy()):.4f}",
          f"vs recomputed {mae(filt['rho'], truth['rho'], hours, 'quiet').quantile(0.5):.4f}")
    for w in WINDOWS:
        line = f"  {w:<9}"
        for q in ("rho", "O", "N2"):
            line += (f"  {q} {mae(filt[q], truth[q], hours, w).quantile(0.5):.3f}"
                     f" -> {mae(smoo[q], truth[q], hours, w).quantile(0.5):.3f}")
        print(line)
    print("error-bar honesty with S_O consider term: z rms (1 = honest), share inside 1 sigma (0.68), filter | smoothed")
    for w in WINDOWS:
        line = f"  {w:<9}"
        for q in ("rho", "O", "N2"):
            zf, cf = zstats(filt[q], truth[q], sd_f[q], hours, w)
            zs, cs = zstats(smoo[q], truth[q], sd_s[q], hours, w)
            line += f"  {q} z {zf:.2f}|{zs:.2f} in {cf:.2f}|{cs:.2f}"
        print(line)


if __name__ == "__main__":
    main()