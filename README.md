# OCC fusion OSSE: can software make cheap sensors accurate?

A small observing-system simulation experiment (OSSE) for the NASA TechLeap Orbital Clarity Challenge.

## What it does
- **Truth (nature run):** NRLMSIS 2.1 along a circular 51.6° orbit, with unmodeled structure (~5%) added. It is driven by a *synthetic* G5-like storm shaped like May 10–11, 2024. The profile uses ap up to 400, F10.7 = 220 and F10.7a = 170, and is **not** the exact historical record.
- **Prior (what operators have):** the same model with degraded inputs. The ap forecast runs 6 h late and is capped at 100, and F10.7 is off by 20 sfu. This stands in for known storm-time model error. The real May 2024 error was larger: LLITED saw NRLMSISE-00 underestimate the storm response by 58%.
- **Cheap sensors, each with unknown errors drawn fresh in every Monte Carlo run:**
  - **Ionization gauge:** gain error ±8%, gain drift, 1% noise. The filter's atomic-O sensitivity is also deliberately 5% wrong.
  - **FIPEX-type O sensor:** gain error ±12%, steady degradation of about 3% per day, 5% noise.
  - **Host GPS drag:** one orbit-averaged value per orbit, C_D bias ±7%, 3% noise.
- **Estimator:** an extended Kalman filter (EKF) with state [log-corrections to O, N2, He; gauge gain; O-sensor gain; C_D bias]. It works in log space, recovers composition and calibration jointly, and reports its own uncertainty.
- **Runs:** 40 Monte Carlo runs each at 300 km and 450 km, plus 10 runs with perfect calibration to isolate common-mode (design-level) error.

## Run
```
pip install pymsis numpy matplotlib
python fusion_osse.py     # ~3 min, writes out/results.json + series
python make_figures.py    # writes out/fig1_*.png, out/fig2_*.png
python verify.py          # ~10 min (or --quick), writes out/verify.json
```

## Verification (`verify.py`)
Checks that the code does what it claims, and shows where the headline numbers come from. Representative numbers, 300 km, `--quick`:

| Test | Result | Meaning |
|---|---|---|
| Limit: perfect sensors, filter told so | 0.7% storm error | Converges to truth; the remainder is from grouping species into 3 families |
| NIS, nominal | gauge 0.95, O 1.00, drag 0.70 | Filter's noise assumptions match the simulated sensors |
| NIS, real noise 3× assumed | 3.5 / 8.3 / 6.1 | Test catches a wrong noise model |
| NEES, nominal | 0.49 | Filter is cautious (safe direction) |
| NEES, filter told sensors are 3× better | 2.8 | Test catches overconfidence |
| Calibration error ×0.25 / ×0.5 / ×1 / ×2 | 1.8% / 2.4% / 4.5% / 8.8% | **Fused accuracy is set by assumed calibration** |
| Prior drivers: truth / 3 h late / 6 h cap 200 / 6 h cap 100 / missed | 4.1% / 8.9% / 19% / 26% / 36% | **The "26%" baseline is a setup choice** |

Composition (O-share error): with perfect sensors it is still about 3 pp (300 km) and 9 pp (450 km), the same as with nominal sensors. It drops to about 1.1 / 1.5 pp only when **all three** sensor gains are fixed (no in-flight drift allowed). Fixing any one gain does not help. A drifting gain and slowly changing composition look alike to the filter, and the nearly parallel gauge and drag sensitivities make this worse once helium matters. Open question: with perfect sensors, fixing only the O-sensor drift raises density error to about 5%. That is not yet explained.

Simulation knobs for your own experiments (all keyword args of `simulate()`, defaults reproduce the headline run): `prior`, `cal_scale`, `noise_scale`, `filter_knows_cal`, `r_filt_exact`, `filt_conf`, `cal_sigma`, `cal_drift`, `configs`.

## Headline results (storm period, median of 40 runs)
| Estimator | 300 km | 450 km |
|---|---|---|
| Empirical model alone | 25.9% | 36.0% |
| Host GPS drag alone | 14.0% | 22.2% |
| Gauge alone (naive) | 6.7% | 7.5% |
| **Fusion: gauge + O sensor + drag** | **4.6%** (P90 7.6%) | **4.6%** (P90 7.5%) |

Atomic-O share during the storm, 300 km: the prior model is off by 5.7 percentage points (pp), fusion by 3.1 pp. The O-sensor gain error drops from about 16% to about 5% in flight, so the filter learns the sensor's degradation.

## What it shows, including where it fails
1. **Fusion removes storm-time model error.** Fused error is about the same in quiet and storm periods. What remains is absolute calibration (gain and C_D priors). That is a calibration problem, which fleet cross-calibration and reference satellites can address.
2. **An ionization gauge is nearly a mass-density sensor.** Its sensitivity is roughly proportional to molecular mass for O and N2 (0.55 vs 0.57 relative to N2). So gauge + drag **cannot** retrieve composition: in the simulation it did worse than the prior, 9.6 pp. The O sensor is what breaks the degeneracy.
3. **At 450 km, composition retrieval fails in this setup.** Error is 8.4 pp versus 3.4 pp for the prior. Once helium matters, the gain drift the filter allows leaks into the N2/He split (see Verification). A channel with different helium sensitivity, drift-stable sensors, or an in-flight reference is needed there.
4. **The filter's ±2σ bands are conservative:** they contain the truth about 100% of the time. Tuning would tighten them.

## Limitations (say these in the proposal)
- The truth and prior are both NRLMSIS, so the model is identical twice. A stronger OSSE would use TIE-GCM or real CHAMP/GRACE/Swarm data as truth.
- Ram-to-ambient conversion, attitude and pointing errors, and O recombination in the chamber are folded into gain and noise terms.
- Only one host is simulated. Fleet cross-calibration is not simulated yet (see the next steps below).
- Sensor error magnitudes are assumptions. Replace them with your bench data as it comes in.

## Next steps
- Replay real data as truth (GRACE-FO/Swarm densities from TU Delft's thermosphere data site).
- Simulate a fleet of N hosts with conjunction cross-calibration: independent errors fall roughly as σ/√N, but common-mode errors do not average down.
- Port the filter to a C/embedded prototype to size onboard compute.
