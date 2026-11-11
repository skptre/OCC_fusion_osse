"""Phase B: ground RTS smoother + honest error bars, on the same runs as the real-time filter.

Two modes:
  default (S_O NOT ground-calibrated): estimate with S_O fixed at nominal (SO_MODE off) -> filter + RTS smoother;
      uncertainty = smoother covariance + (d ln product / d ln S_O)^2 * SO_BRACKET_SD^2, the sensitivity measured by
      re-running the same data with the true S_O shifted by DELTA (consider analysis, Bierman 1977).
  est (the architecture): ground-anchored in-flight S_O estimation (register defaults SO_MODE estimate, SO_SD 0.05);
      S_O is an estimated state, so the smoother runs on all states and no consider term is added.
Usage: python scripts/smooth_test.py [runs=30] [truth_version=0] [leak] [est] [perturbed]
Memory: about 1.5 GB per 30 runs (two recorded runs in default mode, one in est mode)."""
import sys
from pathlib import Path

import numpy as np
import simt
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from osse.filter import IDX, N_STATES, WC, HARM, correction, group_H
from osse.params import value
from osse.scenario import OSSE
from osse.smoother import rts

WINDOWS = ("quiet", "storm", "recovery")
DELTA = 0.01


def flat_extras(s, phase, K, N):
    b = s.basis_t[phase].transpose(0, 1).reshape(K * N, -1) if s.harm_on else None
    d = s.dz_t[phase].transpose(0, 1).reshape(K * N)
    return b, d


def products(x, s, phase):
    K, N, _ = x.shape
    b, d = flat_extras(s, phase, K, N)
    e = torch.exp(correction(x.reshape(K * N, -1), b, d)[:, s.gidx]).reshape(K, N, -1)
    n = s.prior[phase].transpose(0, 1) * e
    return {"rho": (n * s.mass).sum(-1) * value("AMU"), "O": n[..., s.o_idx], "N2": n[..., s.n2_idx]}


def mae(est, truth, hours, w):
    h0, h1 = value(f"{w.upper()}_HOURS")
    m = (hours >= h0) & (hours < h1)
    return (est[m] / truth[m] - 1).abs().mean(0)


def log_sd(x, P, s, phase):
    K, N, ns = x.shape
    xf = x.reshape(K * N, ns)
    b, d = flat_extras(s, phase, K, N)
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


def smooth(ser, s, E):
    """RTS on the active states only: switched-off states (e.g. N2 harmonics, prior variance 1e-12) make the
    predicted covariance near-singular and corrupt the smoother gain; they are never updated, so they are copied."""
    act = torch.tensor([i for i in range(E) if float(s.P0[i, i]) > 1e-9])
    xf, Pf = ser["x"][..., :E], ser["P"][..., :E, :E]
    xa, Pa = rts(xf[..., act], Pf[..., act[:, None], act], s.F[act[:, None], act], s.Qd[act[:, None], act])
    xs, Ps = xf.clone(), Pf.clone()
    xs[..., act] = xa
    Ps[..., act[:, None], act] = Pa
    return xs, Ps


def main():
    args = sys.argv[1:]
    runs = int(args[0]) if len(args) > 0 else 30
    tv = float(args[1]) if len(args) > 1 else 0.0
    tv = int(tv) if tv == int(tv) else tv  # pymsis accepts version 0 (int), 2.0, 2.1
    sensors = ("gauge", "o", "drag", "leak") if "leak" in args[2:] else ("gauge", "o", "drag")
    est_mode = "est" in args[2:]
    base = dict(TRUTH_MSIS_VERSION=tv, USE_SENSORS=sensors)
    if "perturbed" in args[2:]:
        base["TRUTH_KIND"] = "perturbed"
    if est_mode:
        base.update(SO_MODE="estimate", SO_SD=value("SO_SD"), SO_TRUTH_SD=value("SO_SD"))
        E, so_sd = N_STATES, 0.0
    else:
        base.update(SO_MODE="off", SO_TRUTH_SD=value("SO_BRACKET_SD"))
        E, so_sd = IDX["ln_so"], value("SO_BRACKET_SD")

    s, r, sec = run(runs, base)
    ser = r.series
    phase = r["phase"][:runs]
    truth = {"rho": ser["rho_truth"], "O": ser["O_truth"], "N2": ser["N2_truth"]}
    hours = torch.arange(ser["x"].shape[0], dtype=torch.float64) * s.dt / 3600

    xs, Ps = smooth(ser, s, E)
    xf, Pf = ser["x"][..., :E], ser["P"][..., :E, :E]
    filt, smoo = products(xf, s, phase), products(xs, s, phase)
    sd_f, sd_s = log_sd(xf, Pf, s, phase), log_sd(xs, Ps, s, phase)
    if not est_mode:
        _, r2, _ = run(runs, {**base, "SO_TRUTH_OFFSET": DELTA})
        xs2, _ = smooth(r2.series, s, E)
        filt2, smoo2 = products(r2.series["x"][..., :E], s, phase), products(xs2, s, phase)
        sd_f = {q: (v ** 2 + so_sd ** 2 * (torch.log(filt2[q] / filt[q]) / DELTA) ** 2).sqrt() for q, v in sd_f.items()}
        sd_s = {q: (v ** 2 + so_sd ** 2 * (torch.log(smoo2[q] / smoo[q]) / DELTA) ** 2).sqrt() for q, v in sd_s.items()}

    mode = "S_O ground-calibrated + estimated" if est_mode else f"S_O uncalibrated, consider analysis (sd {so_sd})"
    print(f"truth v{tv:g}{' perturbed' if 'perturbed' in args[2:] else ''}, sensors {sensors}, {mode}, "
          f"{runs} runs ({sec:.0f} s per run)")
    print("self-check (must match): scorer quiet rho MAE p50",
          f"{np.median(r['quiet_rho_fused_mae'][:runs].numpy()):.4f}",
          f"vs recomputed {mae(filt['rho'], truth['rho'], hours, 'quiet').quantile(0.5):.4f}")
    print("MAE p50, filter -> smoothed")
    for w in WINDOWS:
        line = f"  {w:<9}"
        for q in ("rho", "O", "N2"):
            line += (f"  {q} {mae(filt[q], truth[q], hours, w).quantile(0.5):.3f}"
                     f" -> {mae(smoo[q], truth[q], hours, w).quantile(0.5):.3f}")
        print(line)
    print("error-bar honesty: z rms (1 = honest; >1 = bars too small by that factor), share inside 1 sigma (0.68), "
          "filter | smoothed")
    for w in WINDOWS:
        line = f"  {w:<9}"
        for q in ("rho", "O", "N2"):
            zf, cf = zstats(filt[q], truth[q], sd_f[q], hours, w)
            zs, cs = zstats(smoo[q], truth[q], sd_s[q], hours, w)
            line += f"  {q} z {zf:.2f}|{zs:.2f} in {cf:.2f}|{cs:.2f}"
        print(line)


if __name__ == "__main__":
    main()
