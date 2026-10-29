"""Figures for the fusion OSSE (reads ./out/results.json and series_*.npz)."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "out")
SURF, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e6e5e1"
BLUE, ORANGE, AQUA, GRAY, BLUE_LT = "#2a78d6", "#eb6834", "#1baf7a", "#8a8984", "#b7d3f6"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.facecolor": SURF, "figure.facecolor": SURF,
                     "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8, "axes.spines.top": False,
                     "axes.spines.right": False, "legend.frameon": False})

s = np.load(os.path.join(OUT, "series_300km.npz"))
h = s["hrs"]
fig, ax = plt.subplots(3, 1, figsize=(10, 8.2), sharex=True, gridspec_kw={"height_ratios": [1, 2.6, 1.7]})
# (a) driver
ax[0].step(h, s["ap"], where="post", color=INK, lw=1.6, label="True ap (nature run)")
ax[0].step(h, s["ap_p"], where="post", color=GRAY, lw=1.6, label="ap the model was given (late, capped)")
ax[0].set_ylabel("3-h ap"); ax[0].legend(loc="upper left", fontsize=8)
ax[0].set_title("A. Storm driver (synthetic G5-like profile)", loc="left", color=INK, fontsize=10, fontweight="bold")
# (b) density error
err = lambda e: (e / s["rho_t"] - 1) * 100
band = 2 * s["sig"] * 100
ax[1].fill_between(h, err(s["rho_f"]) - band, err(s["rho_f"]) + band, color=BLUE, alpha=0.10, lw=0, label="Fused ±2σ (filter's own uncertainty)")
for y in (20, -20):
    ax[1].axhline(y, color=INK2, lw=0.8)
ax[1].text(1, 21, "OCC 20% accuracy target", ha="left", va="bottom", color=INK2, fontsize=8)
ax[1].plot(h, err(s["rho_drag"]), color=AQUA, lw=0.9, alpha=0.8, label="Host GPS drag alone (1 value per orbit)")
ax[1].plot(h, err(s["rho_p"]), color=GRAY, lw=1.4, label="Empirical model alone (what operators use)")
ax[1].plot(h, err(s["rho_gauge"]), color=ORANGE, lw=1.4, label="Gauge alone, naive conversion")
ax[1].plot(h, err(s["rho_f"]), color=BLUE, lw=2.0, label="Software fusion (gauge + O sensor + drag)")
ax[1].set_ylabel("Density error vs truth (%)"); ax[1].set_ylim(-75, 60)
ax[1].legend(loc="lower left", fontsize=8, ncol=2)
ax[1].set_title("B. Mass-density error along a 300 km orbit", loc="left", color=INK, fontsize=10, fontweight="bold")
# (c) composition
ax[2].plot(h, s["xO_t"] * 100, color=INK, lw=1.4, label="Truth")
ax[2].plot(h, s["xO_p"] * 100, color=GRAY, lw=1.4, label="Empirical model")
ax[2].plot(h, s["xO_f"] * 100, color=BLUE, lw=2.0, label="Software fusion")
ax[2].set_ylabel("Atomic-O share of gas (%)"); ax[2].legend(loc="lower left", fontsize=8, ncol=3)
ax[2].set_title("C. Composition retrieved without a mass spectrometer", loc="left", color=INK, fontsize=10, fontweight="bold")
ax[2].set_xlabel("Hours from 2024-05-09 00:00 UT (storm onset ≈ hour 39)")
ax[2].set_xlim(0, 96); ax[2].set_xticks(range(0, 97, 12))
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig1_timeseries_300km.png"), dpi=170)

# ---- Monte Carlo summary
R = json.load(open(os.path.join(OUT, "results.json")))
EST = [("prior_model", "Empirical model alone"), ("drag_only", "GPS drag alone"), ("gauge_only", "Gauge alone (naive)"),
       ("fused_gauge_drag", "Fusion: gauge + drag"), ("fused_O_drag", "Fusion: O sensor + drag"),
       ("fused_gauge_O", "Fusion: gauge + O sensor"), ("fused_gauge_O_drag", "Fusion: all three")]
COMP = [("prior_model", "Empirical model alone"), ("fused_gauge_drag", "Fusion: gauge + drag"),
        ("fused_O_drag", "Fusion: O sensor + drag"), ("fused_gauge_O", "Fusion: gauge + O sensor"),
        ("fused_gauge_O_drag", "Fusion: all three")]
fig, ax = plt.subplots(2, 2, figsize=(10, 7.4), gridspec_kw={"height_ratios": [7, 5]})
for j, alt in enumerate(("300", "450")):
    mc = R[alt]["monte_carlo"]
    for i, (items, getter, xl, ttl) in enumerate([
        (EST, lambda r, k: r[k]["storm"]["MAPE"] * 100, "Storm-time density error, median over 40 runs (%)", "density"),
        (COMP, lambda r, k: r["composition"][k]["xO_MAE_pp_storm"], "Storm-time error in atomic-O share (percentage points)", "composition")]):
        a = ax[i, j]
        ys = np.arange(len(items))[::-1]
        for y, (k, lab) in zip(ys, items):
            v = np.array([getter(r, k) for r in mc])
            med, lo, hi = np.median(v), np.percentile(v, 10), np.percentile(v, 90)
            col = BLUE if k.startswith("fused") else GRAY
            a.barh(y, med, height=0.55, color=col, alpha=1.0 if k == "fused_gauge_O_drag" else (0.55 if k.startswith("fused") else 1.0))
            a.plot([lo, hi], [y, y], color=INK, lw=1.0)
            a.text(hi + (0.6 if i == 0 else 0.2), y, f"{med:.1f}", va="center", fontsize=8, color=INK)
        a.set_yticks(ys); a.set_yticklabels([l for _, l in items] if j == 0 else [])
        a.set_xlabel(xl, fontsize=8); a.grid(axis="y", visible=False)
        if i == 0:
            a.axvline(20, color=INK2, lw=0.8); a.text(20.3, ys[0] + 0.45, "OCC 20%", fontsize=8, color=INK2)
            a.set_title(f"{alt} km", loc="left", fontweight="bold", color=INK, fontsize=10)
        a.set_xlim(0, 45 if i == 0 else 13)
fig.suptitle("40 Monte Carlo runs per altitude: new sensor gains, drift, C_D bias, noise and orbit phase each run\n(bar = median, line = 10th-90th percentile)",
             x=0.01, ha="left", fontsize=9, color=INK2)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(os.path.join(OUT, "fig2_monte_carlo_summary.png"), dpi=170)
print("figures written")
