"""Proposal figures from saved outputs (no simulation reruns). Run from the repo root after the Colab jobs finish:
    python scripts/figures.py
Reads out/headline/*.csv + *_series.pt, out/alt_grid/*.csv, out/phase_a3/*.csv; writes out/figures/*.png (300 dpi).
Each figure is skipped (with a message) if its inputs are missing. Baseline cases (base_*) are preferred; the
leak cases are shown as the Phase 2 enhancement."""
import csv
import glob
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import torch

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
OUT = REPO / "out" / "figures"
HL = REPO / "out" / "headline"
WINDOWS = ("quiet", "storm", "recovery")
QTY = {"rho": "Density", "O": "Atomic O", "N2": "N$_2$"}
C_MODEL, C_OURS, C_LEAK, C_BENCH = "#9aa4ad", "#0b6e8a", "#1f7a4d", "#b3261e"
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})


def load(case):
    p = HL / f"{case}.csv"
    if not p.exists():
        return None
    return {r["metric"]: (float(r["p10"]), float(r["p50"]), float(r["p90"])) for r in csv.DictReader(open(p))}


def first(*cases):
    for c in cases:
        m = load(c)
        if m:
            return c, m
    return None, None


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / name)


def fig_accuracy():
    case, m = first("base_harsh", "harsh")
    leak = load("harsh")
    if m is None:
        return print("skip accuracy: no headline csv")
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4), sharey=True)
    x = np.arange(3)
    for ax, q in zip(axes, QTY):
        mod = [100 * m[f"{w}_{q}_prior_mae"][1] for w in WINDOWS]
        ours = [100 * m[f"{w}_{q}_fused_mae"][1] for w in WINDOWS]
        p90 = [100 * m[f"{w}_{q}_fused_mae"][2] for w in WINDOWS]
        ax.bar(x - 0.27, mod, 0.26, color=C_MODEL, label="Model (NRLMSIS 2.1, forecast drivers)")
        ax.bar(x, ours, 0.26, color=C_OURS, label="Fused, baseline hardware" if case != "harsh" else "Fused")
        ax.errorbar(x, ours, yerr=[np.zeros(3), np.array(p90) - np.array(ours)], fmt="none", ecolor="#333",
                    capsize=3, lw=0.8, label="90th percentile")
        if leak is not None and case != "harsh":
            ax.bar(x + 0.27, [100 * leak[f"{w}_{q}_fused_mae"][1] for w in WINDOWS], 0.26, color=C_LEAK,
                   label="Fused + Phase 2 leak")
        if q == "rho":
            ax.axhline(20, color=C_BENCH, ls="--", lw=1, label="OCC density benchmark (20%)")
        ax.set_xticks(x, [w.capitalize() for w in WINDOWS])
        ax.set_title(QTY[q])
    axes[0].set_ylabel("Median absolute error (%)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(0.5, 1.12), fontsize=8.5)
    save(fig, "fig_accuracy.png")


def fig_ablation():
    rows = [("Host drag only", "harsh_drag_only"), ("Gauge + drag", "base_gauge_drag"),
            ("Full suite (baseline)", "base_harsh"), ("Full suite + leak", "harsh")]
    data = [(lab, load(c)) for lab, c in rows if load(c)]
    if len(data) < 2:
        return print("skip ablation: missing cases")
    colors = {"Host drag only": C_MODEL, "Gauge + drag": "#5b8fa0", "Full suite (baseline)": C_OURS,
              "Full suite + leak": C_LEAK}
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2))
    for ax, q in zip(axes, QTY):
        vals = [100 * np.mean([m[f"{w}_{q}_fused_mae"][1] for w in WINDOWS]) for _, m in data]
        model = 100 * np.mean([data[0][1][f"{w}_{q}_prior_mae"][1] for w in WINDOWS])
        ax.barh(range(len(data)), vals, color=[colors[lab] for lab, _ in data])
        ax.axvline(model, color="#333", ls=":", lw=1, label="Model")
        ax.set_yticks(range(len(data)), [lab for lab, _ in data] if q == "rho" else [""] * len(data))
        ax.set_title(QTY[q])
        ax.set_xlabel("Median abs. error, mean of windows (%)")
    axes[0].legend(frameon=False, fontsize=8)
    save(fig, "fig_ablation.png")


def fig_truths():
    cases = [("Identical twin", "base_twin"), ("NRLMSISE-00", "base_msise00"),
             ("Driver-error truth", "base_driver_error"), ("Harsh truth", "base_harsh")]
    data = [(lab, load(c)) for lab, c in cases if load(c)]
    if not data:
        return print("skip truths: no base_* cases yet")
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    x = np.arange(len(data))
    for i, w in enumerate(WINDOWS):
        ax.bar(x + (i - 1) * 0.25, [100 * m[f"{w}_rho_fused_mae"][1] for _, m in data], 0.24,
               label=w.capitalize(), color=["#7fb8c8", C_OURS, "#06414f"][i])
    ax.axhline(20, color=C_BENCH, ls="--", lw=1, label="Benchmark 20%")
    ax.set_xticks(x, [lab for lab, _ in data])
    ax.set_ylabel("Density median abs. error (%)")
    ax.legend(frameon=False, fontsize=8, ncol=4)
    save(fig, "fig_truths.png")


def _density(s, x, phase, steps):
    from osse.filter import correction
    from osse.params import value
    K, N, _ = x.shape
    b = s.basis_t[phase][:, steps].transpose(0, 1).reshape(K * N, -1) if s.harm_on else None
    d = s.dz_t[phase][:, steps].transpose(0, 1).reshape(K * N)
    e = torch.exp(correction(x.reshape(K * N, -1), b, d)[:, s.gidx]).reshape(K, N, -1)
    n_prior = s.prior[phase][:, steps].transpose(0, 1)
    rho = lambda n: (n * s.mass).sum(-1) * value("AMU")
    return rho(n_prior * e), rho(n_prior)


def fig_timeseries():
    case = "base_harsh" if (HL / "base_harsh_series.pt").exists() else "harsh"
    p = HL / f"{case}_series.pt"
    if not p.exists():
        return print("skip timeseries: no series file")
    from osse.scenario import OSSE
    ser = torch.load(p, weights_only=False)
    s = OSSE(**ser["case"])
    s._build("cpu", torch.float64)
    steps = ser["step"].long()
    hours = steps.numpy() * s.dt / 3600
    run = 0
    rho_f, rho_p = _density(s, ser["x"], ser["phase"], steps)
    fig, axes = plt.subplots(4, 1, figsize=(10, 9), sharex=True)
    panels = [(ser["rho_truth"], rho_f, rho_p, "Density (kg m$^{-3}$)"),
              (ser["O_truth"], ser["O_fused"], ser["O_prior"], "Atomic O (m$^{-3}$)"),
              (ser["N2_truth"], ser["N2_fused"], ser["N2_prior"], "N$_2$ (m$^{-3}$)")]
    nwin = max(1, int(round(s.nper / max(1, int(steps[1] - steps[0])))))  # recorded points per orbit
    sm = lambda y: np.exp(np.convolve(np.log(y), np.ones(nwin) / nwin, mode="same"))  # orbit running mean
    for ax, (tru, fus, pri, lab) in zip(axes, panels):
        ax.plot(hours, sm(pri[:, run].numpy()), color=C_MODEL, lw=0.9, label="Model (forecast-driven)")
        ax.plot(hours, sm(tru[:, run].numpy()), color="#222", lw=0.8, label="Truth")
        ax.plot(hours, sm(fus[:, run].numpy()), color=C_OURS, lw=1.0, label="Fused")
        ax.set_yscale("log")
        ax.set_ylabel(lab)
    for ax in axes:
        ax.axvspan(39, 78, color="#f2d7d5", alpha=0.35, lw=0)
    ax = axes[3]
    ax.plot(hours, 100 * (ser["gauge_gain_est"][:, run] - ser["gauge_gain_true"][:, run]).numpy(), color=C_OURS,
            lw=0.8, label="Gauge gain error")
    ax.plot(hours, 100 * (ser["o_gain_est"][:, run] - ser["o_gain_true"][:, run]).numpy(), color="#c77b00",
            lw=0.8, label="FIPEX gain error")
    ax.axhline(0, color="#999", lw=0.5)
    ax.set_ylabel("In-flight gain error (%)")
    ax.set_xlabel("Hours after 2024-05-09 00:00 UT (shaded: storm)")
    axes[0].legend(frameon=False, ncol=3, fontsize=8)
    ax.legend(frameon=False, ncol=2, fontsize=8)
    save(fig, "fig_timeseries.png")


def fig_altitude():
    d = REPO / "out" / ("alt_grid_noleak" if (REPO / "out" / "alt_grid_noleak").exists() else "alt_grid")
    print("altitude figure from", d.name)
    files = sorted(glob.glob(str(d / "*km.csv")), key=lambda f: int(Path(f).stem[:-2]))
    if not files:
        return print("skip altitude: no alt_grid csv")
    alts = [int(Path(f).stem[:-2]) for f in files]
    ms = [{r["metric"]: float(r["p50"]) for r in csv.DictReader(open(f))} for f in files]
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)
    for ax, q in zip(axes, QTY):
        ax.plot([100 * m[f"storm_{q}_prior_mae"] for m in ms], alts, "o--", color=C_MODEL, label="Model")
        ax.plot([100 * m[f"storm_{q}_fused_mae"] for m in ms], alts, "o-", color=C_OURS, label="Fused")
        if q == "rho":
            ax.axvline(20, color=C_BENCH, ls="--", lw=1, label="Benchmark 20%")
        ax.set_title(QTY[q] + " (storm window)")
        ax.set_xlabel("Median abs. error (%)")
    axes[0].set_ylabel("Altitude (km)")
    axes[0].legend(frameon=False, fontsize=8)
    save(fig, "fig_altitude.png")


def fig_requirements():
    d = REPO / "out" / ("phase_a_noleak" if (REPO / "out" / "phase_a_noleak").exists() else "phase_a3")
    print("requirements figure from", d.name)
    rows = [r for f in sorted(glob.glob(str(d / "A*.csv"))) for r in csv.DictReader(open(f))]
    key = "storm_rho_fused_mae_p50"
    rows = [r for r in rows if r.get(key) not in ("", None)]
    if not rows:
        return print("skip requirements: no phase_a csv")
    ignore = ("TRUTH_KIND", "TRUTH_MSIS_VERSION", "USE_SENSORS")
    cfgs = [{k: r[k] for k in r if k.isupper() and k not in ignore and r[k] not in ("", None)} for r in rows]
    base = next((r for r, c in zip(rows, cfgs) if not c), rows[0])
    b = float(base[key])
    items = [(", ".join(f"{k}={v}" for k, v in c.items())[:48], 100 * (float(r[key]) - b))
             for r, c in zip(rows, cfgs) if c]
    items.sort(key=lambda t: abs(t[1]))
    fig, ax = plt.subplots(figsize=(8, 0.28 * len(items) + 1))
    ax.barh(range(len(items)), [v for _, v in items], color=[C_BENCH if v > 0 else C_OURS for _, v in items])
    ax.set_yticks(range(len(items)), [lab for lab, _ in items], fontsize=7)
    ax.axvline(0, color="#333", lw=0.6)
    ax.set_xlabel(f"Change in storm density error vs baseline ({100 * b:.1f}%), percentage points")
    save(fig, "fig_requirements.png")


if __name__ == "__main__":
    for f in (fig_accuracy, fig_ablation, fig_truths, fig_timeseries, fig_altitude, fig_requirements):
        try:
            f()
        except Exception as exc:  # one broken figure must not stop the others
            print(f"FAILED {f.__name__}: {exc!r}")
