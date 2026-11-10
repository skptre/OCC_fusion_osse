# Overnight research + experiments (Nov 9, 2026)

Rough notes. Sources: 3 research agents (estimation and self-calibration; failure modes; cross-domain and scoring), plus my own experiments on your pushed code (scratch copy; repo untouched).

**Tags:**
- **[TESTED]** = I ran it tonight. Numbers are 200 runs, 300 km, 51.6°, May 2024, same seed unless noted.
- **[LIT]** = from the literature, with a citation.
- **[DERIVED]** = physics I checked by hand.
- **UNCONFIRMED** = the agents couldn't verify it against a primary source. Check before citing.

---

## 0. TL;DR (ranked by impact on our score)

0. **[TESTED, round 2] S_O, our biggest unknown, can be MEASURED IN FLIGHT.** A likelihood bank of 7 filters recovered a true S_O of 0.70 as 0.709 (P10–P90 0.66–0.77) from one unit in 5 days. A wrong S_O costs 10–21% in N₂ and NEES 100. See §1e. Round 2 also showed the overconfidence is model mismatch, not linearization, and ranks 15 filter changes.
1. **[TESTED] Composition is limited by sensor calibration and drift, not by the filter or the physics.** With perfect, non-drifting sensors, O comes out within ±0.3% and N₂ within ±1–2%, storm included. All the composition error comes from gain uncertainty and drift.
   - So the proposal's composition claim rests on: (a) a vendor drift spec, (b) relative CCG-vs-FIPEX calibration (ground plus in-flight), (c) the fleet cross-calibration story.
2. **[TESTED] The Gauss-Markov filter structure is worth adopting** (prototype ready).
   - It halves the run-to-run spread with imperfect sensors.
   - It learns the gains to about 4–5% in quiet times.
   - Cost: NEES of about 3 (overconfident), not yet fixed; see #6.
3. **[LIT] The WADIS-2 FIPEX calibration was +35% / −28% per sensor** (Eberhart 2019), much worse than our 12% placeholder.
   - Stuttgart's "reworked absolute calibration" is therefore make-or-break for composition. **Ask for its uncertainty first today.**
4. **[TESTED] Drift spec matters most for storm N₂.**
   - Gauge drift 2%/day → 0.1%/day takes storm N₂ MAE from 11% to 5.4% (current filter, no FIPEX drift).
   - Quiet N₂ stays at about 8% regardless. Quiet is limited by absolute calibration (gauge 30%, FIPEX 12%), not by drift.
5. **[LIT] A cold cathode gauge in a ram chamber reads ambient flux, so its gas weights are S_i·√m_i, not S_i.** We must model this; the real gauge works this way.
   - [TESTED] It barely changes our results (same N₂ errors within ~1 pp), so the conclusions hold. It's a model-correctness fix for Phase B.
   - The chamber wall temperature T_c (√T scaling) and the angle of attack (cos θ) also belong in the gauge model.
6. **[TESTED] NEES (honest uncertainty) is the main open software problem.**
   - What I ruled out: drag (NEES 3.5 without drag), per-gas wiggles, boundary-timed Q (made it worse).
   - Prime remaining suspects [LIT]:
     - (a) "spurious observability" from EKF linearisation. Fix: first-estimates or observability-constrained Jacobians (Huang, Mourikis & Roumeliotis 2009/10).
     - (b) the deterministic forecast-error trend modelled as a random walk.
     - (c) consider (Schmidt) parameters for S_O and the gas factors.
   - This matters for Performance ("realistic uncertainty").
7. **[TESTED] A ground RTS smoother cuts errors about 10–25% for free.** Storm density rms 5.7% → 4.4%; storm O 11.7% → 9.0%; quiet N₂ 8.1% → 6.3% (30 runs, default drift).
   - Our product is ground-processed, so this is legitimate. Onboard EKF for real time, ground smoother for the archive product.
8. **[LIT] The biggest real-world risk not in our simulation yet is an outgassing background in the gauge.** It's additive, decays only as about t^−0.5 for months to years (Rosetta, Schläppi 2010), and can be ~10% at night and 450 km.
   - Needs a background state in the filter (additive, separable from the multiplicative gain through day/night variation) plus operational burn-in.
9. **[LIT] The relevance demo: show our data improves model forecasts** (HASDM, EXTEMPLAR, MSIS-UQ style).
   - In the OSSE, estimate effective drivers (ap/F10.7 or exospheric temperature) from our measurements, forecast forward, and score against the NOAA-forecast baseline at 0/6/24/48 h leads.
   - That's the "specific, well-evidenced case for how the data would improve model accuracy" the rubric asks for.
10. **[LIT] Fleet "ubercal" (SDSS-style self-calibration).** Units crossing near the same place and time compare readings, giving per-unit relative gains by one global least-squares solve; drag and reference missions (Swarm, GRACE-FO) fix the single common scale.
    - Calibration then *improves* as the fleet grows, a strong scalability narrative.
11. **[TESTED, with a warning] Physics-constrained states** (estimate driver or exospheric-temperature corrections instead of free per-gas corrections) look extremely good in our OSSE: two MSIS driver directions explain 99.5% of the model gap.
    - **But that's an identical-twin artifact.** Our truth *is* MSIS with different drivers, so the gap is driver-shaped by construction.
    - Real data needs exospheric temperature plus a δO term (Weimer 2016). Only test this after the different-model truth (C2) exists, or the result is self-fulfilling.
12. **[LIT] Hosting risk outside software: the MAG084's NdFeB magnet.** Roughly 2000 nT at 1 m and about 3e-4 N·m torque (derived and assumed, UNCONFIRMED magnitude). Could be a deal-breaker for hosts with magnetometers or magnetorquers. Flag to the mech team: measure the dipole, consider compensation.

---

## 1. Experiments run tonight (scratch prototype on your pushed code)

Baseline is your current filter, defaults, no FIPEX drift unless stated.

| Test | Result | Verdict |
|---|---|---|
| Perfect, non-drifting sensors (current filter) | quiet O +0.1%, N₂ −0.4%; storm O −0.1%, N₂ +0.7%; NEES 0.9 | **Good**: filter and information content are sound |
| Same, Gauss-Markov filter | storm N₂ +1.9%; NEES 1.8 | GM slightly worse with perfect sensors |
| GM vs current, default sensors | quiet density P10–P90 −11…+7% → −8…−0.5%; storm N₂ −4…+20% → −1…+13%; gains learned to ~4–5% in quiet (current ~8%, flat) | **Adopt GM** |
| GM + storm-time Q (oracle, smoothed) | storm N₂ +8.6% → +7.3%; NEES 3.4 → 2.8 | small help; not worth it as is |
| GM + Q injected at 3-h ap boundaries | N₂ MAE −5%; NEES worse (4.4) | **drop** |
| Prior/model-gap jumps | 64% of N₂ gap-change variance happens at 39 of 14,399 steps (the 3-h ap block boundaries); truth also jumps | **Realism fix:** truth should use interpolated (smooth) drivers (`get_f107_ap(..., interpolate=True)`); the operator prior can stay stepwise |
| Ram-chamber √m gauge weights | results within ~1 pp of before (both filters) | model it for correctness; conclusions unchanged |
| Real geodetic altitude (oblateness ±13 km) + eccentricity 0.001 | quiet N₂ MAE 6.0% → 5.3% (GM); else unchanged | small; free extra realism, keep |
| GM without drag | NEES 3.5 (unchanged) | drag is not the NEES cause |
| GM gauge drift 0.1%/day | storm N₂ MAE 10.3% → 5.7%; NEES 4.8 | drift spec drives storm composition |
| RTS smoother (GM, 30 runs, default drift) | density storm rms 5.7% → 4.4%; O storm 11.7% → 9.0%; N₂ quiet 8.1% → 6.3% | **Good**: use on ground |
| Drift sweep (current filter, 9 combos) | see §1b | requirement curves for Phase A |

### 1b. Drift sweep, current filter (median MAE / P90)

| Gauge drift/day | FIPEX drift/day | quiet ρ | storm ρ | quiet N₂ | storm N₂ |
|---|---|---|---|---|---|
| 0.02 | 0.03 | 5.1 / 12.1 | 4.8 / 12.6 | 8.9 / 16.2 | 9.5 / 19.6 |
| 0.02 | 0 | 5.1 / 12.2 | 5.3 / 13.1 | 9.8 / 17.7 | 11.0 / 20.5 |
| 0.005 | 0.01 | 5.0 / 11.8 | 4.4 / 11.5 | 8.1 / 15.5 | 7.3 / 15.2 |
| 0.001 | 0 | 5.0 / 11.7 | 4.5 / 10.8 | 8.8 / 16.5 | 5.4 / 11.1 |

**Read:**
- Density stays ≈5% median / ≈12% P90 whatever the drift, inside OCC's 20%. It's limited by absolute calibration.
- Storm N₂ halves with good drift.
- Quiet N₂ doesn't improve, because it's set by absolute calibration plus the prior bias.
- Raw data: `scratchpad/proto/exp_drift.json`.

### 1c. Drift sweep, Gauss-Markov filter (median MAE / P90, %), plus NEES

| Gauge drift/day | FIPEX drift/day | quiet ρ | storm ρ | quiet N₂ | storm N₂ | NEES |
|---|---|---|---|---|---|---|
| 0.02 | 0.03 | 4.3 / 7.9 | 4.2 / 9.4 | 5.8 / 11.6 | 8.7 / 13.6 | 3.0 |
| 0.02 | 0.01 | 4.3 / 7.7 | 2.8 / 5.6 | 6.0 / 11.8 | 10.1 / 14.8 | 3.4 |
| 0.02 | 0.0 | 4.0 / 7.4 | 3.0 / 5.9 | 6.1 / 11.9 | 11.8 / 16.4 | 3.3 |
| 0.005 | 0.03 | 3.8 / 6.5 | 4.0 / 7.6 | 5.0 / 9.6 | 7.8 / 10.8 | 3.2 |
| 0.005 | 0.01 | 3.8 / 6.5 | 3.6 / 6.9 | 4.9 / 9.4 | 6.6 / 9.9 | 4.7 |
| 0.005 | 0.0 | 3.8 / 6.5 | 2.4 / 5.4 | 5.5 / 10.1 | 5.8 / 9.0 | 4.5 |
| 0.001 | 0.03 | 3.9 / 6.3 | 4.2 / 7.0 | 4.8 / 9.4 | 7.7 / 10.1 | 3.2 |
| 0.001 | 0.01 | 3.8 / 6.3 | 4.3 / 7.1 | 4.8 / 9.1 | 5.9 / 8.3 | 4.9 |
| 0.001 | 0.0 | 3.9 / 6.3 | 4.7 / 7.4 | 5.6 / 9.8 | **3.9 / 5.3** | 4.4 |

**GM vs current, same drift:** P90 density error drops from ~11–13% to ~6–9%; P90 N₂ from ~15–20% to ~9–14%. With good drift (0.1%/day gauge, no FIPEX drift), storm N₂ reaches **3.9% median / 5.3% P90**. GM is clearly better everywhere except NEES (3–5), which still needs the fix in §4.2 before the error bars can be called "realistic".

---

### 1d. Where the GM filter's overconfidence comes from (per-state NEES, z = error/σ)

| State group | default sensors | perfect sensors |
|---|---|---|
| wiggles (common, O, N₂, He) | z² ≈ 1.0–1.6 ✔ | ≈ 1.0–1.2 ✔ |
| model gap O / N₂ / He | z² 2.7 / 2.3 / 3.6; gap O z = −1.4 | 1.8 / 1.7 / 0.9 |
| FIPEX gain | z² 3.0, z = +1.6 (mirror of gap O) | (tiny-P artifact) |
| gauge gain / C_D | 1.0 / 0.8 | — |

**Read:** the wiggle model is right. The overconfidence lives in the **split between "O model gap" and "FIPEX gain"**. FIPEX only measures their sum, so the split is weakly observable, and the one-sided FIPEX drift pushes along it.

**Tried two fixes:**
- **O-gain drift-rate state (zero-mean prior):** no improvement; NEES 3.0 → 4.1. The drift is indistinguishable from a slow trend in O.
- **Drift-rate state with the mean degradation known from characterisation (3 ± 1 %/day):** storm O bias −9.3% → −5.9%, storm density MAE 4.2% → 2.8%; but storm N₂ MAE got worse (8.7% → 10.3%) and NEES stayed ≈3.3.
- **Conclusion:** one-sided FIPEX drift is fundamentally weakly observable in flight. The real fixes are (1) a low-drift sensor spec or characterisation from Stuttgart, (2) the fleet ubercal (other units' FIPEX gains constrain the drift), (3) consider-parameter handling so NEES reflects it honestly. **Drift is THE FIPEX number to get today.**

---

---

## 1e. ROUND 2: filter-only research (3 more agents) + tests

### Big result [TESTED]: S_O is measurable IN FLIGHT by likelihood (multiple-model bank)

- **Setup:** the truth's S_O is 0.70, unknown to the filters. Run 7 GM filters with S_O = 0.45, 0.50, 0.56, 0.63, 0.70, 0.77, 0.85 on the same data, and score each by its innovation negative log-likelihood (how well it predicts the sensors). 100 runs, no FIPEX drift, all other gains unknown as usual.
- **Result:** the likelihood-weighted S_O estimate is **median 0.709, P10–P90 0.658–0.767** (true 0.70) from **one unit over 5 days**. The best-fit grid point was 0.70 in 53% of runs, and 0.63 or 0.77 in the rest.
- **Why it matters:** S_O is the biggest unknown (never measured). This is a defensible in-flight measurement of it: Multiple-Model Adaptive Estimation (Magill 1965, IEEE TAC 10:434) = a profile likelihood (Raue et al. 2009, Bioinformatics 25:1923).
  - A fleet of N units pools the estimate, roughly √N tighter.
  - Onboard cost: 7 filters ≈ 10⁵ FLOP per 30 s, trivial for an M7. Or run it on the ground.
- **What a wrong S_O costs** (filter 0.56 vs truth 0.70): quiet N₂ MAE 21%, storm 10%, NEES 100. With the right S_O: 6% / 10%, NEES 2.8. This is the quantified case for estimating S_O instead of assuming it.
- **Caveats:** tested without FIPEX drift; needs re-testing with drift, and over longer time.
- **Alternative:** gradient/ML learning of S_O with the other hyperparameters through the PyTorch filter (Schweppe 1965 prediction-error likelihood; Kloss et al. 2021 Auton. Robots 45:561). Same principle, continuous instead of a grid.

### Diagnostic [TESTED]: the overconfidence is model mismatch, not linearization

- Evaluating the gauge slopes at the **truth** made NEES worse (3.4 → 4.1).
- So "spurious observability" fixes (first-estimates Jacobians, observability-constrained EKF) **won't help**. The fix must be structural: consider parameters, or a drift/gap model that matches reality.
- **Key insight (agent, derived):** NIS can never reveal overconfidence in a direction the sensors can't see (gap_O vs b_o). Only structure makes that honest.

### The fundamental limit (agents, derived, consistent with our tests)

- 3 sensors, 3 unknown absolute offsets (gauge gain, FIPEX gain, C_D), and no sensor with a known reference. This is the classic **sensor registration rank deficiency** (Okello & Ristic 2003 IEEE TAES 39:1074; Lin, Bar-Shalom & Kirubarajan 2004 IEEE TAES 40:576).
- The data fix only **relative** gains and composition. The absolute level must come from a prior or a reference.
- **Proposal wording:** "relative composition from the sensors; absolute level anchored by drag with a physics-modelled C_D and by ground calibration."
- **Fisher information** for a known-shape signal with an unknown gain: only the **centered variation** of each state's sensitivity along the orbit helps (I = N·Var(h)/σ²). Computing Var(h) per orbit predicts separability before any run. Cheap diagnostic to add.

### Ranked filter changes (all three agents combined, with my test verdicts)

1. **[TESTED ✔] Estimate S_O in flight** (MMAE bank or ML learning). See above.
2. **[TESTED ✔] Gauss-Markov states.**
3. **[TESTED ✔] Ground RTS smoother** (10–25%). The agents add: the iterated smoother = batch Gauss-Newton MAP (Bell 1994 SIAM J. Optim. 4:626), so a full-batch factor-graph MAP is the "archive" product with consistent marginals. Smoothing improves random-walk gap combinations σ by ~29% (Durbin & Koopman).
4. **Consider (Schmidt-Kalman) parameters** for the FIPEX degradation rate, and S_O if not estimated. Recursive form: Zanetti & D'Souza 2015 J. Astronaut. Sci. 60:672. Purpose: honest NEES, not accuracy. My drift-rate test confirms the accuracy doesn't improve and the honesty must come from consider handling. **Next to test.**
5. **Mean-reverting (OU) model gap with activity-dependent σ** instead of a random walk. The agents say this is the only route to better absolute b_o/b_g/N₂ without new data, because quiet periods act as references. Needs a cited MSIS error climatology (Bruinsma & Laurens 2024 gives storm σ) and honest testing. **Test after the fraternal truth.**
6. **Exact daily drag:** accumulator state (onboard) or the exact factor (ground), plus the **Jensen correction** log E[e^w] = σ²/2 ≈ 0.7% for 12% wiggles (a systematic 0.7% bias, derived).
7. **ML hyperparameter learning ground pipeline:** EKF → RTS smoother → EM warm start (Shumway & Stoffer 1982) → full maximum-likelihood fit of Q, R, S_O, storm-Q coefficients via autograd through our PyTorch filter → profile likelihood / MCMC for honest parameter uncertainty → propagate ~50 parameter samples through the smoother (law of total variance), which makes covariances honest. Validate on the OSSE first (learned values within the Cramér-Rao bound).
   - Data needs (derived): gauge R learnable to ~2% from one 5-day run; the jump variance ~22%; drag R not learnable from one run (5 points).
8. **Storm handling:** Kp-scheduled Q (q₀ + q₁·max(0, Kp−3)^α, coefficients learned by ML) plus a 2-mode IMM. Inflate gap states only, never gains.
9. **Robust updates:** Student-t / Huber EKF for gauge mode jumps and outgassing bursts (Agamennoni et al. 2012 IEEE TSP 60:5024; Karlgaard & Schaub 2007 JGCD 30:885), paired with a CUSUM-on-NIS step detector so real level changes aren't rejected.
10. **Variational-Bayes adaptive R onboard** (Särkkä & Nummenmaa 2009 IEEE TAC 54:596), so the filter adapts to real sensor noise without waiting for vendor numbers. Restrict adaptation to well-observed blocks.
11. **Physics-coupled states** (ΔT∞ with diurnal/latitude shape + slow O boundary perturbation; Weimer 2016 needed exactly T∞ + time-varying O; HASDM DCA) and **EOF/POD error modes** (Matsuo & Forbes 2010 JGR 115; Sutton 2012 Space Weather 10: 33% RMS better than spherical harmonics). Cheating risk in our OSSE (identical twin), so **only after the fraternal truth**.
12. **Driven gap model:** dx/dt = −x/τ + β·(driver_real − driver_forecast), with τ shrinking with heating (Burke 2009 JGR doi:10.1029/2008JA013848; Weimer 2011 JGR doi:10.1029/2010JA015685; density lags 2–4 h, Sutton 2009). Same cheating caveat.
13. **Smoother drivers:** GFZ **Hp30/Hp60** (30/60-min, open-ended Kp-like, near-real-time nowcast + forecast; Yamazaki et al. 2022 GRL doi:10.1029/2022GL098860; data doi:10.5880/Hpo.0002). Use it for the truth (realistic, no 3-h jumps) and legitimately for the operator prior.
14. **Report estimable functions in an explicit datum** (geodesy / bundle-adjustment "gauge freedom", Triggs 2000): e.g. "O on the FIPEX scale <1%, absolute O ±(prior)", stated honestly. Reparameterising alone doesn't improve accuracy (datum invariance) unless real cross-calibration priors exist.
15. **Onboard numerics:** UD/square-root or Joseph, P in double (M7 DP FPU). The cost of everything combined is still ≪1e6 FLOP per 30 s.

**Not recommended:** KalmanNet (needs truth labels, no honest covariance), H-infinity (no meaningful NEES), the desensitized KF (hand-tuned), truncated-Gaussian monotone constraints (use exp-parameterised rates instead).

### Must-do before trusting the advanced ideas

**Change the truth generator first:** DTM2020 or NRLMSISE-00 truth vs an MSIS 2.x prior, plus an injected slow O perturbation, plus smooth (Hp30) drivers. Otherwise anything parameterised in MSIS-driver space (11, 12, part of 5) looks artificially perfect.

---

## 1f. SWARM-EX (agent, after the Stuttgart call)

- **SWARM-EX has NOT flown.** As of the latest sources: 3 × 3U, "not launched (ELaNa 59)", planned 2026-12-29, ~400–420 km, 51.6–52° (Nanosats DB; GT SSDL page Jan 2026: "subsystem assembly and testing"). Launch has slipped repeatedly since Q4 2023. So the vendor's "closest flown precedent" means *planned user of the same Stuttgart FIPEX*, not flight heritage.
- **FIPEX on SWARM-EX:**
  - 2 sensors per spacecraft, because FIPEX is "novel… not yet been successfully flown" (Lowe et al. 2024, IEEE Aerospace). They want to see how the space environment degrades it.
  - Dayside only, off in eclipse; science instruments run 43% of the orbit.
  - Pointing ≤30° off ram (an empirical SNR limit).
  - FIPEX + Langmuir probe ≈ 8–14 W combined (Fitzpatrick & Palo 2025 ASR 75(9), doi:10.1016/j.asr.2024.06.057; Fitzpatrick 2022 AIAA doi:10.2514/6.2022-0236).
- **Published processing:** none. No current→flux→density method, no angle/wind/temperature correction, no uncertainty budget, no drift-tracking method. They use atomic O "as a proxy for density". Drift handling = redundancy + occasional cross-calibration between spacecraft (SMD-1, within 100 km).
- **Other FIPEX flights, drift:**
  - ISS/EuTEF 572 days (Schmiel 2009/2010): "significant differences" from models, no drift number.
  - QB50: "very limited results".
  - SOMP2b FIPEXnano 2021–2024 (Langer 2024): signal drop/saturation after dormancy, range-switching bug, heater warm-up spun the spacecraft, unexplained behaviour; **no sensitivity-vs-time numbers.**
  - **No published FIPEX drift number exists anywhere.** Drift stays a sweep → requirement.
- **What we can use or cite:**
  - Duty-cycling precedent (dayside only).
  - 30° pointing limit as a precedent.
  - Power order of magnitude.
  - Drag parameters in a GNSS navigation filter (Lowe 2024; Dennison, Stacey & D'Amico 2023), which is precedent for our host-drag EKF. Note: same Lowe as Lowe & D'Amico 2026.
  - SOMP2b commissioning lessons: half heater power at start, one sensor at a time, fixed measurement range within an orbit, expect a burn-in transient.
- **Our differentiation vs SWARM-EX:**
  - total density over the **whole orbit including eclipse** (gauge + drag) from **one** host vs O-only, dayside-only
  - **continuous in-flight self-calibration** of FIPEX through the filter (gauge + drag constrain its gain) vs redundancy
  - **composition beyond O** (N₂)
  - **in-flight S_O estimation**
  - a **published, quantified uncertainty method** (OSSE + NIS/NEES)
  - hosted payload, so no student bus or formation risk
- **What they do better (cite, don't claim):** multi-point formation, cm-level relative GNSS, a plasma channel, explicit cross-calibration demonstrations.
- Sources and PDFs: `scratchpad/swx` (agent working files); key URLs:
  - https://slab.stanford.edu/projects/swarmex
  - https://par.nsf.gov/servlets/purl/10582659
  - https://par.nsf.gov/servlets/purl/10582655
  - https://www.nanosats.eu/sat/swarm-ex
  - Langer et al. 2024 CEAS Space J. 16:569, doi:10.1007/s12567-023-00530-y

---

## 1g. Inferring the OTHER gases (O₂, He, N, Ar, H) from measured O + N₂ + ρ (3 agents + cross-critique round)

**Answer: yes, partly, with big gains in storms and modest gains in quiet times.** The method is a **regularised Bayesian fit of a few model drivers** (effective F10.7 and ap, or better T∞ plus boundary scales) to our measured O, N₂ and ρ. The other gases are then read from the adjusted model.

**Key rules found:**
1. **Observation error must include ~15–20% model-representation error**, not just sensor noise. Without it, the fit overrules the prior and makes quiet-time minor species *worse* than the plain forecast. The physics agent found this; the storm agent confirmed it in round 2.
2. **N₂ correction:** N₂ inferred as (ρ − m_O·n_O)/m_N₂ wrongly lumps O₂ and He mass into "N₂" (5–12% too high in storms at 250–300 km). **Iterate:** n_N₂ = (ρ − m_O·n_O − m_O₂·n̂_O₂ − m_He·n̂_He)/m_N₂. Above 450 km at solar minimum, ρ − O is mostly He, so the residual is a He measurement there.
3. **Gate by regime:** quiet low-latitude O₂ and Ar → keep the forecast (the sensors add nothing). Better still, the filter learns the persistent MSIS-vs-reality O/N₂ offset as its own bias state so the drivers don't absorb it.
4. Fit **at least two** drivers (ap alone breaks when F10.7 is also wrong). Smooth along the orbit (Kalman/3D-Var).

**Expected accuracy:** fraternal twin (truth = NRLMSISE-00, model = MSIS 2.1), 5% sensor noise, 6 dates × lat/lon/alt grid, median / P90 factor error %. This is a *lower bound* on the real error.

| Gas | Storm high-lat: forecast → ours | Storm low-lat | Quiet high-lat | Quiet low-lat | Verdict |
|---|---|---|---|---|---|
| **O** | measured | measured | measured | measured | **measured** |
| **N₂** | inferred (~5% + propagated O₂/He) | same | same | same | **credible** |
| **O₂** | 271/719 → **25/46** | 104/282 → **17–20/50** | 21/51 → 21/43 | **forecast 6/15** | **storm: credible ~±25%**; quiet: model |
| **He** | 122/366 → **15/38** | 36/65 → **8/27** | 15/23 → **5/18** | 4/10 → 4/10 | **credible** (storm ±8–15%, quiet ±5%); real-world coupling to verify on DE-2 |
| **N** | 92/356 → **19/52** | 94/208 → **13/37** | 15/31 → **7/18** | 10/20 → **8/19** | weakly credible; physically photochemical (model-dominated) |
| **Ar** | 673/2366 → **22/70** | — | — | forecast 10/28 | storm improves; model-only claim |
| **H** | 98/285 → 18–29/45 | — | — | — | model-only (no physical link) |

**Storms, where it matters most:** O₂/He/N/Ar errors drop **4–10×** vs the forecast-driven model. Quiet: He and N improve modestly; O₂ and Ar stay with the model.

**Real-data support:**
- He depletion and Ar rise at high latitude in storms, plus He rise at low latitude, are observed (AE-C Feb 1974 storm, Mayr & Hedin 1977 JGR 82; ESRO-4/OGO-6; CHAMP/GRACE Liu et al. 2014 doi:10.1002/2013JA019453).
- O/N₂ can also *rise* (DE-2, Burns et al. 1995).
- **No published coefficient** links He to O/N₂, and **no in-situ O₂ storm data above ~250 km exist** (ion-source recombination). O₂ claims are model-physics-based.

**Honest validation:**
1. **DE-2 NACS replay** (public CDF: https://cdaweb.gsfc.nasa.gov/data/de/de2/neutral_gas_nacs/, doi:10.48322/j8kp-5y58; O, N₂, He, N, Ar at 250–500 km, Aug 1981–Feb 1983, includes the July 1982 Kp≈9 storm): feed only O + N₂ + ρ, score He/N/Ar against measured.
2. AE-C/E data for solar minimum.
3. Physics-model truth (TIE-GCM/WACCM-X runs for May 2024).
- Caveat: DE-2/AE went into building MSIS, so in-sample bias is possible.

**Hardware:**
- No extra hardware is needed for the claims above.
- Direct O₂/He/Ar would need a miniature neutral mass spectrometer (heavier, costlier).
- The Pt channel was ruled out by the vendor.
- In-situ UV absorption for O₂ is impossible (optical depth ~10⁻⁷, derived).
- A second gauge adds little (O₂ and N₂ ionise similarly).

**Where it fits our plan:** a **post-processing layer** on the filter's O/N₂/ρ (doesn't change the main filter), so it can be built in Phase B/C. It belongs with the parked "physics-constrained states", and must be scored on the fraternal truth / DE-2, never on the identical twin.

Agent scripts: `scratchpad/inv/` (physics), `scratchpad/storm/exp3.py`, `exp4.py` (storm).

**Addendum: physics agent's round 2** (reproduced the storm agent's setup, 1,728 points, truth NRLMSISE-00):
- The two agents agree; they had tested different regimes.
- **The fraternal test is biased against O₂ adjustment:** MSIS 2.x refit only O and N₂, so the truth's O₂ follows the *drivers*, not N₂. Quiet-time "harm" is partly a test artifact.
- **Regularized fit (Mreg) results:**
  - **Solar minimum:** O₂ 101% → **6%**, He 12 → 6%, N 38 → 12%.
  - **Storm:** He 58 → **5%**, N 51 → 14%, O₂ 72 → 18%.
  - Ratio scaling *worsens* He in storms (He isn't tied to O).
  - Regularization cuts the P90 tails massively (solar-min O₂ P90 1326% → 37%).
- **Recipe refinement:**
  - Fit **O and ρ directly** (not pre-differenced N₂), so He and O₂ are included automatically.
  - Observation error = sensor + ~15% model structure.
  - Priors: F10.7 σ 0.10 (ln); ap σ 0.8 storm / 0.4 quiet, tied to forecast confidence.
  - Optional He multiplier (σ 0.3–0.5, set from DE-2 residuals).
  - Correlated over a few orbits (IDEA-style).
  - Report the O₂ spread between Mreg and ratio scaling as its uncertainty.
- **Verifiable expectations** (assumption until the DE-2 test):
  - He 20–30%; N ~15% in storms.
  - O₂ "physics-adjusted, unverified ±30%".
  - Ar and H model-only.

---

## 2. Physics insights (verified)

- **[DERIVED] The gauge is nearly a mass-density meter without a ram chamber.** S/m: O 0.56/16 = 0.035, N₂ 1/28 = 0.036, O₂ 0.032, He 0.045.
  - That's why gauge + drag can't give composition (our old condition number ~120), and why composition rests on FIPEX.
  - With the ram chamber (√m weighting), the per-mass weights become O 0.14 vs N₂ 0.19, so the gauge regains a little composition sensitivity.
- **[DERIVED] Ram chamber equilibrium** (collisionless orifice): n_chamber/n_ambient ≈ √(T_a/T_c)·[e^(−x²) + √π·x·(1 + erf x)], with x = s·cos θ and s = V/√(2kT_a/m). For large x this becomes n_c ≈ n_a·V·cos θ·√(2πm/(k·T_c)).
  - So the chamber senses **flux** and is nearly independent of ambient temperature.
  - Chamber wall temperature error: ½·ΔT/T (10 K at 300 K = 1.7%).
  - Attitude error: δθ·tan θ (2° at 45° = 3.5%; 2° at 70° = 10%), so gate θ > 60°.
  - The textbook citation is UNCONFIRMED; Moe & Moe 1968 (NASA CR-96311) and Horowitz & Newton 1969 (TN D-5447) use this framework.
- **[DERIVED] Wind and corotation** change the ram speed by up to ~0.46 + 0.1–0.3 km/s → 1–6% flux bias for both the gauge and FIPEX.
  - Not in our simulation. Add an HWM-type wind prior or treat it as noise; storm winds matter.
- **[DERIVED] Composition varies with altitude:** ln(O/N₂) changes with scale height ~77 km at 1000 K.
  - Oblateness (±13 km at 51.6°) and eccentricity give natural excitation. Tested: small benefit with the current state design. It would matter more with physics-constrained states.
- **[LIT] Explorer 32 trusted its gauges for relative variation (2%) and drag for the absolute level.** That's exactly our architecture, and good heritage to cite (Newton, Pelz & Volland, NASA TM-X-63198, NTRS 19680014226).
- **[LIT] Ion gauges have never been calibrated in atomic O** (Friedman 1966, SAO Spec. Rept. 217). Re-interpreting O recombination changed Explorer 17/32 densities by **2×** (Ballance 1969, NASA TM-X-53898).
  - So S_O / recombination is a real, historically documented risk. Our sweep plus in-flight estimation plus a lab test is the answer.
  - Choosing a wall material with stable, known recombination (near-complete, like the OGO 6 antechamber, Hedin 1973 TN D-7239) can make it predictable.

---

## 3. Failure modes worth handling in software (top list)

**Gauge:**
1. **O response and wall recombination.** Unknown; 2× historical ambiguity. Mitigation: O-aware measurement model, S_O state or consider parameter, choice of wall material, anchor to drag.
2. **Outgassing background.** Additive, t^−0.5 decay, worst at night and high altitude. Mitigation: background state separated from gain by day/night variation, wake or angle sweeps if the host slews, discard the first weeks (SOMP2b needed "a few weeks" to commission).
3. **Attitude / angle of attack.** Mitigation: host quaternions as a hosting requirement, gate θ > 60°, fit the angular law from host slews.
4. **Chamber temperature.** Mitigation: thermistor and √T_c correction (Arrhenius for the background).
5. **Adsorption/desorption memory.** Up to −34% on Explorer 17 (Moe & Moe 1968, snippet). Mitigation: a wall-coverage state, or avoid fast flux changes.
6. **Ignition delay** (~0.1–1 min at our pressures; random, ∝ 1/p, INFICON manual). Mitigation: keep HV on, restart on the dayside, mask the first minutes. Gaps are already handled by NaN skipping.
7. **Nonlinearity and discharge mode jumps.** Mitigation: piecewise calibration, step detection on innovations.
8. **Contamination ageing.** Mitigation: gain random walk anchored to drag.
9. **HV arcing during launch outgassing.** Mitigation: HV-on interlock below 5e-3 mbar, ramp, watch current.
10. **Magnet versus host ADCS** (see TL;DR 12).

**FIPEX:**
1. **Per-unit calibration +35/−28%** (Eberhart 2019) and per-unit power-law curves. Mitigation: individual calibration, in-flight scale factor, fleet consensus.
2. **Temperature control.** Ion conductivity is exponential in T. Mitigation: closed-loop heater; reject data while unsettled.
3. **Re-accommodation after O₂ exposure or heater off.** Upleg data were unusable on WADIS. Mitigation: burn-in, gate after any heater-off. **So avoid FIPEX duty cycling where possible.**
4. **Flux, not density; angle mattered >10× on WADIS-2.** Mitigation: fixed ram-normal mounting, flag large θ.
5. **Poisoning** (silicone/siloxane, as with industrial hot sensors). No FIPEX space data. Mitigation: drift states, FIPEX/gauge ratio trend monitoring, host materials control near the aperture.
6. **O₂ from Pt − Au** is poor above ~350 km (O₂/O a few %). Treat O₂ as unobservable there.

**Drag:**
- C_D–density correlation ≈1 when co-estimated (CEAS 2025, doi:10.1007/s12567-025-00657-0).
- Attitude can change projected area 2–5×.
- Thrust events alias into density.
- Solar radiation pressure matters at 450 km near solar minimum.
- Mitigations: per-host ballistic nuisance state, host attitude and thrust logs, residual-jump detection.

**Consistency checks the software can run:**
- The implied O fraction (FIPEX/gauge) must stay within physical bounds (~0.4–0.95 at 300–450 km).
- Pt ≥ Au must hold.
- Fleet conjunction comparisons; NIS monitoring for steps.

---

## 4. Filter and software improvements (ranked)

1. **Gauss-Markov states** (TESTED, adopt).
2. **Fix NEES:** per-subspace NEES plus an innovation whiteness test (Bar-Shalom 2001); first-estimates Jacobians for the gain states (Huang et al. 2009/10); Schmidt consider parameters for S_O and the gas factors (Schmidt 1966; Zanetti & D'Souza 2013, J. Astronaut. Sci. 60:672).
3. **Ground RTS / fixed-interval smoother** (TESTED, 10–25% better).
4. **Drag as an integral measurement** (accumulator state, or stochastic cloning, Roumeliotis & Burdick 2002). The agent's top pick. My test suggests drag isn't the NEES cause, but it's still the correct model of the measurement.
5. **Additive background state** for gauge outgassing.
6. **Drift-rate state for FIPEX's one-sided drift** (earlier finding 8).
7. **Storm handling:** inflate Q on the model-gap states only, **never on the gains** (or storm composition aliases into the gains). Driven by measured Kp/ap, optionally a 2-mode IMM (Blom & Bar-Shalom 1988). My smoothed oracle test gave only a small benefit.
8. **Iterated EKF** (2–3 iterations; Bell & Cathey 1993) instead of a UKF, if nonlinearity matters. Cheap.
9. **Physics-constrained states** (exospheric temperature + δO; HASDM DCA, Storz 2005; Weimer 2016 JGR doi:10.1002/2016JA022691). Only after C2.
10. **Onboard implementation:** sequential scalar updates, Joseph or UD (Bierman 1977), **P in double precision.** In float32 the per-step gain Q (~1e−9) falls below P's resolution. The M7 has a double-precision FPU. Compute is trivial (~10⁴ FLOP/epoch even with IMM).

---

## 5. Calibration chain for the proposal (cal/val plan)

1. **Ground:** per-unit calibration of the CCG + FIPEX pair in one chamber, with the RGA as composition reference. Ideally test the CCG in Stuttgart's AO beam (S_O). FIPEX per-unit curves.
2. **Commissioning:** burn-in (outgassing decay, FIPEX accommodation). Gauge background measured in low-density windows or wake attitudes.
3. **In flight, per unit:** GM filter learns the gains from orbital composition variation; drag anchors the absolute level daily; Explorer 32 heritage (relative from the gauge, absolute from drag).
4. **Fleet:** crossover ubercal for relative gains (Padmanabhan 2008 ApJ 674:1217; GSICS SNO, Goldberg 2011 BAMS 92:467; Balzano & Nowak 2007 IPSN blind calibration). Absolute scale from fleet-averaged drag, which averages down independent C_D errors, plus reference missions (Swarm, GRACE-FO) at conjunctions.
5. **Validation:** GOLD ΣO/N₂ for storm morphology and relative change, not absolute (GOLD reads ~40% above MSIS; Liu 2023). Swarm/GRACE-FO densities at conjunctions.

---

## 6. Relevance-score ideas (Relevance = 5 needs "well-evidenced case for model improvement")

1. **Model-improvement demo** in the OSSE. Estimate effective drivers or exospheric temperature, forecast forward, and score vs the NOAA baseline at 0/6/24/48 h.
   - Metrics from Bruinsma et al. 2018 (Space Weather 16:1806) and the storm metrics of Bruinsma et al. 2021 (JSWSC, doi:10.1051/swsc/2021002).
   - Prior art: HASDM DCA (−32% epoch error, −25% 1-day prediction error), MSIS-UQ (Licata 2022), EXTEMPLAR (Weimer 2021), Sutton 2018 IDEA.
2. **Ablation:** drag-only vs drag + gauge vs full suite, compared at other altitudes and on forecast skill. Shows composition adds value beyond density (Sutton 2018; Morozov 2013).
3. **Gain-free observables** (radio "closure" idea): ln ρ(t₁) − ln ρ(t₂) for one unit doesn't depend on its gain. Shows **precision** (10%) is met even with 30% gain uncertainty; accuracy comes from the calibration chain.
4. **The May 2024 storm motivation:** forecast Ap 90 vs actual 271. Parker & Linares 2024 (doi:10.2514/1.A36164): "poorly predicted, even one day in advance"; mass Starlink manoeuvres.

---

## 7. Acquisition and compute tricks

- **Event-triggered telemetry:** send only when the innovation exceeds kσ, plus a storm mode on a Kp alert (Wu et al. 2013 IEEE TAC; Sun & Work 2017). Quantify bytes/day vs error in the OSSE. That's a Cost/Scalability point.
- **Duty cycling:** keep the gauge on (ignition, outgassing burst on restart). FIPEX off in eclipse is what SWARM-EX does, but re-accommodation is a risk, so weigh it against power.
- **Keep the gauge running across terminators and latitude extremes,** where composition changes fastest (the calibration excitation).
- **ML:** use MSIS-UQ-style calibrated priors (low risk). Keep KalmanNet out of the flight path; at most an offline benchmark (Revach 2022 IEEE TSP 70:1532).

---

## 8. For Stuttgart today (updated priorities)

1. **"Your WADIS-2 paper reports +35%/−28% per-sensor calibration uncertainty. What is the new absolute calibration's uncertainty, and is it per unit?"** Most important.
2. **Drift / sensitivity loss per month in AO.** The second most important number for us.
3. Re-accommodation after heater-off or O₂ exposure: how long, and can we duty-cycle?
4. Poisoning / contamination sensitivity (silicones); host material constraints near the sensor.
5. Angle response (WADIS-2 saw >10× with orientation); recommended mounting.
6. Can their AO facility test our CCG (S_O; recombination on our chamber walls)?
7. SOURCE / SOMP2b in-orbit data (SOMP2b FIPEXnano flew Jan 2021 – Nov 2024; Langer et al. 2024, CEAS Space J., doi:10.1007/s12567-023-00530-y).

## 9. For INFICON (updated)

- **Magnet dipole moment / external field** (host ADCS risk).
- Ignition delay at 1e-7–1e-6 mbar; is there a low-pressure starter option?
- Pumping speed per gas.
- Behavior in O / O₂ (wall material, recombination).
- Outgassing of the gauge itself.
- Drift per month; is 30% a 1σ or a bound; temperature coefficient (head vs electronics).

---

## 10. Reviewer objections to pre-empt

- "Ion gauges respond badly to atomic O" (NASA TN D-6815: oxygen the only problematic gas; sensitivity shifts up to 25% with use). **Answer:** S_O sweep + in-flight estimation + lab plan + Explorer 32 relative/absolute split.
- "Outgassing / contamination." **Answer:** background state + burn-in + windows.
- "Host B/m and attitude." **Answer:** per-host nuisance states + fleet averaging + hosting requirements.
- "N₂ error amplification." **Answer:** honest numbers vs drift/calibration requirements; GM self-calibration; fleet ubercal.
- "Relying on MSIS as the reference" (the Argo pitfall). **Answer:** drag and reference missions anchor the absolute level; MSIS supplies only the shape.

---

## 11. Open / unconfirmed

- NEES ≈ 3 cause not yet found (see §4.2).
- Ram-enhancement textbook citation; TN D-5447 error table (image-only PDF, not OCR'd).
- MAG084 magnet moment (estimate only).
- FIPEX in-orbit degradation data: none published that the agents could find.
- A paper driving Q directly from Kp: not found.
- Physics-constrained states: must re-test with a different-model truth.
