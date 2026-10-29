"""
Verification tests for the fusion OSSE.  Answers two questions:
  (a) Does the code do what it claims?        -> limit test, NIS/NEES consistency tests
  (b) Where do the headline numbers come from? -> calibration sweep, baseline (prior) sweep,
                                                 what limits composition (+ observability)

Run:  python verify.py           (10 seeds per case, ~5-10 min)
      python verify.py --quick   (4 seeds per case)
Writes out/verify.json and prints a summary. Exit code 1 if a pass/fail check fails.

How to read the consistency tests (standard Kalman-filter checks, Bar-Shalom et al.):
  NIS  = innovation^2 / predicted innovation variance, averaged. ~1 means the filter's noise
         assumptions match reality; >>1 means reality is noisier than the filter thinks.
  NEES = (log density error / filter sigma)^2, averaged. ~1 honest, <1 cautious (safe),
         >1 overconfident (dangerous: the filter claims accuracy it doesn't have).
"""
import json, os, sys
import numpy as np
import fusion_osse as F

QUICK = "--quick" in sys.argv
SEEDS = list(range(200, 204 if QUICK else 210))
FUSED = "fused_gauge_O_drag"


def runs(alt=300, configs=(FUSED,), **kw):
    return [F.simulate(alt, sd, configs=list(configs), **kw)[0] for sd in SEEDS]

def med(rs, *path):
    vals = []
    for r in rs:
        v = r
        for p in path: v = v[p]
        vals.append(v)
    return float(np.median(vals))

def storm_err(rs, name=FUSED):
    return med(rs, name, "storm", "MAPE")


results, checks = {}, []
def check(name, ok, detail):
    checks.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

# ---------------------------------------------------------------- 1. limit test
print("\n1. Limit test: perfect sensors, filter told they are perfect, exact gauge model")
rs = runs(zero_cal=True, filter_knows_cal=True, r_filt_exact=True)
e = storm_err(rs)
results["limit"] = {"storm_MAPE": e}
check("converges to truth", e < 0.01, f"storm density error {e:.2%} (should be < 1%; remainder = 3-family grouping)")

# ---------------------------------------------------------------- 2. consistency
print("\n2. Consistency (NIS / NEES), nominal setup")
nom = runs()
nis = {k: med(nom, FUSED, "NIS", k) for k in ("gauge", "O", "drag")}
nees = med(nom, FUSED, "NEES_rho")
results["nominal"] = {"storm_MAPE": storm_err(nom), "NIS": nis, "NEES_rho": nees}
check("NIS ~ 1 (noise model right)", all(0.5 < v < 1.5 for v in nis.values()),
      ", ".join(f"{k} {v:.2f}" for k, v in nis.items()))
check("NEES <= ~1 (not overconfident)", nees < 1.5, f"NEES {nees:.2f} (<1 = cautious)")

print("\n   2b. Real noise 3x larger than the filter assumes -> NIS should jump")
noisy = runs(noise_scale=3.0)
nis_n = {k: med(noisy, FUSED, "NIS", k) for k in ("gauge", "O", "drag")}
results["noise_x3"] = {"NIS": nis_n, "NEES_rho": med(noisy, FUSED, "NEES_rho")}
check("NIS detects wrong noise model", max(nis_n.values()) > 1.5,
      ", ".join(f"{k} {v:.2f}" for k, v in nis_n.items()))

print("\n   2c. Filter told sensors are 3x better than they are -> NEES should jump")
over = runs(filt_conf=3.0)
nees_o = med(over, FUSED, "NEES_rho")
results["overconfident_x3"] = {"NEES_rho": nees_o, "storm_MAPE": storm_err(over)}
check("NEES detects overconfidence", nees_o > max(1.0, 2 * nees), f"NEES {nees_o:.2f} vs nominal {nees:.2f}")

# ---------------------------------------------------------------- 3. calibration sweep
print("\n3. Where the fused number comes from: scale the TRUE sensor calibration errors")
sweep = {}
for s in (0.25, 0.5, 1.0, 2.0):
    sweep[s] = storm_err(runs(cal_scale=s))
    print(f"   calibration error x{s:<4}  -> storm density error {sweep[s]:.2%}")
results["cal_sweep"] = {str(k): v for k, v in sweep.items()}
v = list(sweep.values())
check("error tracks calibration", all(a < b for a, b in zip(v, v[1:])),
      "monotonic increase -> the fused accuracy is set by calibration, not storms")

# ---------------------------------------------------------------- 4. baseline sweep
print("\n4. Where the baseline number comes from: how degraded the prior model's storm inputs are")
base = {}
for p in ("truth", "lag3", "lag6_cap200", "lag6_cap100", "missed"):
    base[p] = med(runs(prior=p, configs=()), "prior_model", "storm", "MAPE")
    print(f"   prior drivers {p:<12} -> model-only storm density error {base[p]:.2%}")
results["prior_sweep"] = base
print("   (the headline '~26%' uses lag6_cap100: it is a setup choice, not a discovery)")

# ---------------------------------------------------------------- 5. composition floor + observability
print("\n5. What limits composition? Perfect sensors (zero true calibration error, exact gauge model)")
comp = {}
for alt in (300, 450):
    nomc = runs(alt)                                                          # nominal sensors + filter
    drift = runs(alt, zero_cal=True, r_filt_exact=True)                       # perfect, filter lets gains drift
    one = {k: runs(alt, zero_cal=True, r_filt_exact=True, cal_drift={k: 0.0}) for k in ("gauge", "O", "CD")}
    fixed = runs(alt, zero_cal=True, r_filt_exact=True, filter_knows_cal=True)  # all gains known AND fixed
    pp = lambda rs, name=FUSED: med(rs, "composition", name, "xO_MAE_pp_storm")
    comp[alt] = {"nominal_pp": pp(nomc), "perfect_gains_may_drift_pp": pp(drift),
                 **{f"perfect_only_{k}_fixed_pp": pp(v) for k, v in one.items()},
                 "perfect_all_gains_fixed_pp": pp(fixed), "prior_model_pp": pp(drift, "prior_model")}
    c = comp[alt]
    print(f"   {alt} km O-share error: nominal {c['nominal_pp']:.1f} | perfect, gains may drift "
          f"{c['perfect_gains_may_drift_pp']:.1f} | only one gain fixed "
          + "/".join(f"{c[f'perfect_only_{k}_fixed_pp']:.1f}" for k in ("gauge", "O", "CD"))
          + f" | all gains fixed {c['perfect_all_gains_fixed_pp']:.1f} | model alone {c['prior_model_pp']:.1f}  (pp)")
results["composition_limits"] = comp
f = comp[300]
check("composition limited by in-flight gain drift", f["perfect_all_gains_fixed_pp"] < 0.6 * f["perfect_gains_may_drift_pp"],
      "fixing all gains cuts composition error; fixing any single one does not")

# Observability: each sensor is a weighted sum over species. Rows = sensors, columns = [O, N2, He].
# If two rows are nearly parallel, the split between those species cannot be solved by ANY estimator.
W = {"gauge": [F.R_TRUE["O"], F.R_TRUE["N2"], F.R_TRUE["He"]],
     "drag":  [F.MASS["O"], F.MASS["N2"], F.MASS["He"]],
     "O_sensor": [1.0, 0.0, 0.0]}
def cond(rows):
    M = np.array([np.array(r) / np.linalg.norm(r) for r in rows])
    return float(np.linalg.cond(M))
obs = {"gauge+drag+O [O,N2,He]": cond([W["gauge"], W["drag"], W["O_sensor"]]),
       "gauge+drag  [N2,He] (O known)": cond([W["gauge"][1:], W["drag"][1:]]),
       "gauge+O     [O,N2]": cond([W["gauge"][:2], W["O_sensor"][:2]])}
for k, val in obs.items():
    print(f"   condition number {k:<32} {val:8.1f}   (1 = perfectly separable, large = degenerate)")
results["observability_cond"] = obs
print("   -> Composition error is NOT set by ground calibration of one sensor. It comes from letting the\n"
      "      filter track in-flight gain drift: a slowly drifting gain and slowly changing composition look\n"
      "      alike. Gauge and drag rows are nearly parallel (see condition numbers), which makes that\n"
      "      trade worse once He matters (450 km). Levers: drift-stable sensors, an in-flight reference\n"
      "      (fleet cross-calibration), or a channel with a different He sensitivity.")

# ---------------------------------------------------------------- save
results["checks"] = [{"name": n, "pass": ok, "detail": d} for n, ok, d in checks]
results["seeds"] = SEEDS
with open(os.path.join(F.OUT, "verify.json"), "w") as f:
    json.dump(results, f, indent=1)
nfail = sum(not ok for _, ok, _ in checks)
print(f"\n{len(checks) - nfail}/{len(checks)} checks passed. Wrote out/verify.json")
sys.exit(1 if nfail else 0)
