# Proposal claims register (what to state, with its evidence and caveat)

Living list kept by Claude from Nov 11 onward. Every claim lists its evidence and the caveat it must carry. Numbers are
replaced by final (post-freeze) values at writing time; "PRELIM" marks pre-freeze numbers. Details:
docs/research_findings_2026-11-10.md, docs/status_and_plan.md §7a, docs/sources.md.

## Framing (Relevance)
- **The gap we fill.** OCC's own reference review (Bruinsma et al. 2023, Adv. Space Res., doi:10.1016/j.asr.2023.05.011):
  "In situ composition measurements have not been taken since the Dynamics Explorer 2 mission in the early 1980s";
  density data sparse "for high solar activity, in particular below 400 km"; recommendation 3.2.2 asks for simultaneous
  mass density + composition (O, N2, O2, He) "to revise the composition information in the models"; 3.2.3 asks for
  uninterrupted storm monitoring; 3.1.3/3.1.4 data assimilation with accurate covariances. Our suite does all of these
  from a hosted payload.
- **Model-error context.** Real MSIS storm error: NRLMSISE-00 storm std 14.5 / 21.6 / 27% at GOCE / CHAMP / GRACE
  altitudes (Bruinsma & Laurens 2024). Our DE-2 comparison (real data): MSIS 2.1 storm-day density -26...+11%,
  N2 -51...+15% (450 km cutoff). Datasets themselves disagree by up to 30% (Bruinsma et al. 2023 ASR 72:5476).
- **Composition is the data type operational systems lack**; initialising thermosphere composition gives most of the
  storm-forecast benefit (Chartier, Jackson & Mitchell 2013, JGR 118:7329).
- **Measurand.** Mass density + O + N2 number density (He, O2 = model-based inference, labelled). Do NOT claim the
  pressure or drag-acceleration rows ("drag or pressure as an indirect route" caps Relevance at 3).
- **Altitude range.** Declare from the C6 grid (pending). Composition 250-400 km (450 km with He caveat); density
  higher. Outgassing breaks N2 above ~400 km at solar minimum (L8), which supports the cap.

## Performance numbers (PRELIM, harsh truth = NRLMSISE-00 + calibrated driver errors, median MAE)
- Model (prior) error on this truth: density 15.7% quiet / 23.9% storm; N2 20% / 29% / 19.6% recovery.
- Ours, 3 sensors, S_O +-16% consider: density 6.2 / 8.2 / 10.7% (2-3x better than model, 2x inside 20%).
- Ours, ground S_O calibration (+-5%) + in-flight estimate + daily leak: density 3.4 / 3.5 / 4.7%;
  N2 11.0 / 15.0 / 15.6% (~2x better than the model in every window).
- Without leak AND without S_O calibration, recovery N2 (30%) is WORSE than the model (19.6%): leak + S_O calibration
  are required for "composition beats the model in every window". State them as part of the design, not extras.
- Report accuracy = bias, precision = 1-sigma scatter of 30 s errors, resolution = 30 s, plus MAE p50/p90 (headline.py).
- Real-time numbers from 2000 runs; smoothed ground product from 100 runs (memory limit); say so.
- **Ground RTS smoother** improves density ~20-30% in quiet/recovery (Phase B tests). Ground product = smoothed.

## Truth ladder (how we tested; answers "your truth is your model")
- Three truths: NRLMSISE-00 (independent empirical model); MSIS + effective-driver errors calibrated to published
  model-vs-data error (Sutton 2018; Licata et al. 2022 MSIS-UQ; Bruinsma & Laurens 2024; storm-window scatter set to
  0.20 at 300 km), plus an independent O error (Weimer et al. 2016); and real DE-2 NACS composition (1981-83).
- OSSE best practice: truth errors must match real model-vs-data statistics (Hoffman & Atlas 2016, BAMS 97:1601).
  Ours do by construction; the prior's error on the harsh truth reproduces the published storm error.
- DTM2020 not used (CNES academic/non-commercial licence).
- DE-2 protocol: Jul 13-14 1982 development window used before the freeze; Sep 3-10 1982 (Kp 8.7), Mar 1-2 1982,
  Feb 4-5 1983 held out and run once. NACS has a 25% absolute calibration error (PI statement; Carignan et al. 1981), so
  the replay tests tracking of real departures from MSIS, not the absolute benchmark. Circularity: DE-2 helped build
  MSIS-86, but MSIS 2.x tuned its thermosphere to 1986-2005 data (Emmert et al. 2021), and circularity favours the prior.

## DE-2 development window (Jul 13-14 1982, real NACS truth, 280-450 km; PRELIM, dev = used for design)
- Architecture (ground S_O cal 5% + estimate + leak + altitude-slope states): density model 23% / 48% -> ours 4.1% /
  3.5%; N2 model 71% / 140% -> ours 24% / 45% (3x better); O model 12% / 32% -> ours 17% / 15% (worse day 1, 2x better
  day 2). NEES ~22 (error bars need calibration on real data).
- Finding that drove a design change: real MSIS N2 error grows with altitude (ln NACS/MSIS -0.32 at 300 km -> -0.95
  at 400+ km; O flat) = temperature-type model error (Weimer et al. 2016). Added per-gas altitude-slope states:
  inert on a circular host (bit-identical OSSE), essential on eccentric orbits / real data.
- Framing: DE-2 is data-starved (minutes per day below 450 km; 3.6-11% of 30 s bins covered) vs continuous hosted
  sampling; the O/N2 split needs long sampling, so DE-2 is a harsher information regime than our design. "That
  scarcity of composition data is the gap this suite fills."
- Rejected in dev: N2 prior 35% alone (no change: information, not prior, was the limit).

## FROZEN ARCHITECTURE (freeze-v1, Nov 11) - every post-freeze number runs on this
- Register defaults: S_O estimated, ground-calibrated to 5% (requirement; uncalibrated bracket SO_BRACKET_SD 0.16);
  daily argon leak; ram gauge; per-orbit single-frequency drag 15%; gaps on; NIS gate 15.1; gap prior 20%; Q x4
  (re-checked on both truths: x8 more honest but quiet N2 ties the model); altitude slopes on; N2 harmonics off;
  truth C_D physics. Real-time filter product (the RTS smoother is NOT in the architecture: it degrades estimate-mode
  results; later work).
- Pre-freeze harsh-truth numbers (Q x4, 100 runs): density 3.2 / 3.2 / 4.8%; O 5.8 / 10.3%; N2 10.0 / 16.1 / 16.6%.
- Error-bar calibration factors (filter z, harsh truth, 30 runs): density x2.0, O x2.8, N2 x3.4 (worst window);
  density honest in quiet (z 0.96, 68% inside 1 sigma). Verify on held-out DE-2 + GRACE-FO.
- DE-2 dev rerun on the frozen setup: density 23% / 48% -> 5.0% / 3.8%; N2 71% / 140% -> 21% / 44%; O 12% / 32% ->
  16% / 17%.

## HARDWARE BASELINE DECISION (Nov 11, user): NO calibrated leak in the baseline
- Baseline = current CAD (gauge + FIPEX + host GPS drag) + ground S_O (or S_O/f same-beam) calibration to 5%.
  Headline numbers = the base_* cases (headline.py). The leak cases below become the "Phase 2 enhancement".
- Wording: "A calibrated-leak gauge calibrator (Phase 2 trade study; calibration-gas heritage from flight mass
  spectrometers: MAVEN NGIMS, Mahaffy et al. 2015; LADEE NMS) improves density from ~X% to ~3-5% and makes N2 beat
  the model in every window." Do NOT present the leak as baseline hardware (novel for a cold cathode gauge; no flight
  precedent found).
- Hardware the leak would need (rough estimates, verify with vendors/mech): Ar reservoir (few cm3, ~1 bar; ~3.6 mg/yr),
  calibrated leak (~1e-5 mbar L/s), normally-closed latching microvalve, port into the gauge chamber (CAD change),
  ~50-150 g, power only for brief pulses; small pressure vessel rules; fail-closed. Leak calibrates the chamber
  response, not the inlet (K6).
- Pre-freeze 100-run estimate of the baseline (harsh): density 6.5 / 7.4 / 7.7%; recovery N2 ~ model (~19%).
  -> replace with base_harsh (2000 runs) when done.

## INFICON numbers (expected soon; user Nov 11: "most if not all", do not assume all)
- When they arrive: put each into params.py with kind "vendor" (gauge noise, drift, gain accuracy meaning, gas
  factors, ignition, temperature coefficient, nonlinearity), read the final Phase A curves at those values, and do
  ONE confirming headline run. Phase A sweeps already bracket them, so no re-tuning; frozen filter unchanged.
  Phase A first pass: gauge noise 0.5-5% and gas factors barely matter; gauge drift <= ~2%/day fine.

## HEADLINE RESULTS (freeze-v1, 2000 runs, Colab Nov 11; out/headline/*.csv) - quotable
Harsh truth (NRLMSISE-00 + calibrated driver errors), real-time filter; accuracy = median bias, precision = median 1-sigma
scatter of 30 s errors, MAE p50 / p90; model = forecast-driven MSIS 2.1 on the same runs. Quiet / storm / recovery:
- DENSITY: accuracy +0.1 / +1.1 / +1.8%; precision 1.7 / 2.3 / 2.6%; MAE 3.2 / 3.6 / 4.7% (p90 7.4 / 8.0 / 11.4%);
  model 15.3 / 22.9 / 15.1%. Meets 20% / 10% / 30 s with margin even at p90; 4-6x better than the model.
- O: MAE 5.6 / 9.8 / 10.6% (p90 12.6 / 28.5 / 29.7%); model 14.1 / 17.2 / 14.0% (1.4-2.5x better at median).
- N2: MAE 10.3 / 15.5 / 14.4% (p90 21 / 47 / 28%); model 20.5 / 29.6 / 19.5% (~2x better at median).
- Robustness (density MAE): driver-error truth 3.1 / 3.3 / 3.7%; NRLMSISE-00 3.2 / 3.3 / 4.4%; twin 3.0 / 2.7 / 3.0%.
- C9 best estimate (FIPEX drift 1%/day, gauge 0.5%/day, C_D 5%): density 2.7 / 2.7 / 3.7%; N2 10.3 / 11.0 / 11.7%.
- Uncalibrated (S_O bracket 16%, no leak): density 6.1 / 8.6 / 10.8%; N2 recovery 29% (WORSE than model 19.5%).
- Dual-frequency GPS: no gain over single-frequency (same as Phase A).
- Sensor ablation (harsh): drag alone density 13.6 / 17.0 / 15.3% (~model level); gauge + drag + leak (no FIPEX)
  density 3.5 / 3.6 / 3.7%, O 8.9 / 14.3 / 11.0%, N2 16.5 / 14.4 / 14.8%; full suite O 5.6 / 9.8 / 10.6%,
  N2 10.3 / 15.5 / 14.4%. => the calibrated gauge delivers density; FIPEX delivers composition (quiet O 8.9 -> 5.6%,
  quiet N2 16.5 -> 10.3%).
- HONEST TAILS: in the worst 10% of runs, storm/recovery O (28-30%) is worse than the model's median. NEES tail
  (p90 98) is driven by gap_He (p90 91; He is not a reported product) and FIPEX gain o_gain (p90 24); without FIPEX
  the tail vanishes (gauge+drag NEES p90 5.4). Report medians AND p90; error-bar calibration must cover the tail;
  Phase 2: FIPEX gain/drift robustness (consider or robust update).

## STAGE 6: the data improve the model (driver fit; scripts/driver_fit.py, out/stage6/) - Relevance evidence
Method: every 3 h, fit 2 numbers (effective F10.7 scale, effective ap scale on the NOAA forecast drivers) so NRLMSIS
2.1 matches the FUSED density + O, weighted by filter covariance x calibration factors (2.0 / 2.8) + 5% representation
floor; random-walk pull block to block (choice: 0.1 / 0.7 in ln). Effective drivers capped to the physical index
range (ap <= 400, F10.7 60-400). Truth = harsh (NRLMSISE-00 + calibrated driver errors), so the MSIS 2.1 fit cannot
match it by construction. Rebuild self-check passed (prior + truth reconstructed = scenario tables).
PRELIM: 3 recorded runs of 'harsh' (with leak), mean over runs. FINAL = rerun on base_harsh (no leak) + more recorded
runs before quoting as statistics.
- WHOLE COLUMN from one satellite at 300 km (storm window, vs column truth on the same track/times), density MAE
  forecast-driven model -> fitted model: 250 km 23.4 -> 6.7%; 300 24.8 -> 8.0; 350 26.2 -> 10.0; 400 27.7 -> 12.2;
  450 29.1 -> 14.4; 500 30.6 -> 16.5%. O: 18.9-28.5% -> 14.6-17.8%. => 2-3.5x better density 250-500 km.
- FORECAST (all windows, correction held and damped exp(-lead/12 h); 12 h = calibrated driver-error correlation
  time): density 18.3% -> 8.9 / 10.6 / 13.4 / 15.9% at 3 / 6 / 12 / 24 h lead; O 15.0 -> 11.8 / 12.0 / 13.1 / 13.3%.
  Improves at every lead tested; benefit halves by ~12 h.
- At the satellite: fitted model density 11.6 / 12.5 / 13.3% (model 19.0 / 25.6 / 14.6%; fused 5.4 / 6.4 / 8.3%).
  The fused product stays the product; the fitted model is the extension away from the track.
- CAVEATS: (1) truth is model-shaped (NRLMSISE-00 vertical structure), so the altitude transfer may be optimistic;
  real-data check NOT DONE (option: fit to GRACE-FO fused density, score against Swarm at another altitude). (2) Recovery-window O
  is WORSE with the fit (12.3 -> 17.5%): 2 knobs compromise density vs O; don't claim O improvement in recovery.
  (3) First version persisted the correction undamped and blew up at 12-24 h (ap scale x20 hitting storm-time
  forecast ap, outside MSIS range); fixed by physical caps + damping (disclose as a design lesson, not hidden).
- TESTED, NOT CLAIMED: model-based inference of unmeasured gases gets WORSE (He 11.0 -> 11.0; O2 17.5 -> 26.5;
  N 26.4 -> 33.3; Ar 27.2 -> 43.3; H 21.1 -> 24.6%): two driver knobs bend MSIS composition the wrong way when the
  truth's composition structure differs. => products are measured O, N2, density only. More species = hardware
  (Phase 2: small neutral mass spectrometer / extra species sensor; filter takes any sensor with a predict function).
- Wording: "Our measurements correct the operational model, not just the point we fly through: fitting effective
  drivers to the fused data cuts storm-time density error 2-3.5x from 250 to 500 km and improves 3-24 h forecasts
  (simulation, PRELIM)."

## Honest uncertainty
- Gate false-alarm rate matched chi-square exactly (1.0e-4 at p = 1e-4) in clean runs: evidence the innovations are
  correctly scaled.
- Density and O error bars honest (z ~1) with S_O consider analysis; N2 ~2x overconfident, so a calibration factor is
  measured on the OSSE and verified on DE-2 (PRELIM; product-z run pending for the final architecture).
- Root cause of residual overconfidence (labelled HYPOTHESIS): unmodelled within-orbit (latitude/local-time) structure
  of model error; Phase 2 adds latitude-dependent error states. Drift was tested and ruled out as the cause.
- S_O handled by Schmidt consider analysis (Schmidt 1966; Bierman 1977) or ground-anchored estimation.

## Architecture / design choices (for the design-rationale table)
- 15-state Gauss-Markov EKF: per-gas model gaps (random walk, prior 20% from published error), common + per-gas AR(1)
  wiggles, gauge gain, FIPEX gain, C_D bias, S_O; ram-chamber gauge model n_c = n V cos(theta) sqrt(2 pi m / k T_c)
  (Bird 1994; confirmed by Grabe et al. 2010); Joseph-form updates; NIS gate 15.1; per-orbit drag.
- TESTED AND REJECTED (say so, with reason): adaptive/Kp-scheduled Q (bounded by an oracle test: no recovery gain);
  N2 local-time harmonics (worsened N2 on 2 of 3 truths: weak N2 leverage); in-flight S_O estimation WITHOUT a ground
  anchor (S_O and the model's O/N2 error are indistinguishable: identifiability algebra); dual-frequency drag without
  physics C_D in the filter (NEES 2.0).
- Twin-derived priors were replaced by literature priors after the first fraternal test (model gap 5% -> 20%): shows
  the method was stress-tested, not tuned to look good.

## Calibration / validation plan (Performance scores this)
- Ground: gauge N2/Ar/He calibration; **same-beam gauge + FIPEX O-beam test fixing the S_O/f ratio** (beam flux error
  cancels; with the leak-anchored gauge gain this is as good as knowing S_O; algebra in findings doc section M);
  pre-conditioning to O exposure (Cross et al. 1995).
- Commissioning: leak reading at switch-on; >= 2 weeks; shutter/wake zero checks (L8); host yaw manoeuvres to
  calibrate C_D accommodation (March et al. 2021; OCC allows host manoeuvre requirements).
- In flight: daily argon-leak gauge calibration (novel for a cold cathode gauge; MAVEN NGIMS heritage), per-orbit drag,
  S_O tracking, FIPEX-vs-gauge drift tracking.
- Validation: OSSE truth ladder; DE-2 replay; GRACE-FO/Swarm conjunctions (validation only).

## Requirements to state (from Phase A; PRELIM until the final sweep)
- Gauge drift <~0.5%/day; FIPEX drift <~1%/day; S_O (or S_O/f ratio) known to ~5%; C_D 5% with host geometry model.
- Host asks: single-frequency GPS (dual = upside), attitude knowledge, geometry model, optional yaw manoeuvres.

## Resource needs
- Data: 30 s raw averages ~35 kB/day; raw 1 Hz 0.35-0.7 MB/day; processed 46-81 kB/day (L11).
- Compute: EKF ~2.1 kFLOP / 30 s, ~22 us on an STM32H7; smoother and S_O on the ground.
- Contamination (OCC requires it): all-metal CF chamber, no polymers, 150 C bake, sealed until orbit, baffle with no
  view of blankets, >= 2 weeks commissioning (L8). Outgassing negligible at 300 km after ~1 day.
- MAG084 magnet dipole = hosting risk (mech team to measure; mitigation and excluded hosts).

## Known issues to name with mitigations (K1-K11, findings doc R1)
- S_O never measured (bracket 0.51 cross-section to 0.71 full recombination; Laher & Gilmore 1990; Newton & Horowitz
  1969); recombination products; gauge nonlinearity and mode jumps; ignition delay (60 s at 1e-8 mbar); discharge
  pumping; leak path; same-beam relative only; wall temperature (1.7%/10 K) and pointing (1.5%/10 deg); background;
  no MAG084 drift data; FIPEX drift and n^0.35 response (Eberhart et al. 2019).

## In-flight drift/sensitivity tracking (answer to "what about drift / S_O / 1 year")
- Every headline number already includes, in the truth: FIPEX drift 3%/day one-sided, gauge drift 2%/day, gains
  +-30% unknown, S_O drawn per run (5% calibrated; 16% bracket in the uncalibrated case), C_D bias + drift + O-physics,
  per-orbit drag noise 15%, sensor outages, harsh model error. The filter tracks gauge gain (re-anchored daily by the
  leak), FIPEX gain (cross-checked vs gauge each 30 s and drag each orbit), S_O and C_D as states.
- Wording (draft): "Sensor gains are tracked in flight: the gauge is re-anchored daily by a calibrated leak and FIPEX
  is cross-checked against the gauge and drag every orbit. Gain errors reach steady state within ~2 days under 3%/day
  drift (self-calibration figure). Long-term validity rests on the leak; a 1-year simulation is planned (Phase 2)."
  -> CHECKED Nov 11 (harsh, recorded run 0): gauge gain error stays ~0-6% throughout (leak run), but the FIPEX gain
  error climbs to ~27% during the storm, i.e. the filter partly attributes the storm's O change to FIPEX gain. So do
  NOT claim "gain errors reach steady state within ~2 days" for FIPEX. Honest wording: gauge gain tracked to a few %;
  FIPEX gain tracking degrades in storms (this is the o_gain NEES tail); Phase 2 fix: FIPEX gain/drift robustness.
  Verify on base_harsh series and more runs before final wording.
- NOT covered (state as limits): 1-year accumulation not simulated; S_O time variation (conditioning, Cross et al.
  1995); FIPEX n^0.35 response; gauge nonlinearity/jumps beyond the gate; wall temperature / pointing (C7 pending).
- Wording rule (user, Nov 11): every sentence backed by a test, a citation or a labelled assumption; nothing implied
  beyond what was run.

## Caveats that must appear
- All OSSE numbers: 300 km, 51.6 deg, one storm (May 2024), 5 days, high solar activity.
- One-year drift not yet simulated (planned Stage 7).
- Outlier handling assumes median-of-30 preprocessing.
