"""Stage 6: effective-driver fit ("the data improve the model").
Every 3 h block, fit two numbers -- an effective F10.7 scale and an effective ap scale applied to the forecast drivers --
so NRLMSIS 2.1 matches the FUSED density and atomic O (weighted by the filter covariance x product calibration factors).
Then evaluate the corrected model where we did NOT measure:
  (a1) other altitudes (250-500 km, same ground track and times) vs truth,
  (a2) forecast: hold the last fitted correction and run 3/6/12/24 h ahead vs the plain forecast-driven model,
  (b)  other gases (He, O2, N, Ar, H) vs truth -- model-based inference, not a measurement.
Truth = whatever the headline case used (harsh: NRLMSISE-00 + calibrated driver errors), rebuilt exactly from the
fixed-seed truth driver errors; the fit uses MSIS 2.1, so it cannot match truth by construction.
Run from anywhere (CPU, minutes):  python scripts/driver_fit.py [--case base_harsh]
Reads out/headline/<case>_series.pt (falls back to harsh_series.pt); writes out/stage6/*.csv and *.png."""
import argparse
import csv
import math
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
os.chdir(REPO)  # space-weather file, forecast dir and MSIS cache are repo-relative

from pymsis.utils import get_f107_ap, use_space_weather_file

from osse.atmosphere import orbit, run_msis, truth_errors
from osse.filter import DZ, GAP, HARM, WC, WG, lt_basis
from osse.forecasts import prior_ap_array
from osse.params import value
from osse.scenario import OSSE

HL = REPO / "out" / "headline"
OUT = REPO / "out" / "stage6"
BLOCK_H = 3.0                       # choice: ap cadence (3-hourly index)
ALTS = (250, 300, 350, 400, 450, 500)
LEADS_H = (3, 6, 12, 24)
CAL = {"rho": 2.0, "O": 2.8}        # product z-score calibration factors (claims register, headline z-check)
REPR_SD = 0.05                      # choice: model-representation floor (2-knob MSIS cannot follow wiggles)
FIRST_SD = (0.3, 1.0)               # choice: prior sd on (ln F10.7 scale, ln ap scale) for the first block
WALK_SD = (0.1, 0.7)                # choice: allowed change block-to-block (truth driver errors: tau 12 h)
BOUNDS = np.array([(-1.0, 1.0), (-3.0, 3.0)])
F107_RANGE = (60.0, 400.0)          # physical cap on the EFFECTIVE solar index (sfu), fit and forecast
AP_MAX = 400.0                      # top of the ap scale; effective ap never exceeds it
DAMP_TAU_H = 12.0                   # choice: forecast correction decays exp(-lead/12 h) = driver-error correlation
                                    # time of the calibrated truth (Bruinsma & Laurens 2024 scatter calibration)
FD = 0.01
N_GN = 8
WIN = {"quiet": value("QUIET_HOURS"), "storm": value("STORM_HOURS"), "recovery": value("RECOVERY_HOURS"),
       "all": (value("QUIET_HOURS")[0], value("RECOVERY_HOURS")[1])}
SPECIES = value("SPECIES")
MASS = np.array(value("MASS"))
AMU = value("AMU")
O, N2 = SPECIES.index("O"), SPECIES.index("N2")
OTHER = ("He", "O2", "N", "Ar", "H")
C_MODEL, C_OURS, C_FIT, C_TRUTH = "#9aa4ad", "#0b6e8a", "#c77b00", "#222222"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})


def rho_of(n):
    return (n * MASS).sum(1) * AMU


def version(v):
    return int(v) if float(v).is_integer() else float(v)


def drivers(s, phase, steps):
    """Everything MSIS needs along this run's recorded points, for prior, corrected and truth."""
    t = steps * s.dt
    dates = np.datetime64(value("T0")) + (t * 1e3).astype("timedelta64[ms]")
    lat, lon, _ = orbit(t, s.alt_km, 2 * math.pi * phase / s.n_phases)
    use_space_weather_file(value("SW_FILE"))
    f107, f107a, ap_truth = get_f107_ap(dates)
    d = {"t": t, "dates": dates, "lat": lat, "lon": lon, "f107": np.asarray(f107, float),
         "f107a": np.asarray(f107a, float), "ap_truth": np.asarray(ap_truth, float), "ap_prior": prior_ap_array(t)}
    zero = np.zeros(len(t))
    d["e_f"], d["e_ap"], d["e_o"] = zero, zero, zero
    if s.get("TRUTH_KIND") == "perturbed":  # same call as build_tables: fixed seed per orbit plane
        e = truth_errors(s.n_steps, phase, value("TRUTH_F107_SD"), value("TRUTH_AP_SD"), value("TRUTH_O_SD"))
        d["e_f"], d["e_ap"], d["e_o"] = (a[steps] for a in e)
    return d


def model(d, idx, alt, a, b):
    """NRLMSIS 2.1 on forecast drivers, F10.7 (daily + 81-day) scaled by exp(a), all ap columns by exp(b)."""
    a, b = np.broadcast_to(a, idx.shape), np.broadcast_to(b, idx.shape)
    f = np.clip(d["f107"][idx] * np.exp(a), *F107_RANGE)
    fa = np.clip(value("PRIOR_F107A") * np.exp(a), *F107_RANGE)
    ap = np.clip(d["ap_prior"][idx] * np.exp(b)[:, None], 0.0, AP_MAX)
    return run_msis(d["dates"][idx], d["lat"][idx], d["lon"][idx], alt, f, fa, ap, value("MSIS_VERSION"))


def truth(s, d, idx, alt):
    n = run_msis(d["dates"][idx], d["lat"][idx], d["lon"][idx], alt, d["f107"][idx] * np.exp(d["e_f"][idx]),
                 d["f107a"][idx], d["ap_truth"][idx] * np.exp(d["e_ap"][idx])[:, None],
                 version(s.get("TRUTH_MSIS_VERSION")))
    if s.get("TRUTH_KIND") == "perturbed":
        n[:, O] *= np.exp(d["e_o"][idx])
    return n


def fused(s, ser, r, steps):
    """Fused rho and O at the recorded points + their 2x2 log covariance (rho, O) from the filter P."""
    x = ser["x"][:, r].double().numpy()
    P = ser["P"][:, r].double().numpy()
    phase = int(ser["phase"][r])
    prior = s.prior_np[phase, steps]
    dz = ((s._altitude() - s.alt_km) / 100.0)[phase, steps]
    harm = s.get("N2_LT_HARMONICS") > 0
    basis = lt_basis(s._local_time())[phase, steps] if harm else None
    c = x[:, GAP] + x[:, [WC]] + x[:, WG] + x[:, DZ] * dz[:, None]
    if harm:
        c[:, 1] += (x[:, HARM] * basis).sum(1)
    gidx = np.array(value("GROUP"))
    nf = prior * np.exp(c[:, gidx])
    K = len(steps)
    Ag = np.zeros((K, 3, x.shape[1]))
    for g in range(3):
        Ag[:, g, g] = 1.0
        Ag[:, g, WC] = 1.0
        Ag[:, g, WG.start + g] = 1.0
        Ag[:, g, DZ.start + g] = dz
    if harm:
        Ag[:, 1, HARM] = basis
    m = nf * MASS
    share = np.stack([m[:, gidx == g].sum(1) for g in range(3)], 1) / m.sum(1, keepdims=True)
    A = np.stack([np.einsum("kg,kgs->ks", share, Ag), Ag[:, 0]], 1)        # rows: ln rho, ln O
    C = A @ P @ A.transpose(0, 2, 1)
    D = np.diag([CAL["rho"], CAL["O"]])
    C = D @ C @ D + REPR_SD ** 2 * np.eye(2)
    return {"phase": phase, "n": nf, "rho": rho_of(nf), "y": np.stack([np.log(rho_of(nf)), np.log(nf[:, O])], 1),
            "Winv": np.linalg.inv(C)}


def obs(d, idx, alt, th):
    n = model(d, idx, alt, th[0], th[1])
    return np.stack([np.log(rho_of(n)), np.log(n[:, O])], 1)


def fit_block(d, idx, alt, y, Winv, th_p, sd_p):
    """Gauss-Newton on 2 parameters with a Gaussian pull towards the previous block's fit."""
    lam = 1.0 / np.asarray(sd_p) ** 2
    th = th_p.copy()
    for _ in range(N_GN):
        f0 = obs(d, idx, alt, th)
        J = np.stack([(obs(d, idx, alt, th + FD * np.eye(2)[j]) - f0) / FD for j in range(2)], -1)
        r = y - f0
        H = np.einsum("nki,nkl,nlj->ij", J, Winv, J) + np.diag(lam)
        g = np.einsum("nki,nkl,nl->i", J, Winv, r) - lam * (th - th_p)
        step = np.clip(np.linalg.solve(H, g), -1.0, 1.0)
        th = np.clip(th + step, BOUNDS[:, 0], BOUNDS[:, 1])
        if np.abs(step).max() < 1e-4:
            break
    return th, np.sqrt(np.diag(np.linalg.inv(H)))


def mae(est, tru, hours, w, extra=None):
    lo, hi = WIN[w]
    m = (hours >= lo) & (hours < hi)
    if extra is not None:
        m &= extra
    return float(np.mean(np.abs(est[m] / tru[m] - 1))) if m.any() else np.nan


def one_run(s, ser, r, steps, hours):
    f = fused(s, ser, r, steps)
    d = drivers(s, f["phase"], steps)
    alt = s.alt_km
    all_idx = np.arange(len(steps))
    # self-check: our rebuilt prior / truth must equal the scenario tables at these steps
    prior0 = model(d, all_idx, alt, 0.0, 0.0)
    tab0 = truth(s, d, all_idx, alt)
    chk_p = np.max(np.abs(prior0 / np.maximum(s.prior_np[f["phase"], steps], 1e-30) - 1)[:, [N2, O]])
    chk_t = np.max(np.abs(tab0 / np.maximum(s.truth_np[f["phase"], steps], 1e-30) - 1)[:, [N2, O]])
    print(f"  run {r} (orbit plane {f['phase']}): rebuild check prior {chk_p:.1e}, truth {chk_t:.1e}"
          + ("" if max(chk_p, chk_t) < 1e-6 else "   <-- MISMATCH, tell Claude"), flush=True)

    blk = np.floor(hours / BLOCK_H).astype(int)
    nb = blk.max() + 1
    theta, sd = np.zeros((nb, 2)), np.zeros((nb, 2))
    th_p, sd_p = np.zeros(2), FIRST_SD
    for j in range(nb):
        idx = np.where(blk == j)[0]
        theta[j], sd[j] = fit_block(d, idx, alt, f["y"][idx], f["Winv"][idx], th_p, sd_p)
        th_p, sd_p = theta[j], WALK_SD
    a_pt, b_pt = theta[blk, 0], theta[blk, 1]

    rows_fit = []
    for j in range(nb):
        idx = blk == j
        rows_fit.append({"run": r, "orbit_plane": f["phase"], "block": j, "t_start_h": j * BLOCK_H,
                         "ln_f107_scale": theta[j, 0], "ln_ap_scale": theta[j, 1], "sd_ln_f107": sd[j, 0],
                         "sd_ln_ap": sd[j, 1],
                         "f107_prior": d["f107"][idx].mean(),
                         "f107_fit": np.clip(d["f107"][idx] * np.exp(theta[j, 0]), *F107_RANGE).mean(),
                         "f107_truth": (d["f107"][idx] * np.exp(d["e_f"][idx])).mean(),
                         "ap_prior": d["ap_prior"][idx, 1].mean(),
                         "ap_fit": np.clip(d["ap_prior"][idx, 1] * np.exp(theta[j, 1]), 0.0, AP_MAX).mean(),
                         "ap_truth": (d["ap_truth"][idx, 1] * np.exp(d["e_ap"][idx])).mean()})

    # satellite altitude, judged against the run's own truth (incl. small-scale wiggles), like the headline
    corr = model(d, all_idx, alt, a_pt, b_pt)
    sat_truth = {"rho": ser["rho_truth"][:, r].double().numpy(), "O": ser["O_truth"][:, r].double().numpy(),
                 "N2": ser["N2_truth"][:, r].double().numpy()}
    sat = {}
    for w in WIN:
        for q, est_p, est_c, est_f in (("rho", rho_of(prior0), rho_of(corr), f["rho"]),
                                       ("O", prior0[:, O], corr[:, O], f["n"][:, O]),
                                       ("N2", prior0[:, N2], corr[:, N2], f["n"][:, N2])):
            sat[(w, q)] = tuple(mae(e, sat_truth[q], hours, w) for e in (est_p, est_c, est_f))

    # (a1) other altitudes, same ground track / times; truth = column truth (no small-scale wiggles)
    col = {}
    for z in ALTS:
        tz = truth(s, d, all_idx, z)
        pz = model(d, all_idx, z, 0.0, 0.0)
        cz = model(d, all_idx, z, a_pt, b_pt)
        for w in WIN:
            col[(z, w, "rho")] = (mae(rho_of(pz), rho_of(tz), hours, w), mae(rho_of(cz), rho_of(tz), hours, w))
            col[(z, w, "O")] = (mae(pz[:, O], tz[:, O], hours, w), mae(cz[:, O], tz[:, O], hours, w))
            col[(z, w, "N2")] = (mae(pz[:, N2], tz[:, N2], hours, w), mae(cz[:, N2], tz[:, N2], hours, w))

    # (a2) forecast: block j+L/3 evaluated with the correction fitted on block j, damped towards zero with lead
    fc = {}
    for L in LEADS_H:
        sh = int(round(L / BLOCK_H))
        ok = blk >= sh
        lag = np.clip(blk - sh, 0, None)
        damp = math.exp(-L / DAMP_TAU_H)
        cl = model(d, all_idx, alt, damp * theta[lag, 0], damp * theta[lag, 1])
        for w in WIN:
            for q, ep, ec, tq in (("rho", rho_of(prior0), rho_of(cl), rho_of(tab0)),
                                  ("O", prior0[:, O], cl[:, O], tab0[:, O]),
                                  ("N2", prior0[:, N2], cl[:, N2], tab0[:, N2])):
                fc[(L, w, q)] = (mae(ep, tq, hours, w, ok), mae(ec, tq, hours, w, ok))

    # (b) gases we do not measure, at the satellite altitude, vs column truth
    sp = {}
    for w in WIN:
        for g in OTHER + ("O", "N2"):
            i = SPECIES.index(g)
            sp[(w, g)] = (mae(prior0[:, i], tab0[:, i], hours, w), mae(corr[:, i], tab0[:, i], hours, w))

    series = {"hours": hours, "fit": rows_fit, "rho": (rho_of(prior0), rho_of(corr), f["rho"], sat_truth["rho"])}
    return rows_fit, sat, col, fc, sp, series


def mean_over_runs(dicts):
    keys = dicts[0].keys()
    return {k: tuple(np.nanmean([dd[k][i] for dd in dicts]) for i in range(len(dicts[0][k]))) for k in keys}


def write(name, header, rows):
    with open(OUT / name, "w", newline="") as fh:
        wtr = csv.writer(fh)
        wtr.writerow(header)
        wtr.writerows(rows)
    print("wrote", OUT / name)


def figures(series0, col, fc, sp, sat, alt_sat):
    hrs = series0["hours"]
    fit = series0["fit"]
    tb = np.array([r["t_start_h"] for r in fit]) + BLOCK_H / 2
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    for ax, key, lab in ((axes[0], "f107", "F10.7 (sfu)"), (axes[1], "ap", "ap, current 3 h")):
        ax.plot(tb, [r[f"{key}_prior"] for r in fit], "o-", ms=3, color=C_MODEL, label="Forecast driver (prior)")
        ax.plot(tb, [r[f"{key}_truth"] for r in fit], "o-", ms=3, color=C_TRUTH, lw=0.8, label="Truth driver")
        ax.plot(tb, [r[f"{key}_fit"] for r in fit], "o-", ms=3, color=C_FIT, label="Fitted effective driver")
        ax.set_ylabel(lab)
    axes[1].set_yscale("log")
    p, c, fz, t = series0["rho"]
    for e, col_, lab in ((p, C_MODEL, "Model, forecast drivers"), (c, C_FIT, "Model, fitted drivers"),
                         (fz, C_OURS, "Fused")):
        axes[2].plot(hrs, 100 * (e / t - 1), color=col_, lw=0.7, label=lab)
    axes[2].axhline(0, color="#999", lw=0.5)
    axes[2].set_ylabel("Density error (%)")
    axes[2].set_xlabel("Hours after 2024-05-09 00:00 UT (shaded: storm)")
    for ax in axes:
        ax.axvspan(*WIN["storm"], color="#f2d7d5", alpha=0.35, lw=0)
        ax.legend(frameon=False, fontsize=8, ncol=3)
    axes[0].set_title("Fitted drivers are effective model inputs, not a retrieval of the true F10.7/ap", fontsize=9)
    fig.savefig(OUT / "fig_driver_fit.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / "fig_driver_fit.png")

    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    for ax, q, title in ((axes[0], "rho", "Density"), (axes[1], "O", "Atomic O")):
        for w, ls in (("storm", "-"), ("all", "--")):
            ax.plot([100 * col[(z, w, q)][0] for z in ALTS], ALTS, "o" + ls, color=C_MODEL, ms=4,
                    label=f"Model, forecast drivers ({w})")
            ax.plot([100 * col[(z, w, q)][1] for z in ALTS], ALTS, "o" + ls, color=C_FIT, ms=4,
                    label=f"Model, fitted drivers ({w})")
        ax.plot(100 * sat[("storm", q)][2], alt_sat, "*", color=C_OURS, ms=12, label="Fused at satellite (storm)")
        ax.set_title(f"{title}: error above/below the track")
        ax.set_xlabel("Mean abs. error (%)")
        ax.set_ylabel("Altitude (km)")
    axes[0].legend(frameon=False, fontsize=7)
    ax = axes[2]
    for q, mk in (("rho", "o"), ("O", "s")):
        ax.plot(LEADS_H, [100 * fc[(L, "all", q)][0] for L in LEADS_H], mk + "--", color=C_MODEL,
                label=f"Forecast drivers ({q})")
        ax.plot(LEADS_H, [100 * fc[(L, "all", q)][1] for L in LEADS_H], mk + "-", color=C_FIT,
                label=f"+ last fitted correction ({q})")
    ax.set_xticks(LEADS_H)
    ax.set_xlabel("Forecast lead (h)")
    ax.set_ylabel("Mean abs. error at satellite (%)")
    ax.set_title(f"Forecast skill (correction damped, {DAMP_TAU_H:g} h)")
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(OUT / "fig_model_improvement.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / "fig_model_improvement.png")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", default="base_harsh")
    args = ap.parse_args()
    case = args.case if (HL / f"{args.case}_series.pt").exists() else "harsh"
    print(f"Stage 6 driver fit on recorded runs of '{case}'", flush=True)
    ser = torch.load(HL / f"{case}_series.pt", weights_only=False)
    s = OSSE(**ser["case"])
    steps = ser["step"].long().numpy()
    hours = steps * s.dt / 3600
    OUT.mkdir(parents=True, exist_ok=True)
    runs = [one_run(s, ser, r, steps, hours) for r in range(ser["x"].shape[1])]
    fits = [row for rr in runs for row in rr[0]]
    sat, col, fc, sp = (mean_over_runs([rr[i] for rr in runs]) for i in (1, 2, 3, 4))
    tag = f"{case}, {len(runs)} recorded runs, mean over runs"

    write("driver_fit.csv", list(fits[0].keys()), [list(r.values()) for r in fits])
    write("satellite.csv", ["window", "quantity", "model_forecast", "model_fitted", "fused"],
          [[w, q, *v] for (w, q), v in sat.items()])
    write("altitude.csv", ["alt_km", "window", "quantity", "model_forecast", "model_fitted"],
          [[z, w, q, *v] for (z, w, q), v in col.items()])
    write("forecast.csv", ["lead_h", "window", "quantity", "model_forecast", "model_plus_last_fit"],
          [[L, w, q, *v] for (L, w, q), v in fc.items()])
    write("species_tested_not_claimed.csv", ["window", "species", "model_forecast", "model_fitted"],
          [[w, g, *v] for (w, g), v in sp.items()])

    print(f"\n=== {tag} (mean abs. error, %) ===")
    print("At satellite (vs run truth):            forecast-model / fitted-model / fused")
    for w in ("quiet", "storm", "recovery"):
        print(f"  {w:<9}" + "".join(f" | {q}: {100*sat[(w,q)][0]:5.1f} / {100*sat[(w,q)][1]:5.1f} / "
                                   f"{100*sat[(w,q)][2]:5.1f}" for q in ("rho", "O", "N2")))
    print("Other altitudes, storm window (density | O): forecast-model -> fitted-model")
    for z in ALTS:
        print(f"  {z} km: {100*col[(z,'storm','rho')][0]:5.1f} -> {100*col[(z,'storm','rho')][1]:5.1f}   |   "
              f"{100*col[(z,'storm','O')][0]:5.1f} -> {100*col[(z,'storm','O')][1]:5.1f}")
    print("Forecast, all windows (density | O): forecast-model -> + last fitted correction")
    for L in LEADS_H:
        print(f"  lead {L:>2} h: {100*fc[(L,'all','rho')][0]:5.1f} -> {100*fc[(L,'all','rho')][1]:5.1f}   |   "
              f"{100*fc[(L,'all','O')][0]:5.1f} -> {100*fc[(L,'all','O')][1]:5.1f}")
    print("Unmeasured gases at satellite, all windows (TESTED, NOT CLAIMED): forecast-model -> fitted-model")
    for g in OTHER:
        print(f"  {g:<3}: {100*sp[('all',g)][0]:5.1f} -> {100*sp[('all',g)][1]:5.1f}")

    figures(runs[0][5], col, fc, sp, sat, s.alt_km)


if __name__ == "__main__":
    main()
