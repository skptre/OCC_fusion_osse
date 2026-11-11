# Proposal claims register (what to state, with its evidence and caveat)

Living list kept by Claude from Nov 11 onward. Every claim lists its evidence and the caveat it must carry. Numbers are
replaced by final (post-freeze) values at writing time; "PRELIM" marks pre-freeze numbers. Details:
docs/research_findings_2026-11-10.md, docs/status_and_plan.md §7a, docs/sources.md.

## Framing (Relevance)
- **The gap we fill.** OCC's own reference review (Bruinsma et al. 2023, Adv. Space Res., doi:10.1016/j.asr.2023.05.011):
  "In situ composition measurements have not been taken since the Dynamics Explorer 2 mission in the early 1980s";
  !! QUOTE ONLY AS THEIR STATEMENT, never as our own absolute claim. Counterexamples a reviewer may know (checked
  !! Nov 11): QB50 CubeSats 2017 carried FIPEX (our sensor! e.g. SpaceCube, ~3 months; VZLUSAT-1) and an INMS;
  !! ExoCube (2015) / Dellingr INMS demo spectra; San Marco D/L (1988) carried a neutral mass spectrometer.
  !! SAFE WORDING: "no sustained, calibrated in-situ composition record has been produced since DE-2 (Bruinsma
  !! et al. 2023); CubeSat demonstrations since (QB50 FIPEX/INMS 2017, ExoCube) were short-lived." FIPEX's QB50
  !! flights are a PLUS: flight heritage for our O sensor (TRL argument).
  density data sparse "for high solar activity, in particular below 400 km"; recommendation 3.2.2 asks for simultaneous
  mass density + composition (O, N2, O2, He) "to revise the composition information in the models"; 3.2.3 asks for
  uninterrupted storm monitoring; 3.1.3 data assimilation with accurate covariances (3.1.4 = indirect obs, NOT us).
  [AUDIT FIX] 3.2.2 asks O2, N2, O, He "by means of mass spectrometers (e.g. DE2) or the Terahertz technique".
  SAFE WORDING: "answers 3.2.2 for the two dominant species (O, N2) from a hosted payload, with continuous storm
  coverage (3.2.3) and assimilation-ready products with calibrated covariances (3.1.3)." Never "does all of these".
  Also add counterexample: 2012 Chinese satellite (~499 km) miniature magnetic-sector mass spectrometer (Eur. J. Mass
  Spectrom. 2017, snippet only) -> say "...and experimental flights were short-lived". Never first / only / none.
- **Model-error context.** Real MSIS storm error: NRLMSISE-00 storm std 14.5 / 21.6 / 27% at GOCE / CHAMP / GRACE
  altitudes (Bruinsma & Laurens 2024; exact numbers re-check before quoting, journal 403 in audit). Our DE-2
  comparison (real data): MSIS 2.1 storm-day density -26...+11%, N2 -51...+15% (450 km cutoff).
  [AUDIT FIX] "datasets disagree by up to 30%" was mis-attributed (ASR 72:5476 = Bruinsma, Siemes, Emmert &
  Mlynczak 2023, doi:10.1016/j.asr.2022.09.038, a different paper; 30% not found there). Use instead the review's
  verified sentence: drag force "can vary by more than 30%" depending on the drag-coefficient model.
- **Composition matters for storm forecasts** [AUDIT FIX: scope]: in a TIEGCM study of the Halloween 2003 storm,
  initialising thermospheric composition captured nearly all the benefit of initialising the full thermosphere state
  for storm-time IONOSPHERIC forecasts (>=10% better for ~18 h) (Chartier, Jackson & Mitchell 2013, JGR 118:7329).
  Do NOT say it is about neutral density/drag.
- **Measurand.** Mass density + O + N2 number density ONLY. He/O2/N inference was tested in Stage 6 and REJECTED
  (gets worse); Bruinsma 3.2.2 asks O, N2, O2, He -> we cover the two dominant species. [AUDIT FIX] "~90% of mass"
  is NOT tested: He can reach ~half by number at 450 km at solar minimum (sources.md). State "dominant species at
  250-400 km" only, or compute the mass fraction from MSIS before quoting a %. He/O2 = Phase 2 hardware. Do NOT claim the
  pressure or drag-acceleration rows ("drag or pressure as an indirect route" caps Relevance at 3).
- **Altitude range.** Declare from the C6 grid (pending). Composition 250-400 km (450 km with He caveat); density
  higher. Outgassing breaks N2 above ~400 km at solar minimum (L8), which supports the cap.

## Performance numbers (SUPERSEDED pre-freeze history - do NOT quote; use HEADLINE / base_* sections)
- Model (prior) error on this truth: density 15.7% quiet / 23.9% storm; N2 20% / 29% / 19.6% recovery.
- Ours, 3 sensors, S_O +-16% consider: density 6.2 / 8.2 / 10.7% (2-3x better than model, 2x inside 20%).
- Ours, ground S_O calibration (+-5%) + in-flight estimate + daily leak: density 3.4 / 3.5 / 4.7%;
  N2 11.0 / 15.0 / 15.6% (~2x better than the model in every window).
- Without leak AND without S_O calibration, recovery N2 (30%) is WORSE than the model (19.6%): leak + S_O calibration
  are required for "composition beats the model in every window". State them as part of the design, not extras.
- Report accuracy = bias, precision = 1-sigma scatter of 30 s errors, resolution = 30 s, plus MAE p50/p90 (headline.py).
- [AUDIT FIX] Smoother lines deleted: the RTS smoother is NOT in the frozen architecture (real-time product only).

## Truth ladder (how we tested; answers "your truth is your model")
- Three truths: NRLMSISE-00 (independent empirical model); MSIS + effective-driver errors calibrated to published
  model-vs-data error (Sutton 2018; Licata et al. 2022 MSIS-UQ; Bruinsma & Laurens 2024; storm-window scatter set to
  0.20 at 300 km), plus an independent O error (OUR ASSUMPTION, 10%, 1-day; Weimer et al. 2016 supports only the
  temperature-type error, not the O term); and real DE-2 NACS composition (1981-83).
- OSSE best practice: truth errors must match real model-vs-data statistics (Hoffman & Atlas 2016, BAMS 97:1601).
  Ours do by construction; the prior's error on the harsh truth reproduces the published storm error.
- DTM2020 not used (CNES academic/non-commercial licence).
- DE-2 protocol: Jul 13-14 1982 development window used before the freeze; Sep 3-10 1982 (Kp 8.7), Mar 1-2 1982,
  Feb 4-5 1983 held out. [AUDIT FIX wording] "Run once; a bookkeeping bug found in that run was fixed generically
  (circular OSSE unchanged) and the held-out days were rerun once." NACS has a 25% absolute calibration error (PI
  statement in the NSSDC NACS data documentation; instrument: Carignan et al. 1981), so the replay tests tracking of
  real departures from MSIS, not the absolute benchmark. Circularity: DE-2 helped build MSIS-86; MSIS 2.x revised the
  thermosphere (Emmert et al. 2021: lower N2/O vs NRLMSISE-00; the "1986-2005" detail UNVERIFIED - soften to
  "re-tuned with later data" unless read); circularity favours the prior.

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

## *** BASELINE HEADLINE (NO LEAK) - THE LEAD NUMBERS *** (freeze-v1, 2000 runs, Colab Nov 11; out/headline/base_*.csv)
Hardware = gauge + FIPEX + host GPS drag, ground S_O cal 5%. Harsh truth (NRLMSISE-00 + calibrated driver errors).
Quiet / storm / recovery; accuracy = median bias, precision = median 1-sigma scatter of 30 s errors, MAE p50 (p90).
- DENSITY: accuracy -3.7 / -3.0 / -4.1%; precision 1.6 / 2.2 / 2.1%; MAE 5.6 / 5.8 / 6.7% (p90 12.5 / 13.1 / 14.1%);
  model 15.3 / 23.0 / 14.9%. => meets 20% accuracy / 10% precision / 30 s at the median AND at p90; 2.2-4.0x better
  than the model (4.0x in the storm).
- O: MAE 5.7 / 11.2 / 9.7% (p90 14.4 / 29.4 / 23.5%); model 14.2 / 17.2 / 13.9% => 1.4-2.5x better at the median.
- N2: MAE 13.8 / 17.3 / 19.0% (p90 27 / 43 / 36%); model 20.4 / 29.5 / 19.3% => 1.5x / 1.7x better quiet / storm;
  RECOVERY TIES THE MODEL (19.0 vs 19.3). N2 bias -13 / +3 / -15%. Say so; Phase 2 leak fixes it (leak: 14.4%).
- Robustness across truths (density MAE): driver-error 5.1 / 5.6 / 6.2%; NRLMSISE-00 5.4 / 5.7 / 6.2%; identical twin
  4.7 / 5.0 / 5.4%. => the result does not depend on which truth.
- C9 optimistic sensor values (FIPEX 1%/day, gauge 0.5%/day, C_D 5%; ASSUMPTION, not vendor): density 3.7 / 3.8 /
  3.9%; O 5.1 / 7.6 / 8.4%; N2 12.6 / 12.2 / 14.3%.
- Ablation (no leak): gauge + drag without FIPEX: density 6.0 / 6.4 / 6.7%, O 9.0 / 14.4 / 11.7%, N2 18.2 / 16.0 /
  15.5%. => FIPEX's contribution is O (quiet 9.0 -> 5.7%, storm 14.4 -> 11.2%) and quiet N2 (18.2 -> 13.8%);
  HONEST: storm/recovery N2 is slightly BETTER without FIPEX (16.0 / 15.5 vs 17.3 / 19.0) - the FIPEX gain tail
  leaks into N2. Density barely depends on FIPEX. Drag alone ~ model (harsh_drag_only 13.6 / 17.0 / 15.3%).
- NEES p50 5.8, p90 78.5; tail from gap_He (p90 78; He not a product) and o_gain (p90 10). Without FIPEX NEES p90 5.5.
- Wording: "On an independent, storm-calibrated truth, the baseline suite measures density to 5.6-6.7% (median;
  13-14% at the 90th percentile) every 30 s, 2-4x better than the operational model, and atomic oxygen 1.4-2.5x
  better; with the Phase 2 calibrated leak, density reaches 3-5%."

## HEADLINE RESULTS - WITH LEAK = PHASE 2 CONFIGURATION (freeze-v1, 2000 runs, Colab Nov 11; out/headline/*.csv)
!! [AUDIT CRIT] These are the WITH-LEAK cases, NOT the baseline. Baseline = base_* (running on Colab Nov 11).
!! Quote these only as "with the Phase 2 leak". Ratios corrected: density 3.2-6.4x, O 1.3-2.5x, N2 1.35-2.0x.
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

## HELD-OUT REAL-DATA VALIDATION (freeze-v1 + 3 generic fixes, Nov 11; scripts/de2_replay.py, 200 runs) - quotable
Baseline hardware (gauge + FIPEX + drag, no leak), prior = forecast/real-driver MSIS 2.1. MAE p50, model -> ours.
- GRACE-FO May 2024 superstorm (TOLEOS v0003 accelerometer density, 473-507 km): density quiet 48.6 -> 15.7%,
  storm 46.9 -> 14.3%, recovery 82.5 -> 13.3%. Error is almost all BIAS (+13-16%); scatter is small => the
  remaining error is one absolute-calibration number, removable by commissioning cross-calibration against an
  accelerometer mission (cal/val plan) or the Phase 2 leak. With leak: 5.4 / 5.3 / 7.5%. Meets the 20% benchmark
  without any external calibration. (GRACE-FO O/N2 "truth" is MSIS-scaled, so only density is a real test there.)
  [AUDIT] Caveat: accelerometer-density datasets themselves carry calibration spreads comparable to our bias, so
  "removable" means "reducible to the reference's own absolute level". Save the replay outputs to out/ as evidence.
  Citation: ESA Swarm DISC TOLEOS GF_OPER_DNS1ACC_2_ v0003 (processing: Siemes et al. 2023, JSWSC 13:16,
  doi:10.1051/swsc/2023014) + access date; v0003 = that processing UNVERIFIED.
- DE-2 NACS 1982-83 (real in-situ density + composition, elliptical 280-450 km, NACS absolute cal ~25%):
  DENSITY better than the model on ALL 12 test days: Sep 1982 (8 days incl. storm) 7.0/6.4/11.2/13.4/39.6/39.8/
  39.3/21.8 -> 5.4/5.2/5.7/6.4/10.8/8.2/6.8/7.8%; Mar 1982 20.3/23.6 -> 6.9/6.0%; Feb 1983 11.3/16.4 -> 6.9/11.1%.
  Storm days: 4-6x better.
- DE-2 COMPOSITION: mixed. O better on 8/12 days (Sep storm days 5-7: 36.9/34.8/26.3 -> 14.8/16.8/19.2%), N2
  better on 7/12 (Sep storm 88/83/171 -> 39/39/136%); worse: O on Sep d1-2, d8, Feb d2; N2 on Sep d1-2, d8, Mar. Systematic split: our O biased LOW (-7 to -24%), N2 HIGH, density right => the
  gauge's O/N2 partition (S_O) disagrees with NACS's own calibration; that size is inside NACS's ~25% absolute
  uncertainty, so DE-2 cannot settle it. Claim: "density validated; composition improved during the storm, limited
  elsewhere by the reference's own calibration". Do NOT claim composition validated on DE-2.
- ERROR BARS on real data: NEES p50 18 (GRACE-FO), 23-79 (DE-2) => filter overconfident on real data beyond the
  OSSE calibration factors; Phase 1 task: real-data error-bar calibration (state it, don't hide it).
- FIXES applied after first test run (generic, disclosed in one clause; register detail here): (1) simulation truth
  summed the C_D O-term over uncovered steps (sparse DE-2 windows only) -> exploded Sep 1982 after day 4; (2) FIPEX
  prediction lacked the altitude-slope term (inconsistent with the gauge on non-circular orbits); (3) drag update
  now gated like the other sensors. Circular-orbit OSSE results unchanged (100-run check, 4 decimals). Fix (2)
  costs a little on GRACE-FO (baseline was 15/12/12 -> now 15.7/14.3/13.3; leak 5.2/4.2/5.5 -> 5.4/5.3/7.5); kept
  because it is physically correct. Proposal clause: "a simulation bookkeeping error on sparse-coverage windows
  was fixed; circular-orbit results unchanged."

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
- [AUDIT FIX] Error bars: filter is overconfident; product calibration factors x2.0 (density) / x2.8 (O) / x3.4 (N2)
  measured on the OSSE; on real data NEES 18-79 => still overconfident; real-data error-bar calibration = Phase 1.
  (Old "z ~1 honest" line deleted.) The chi-square false-alarm match has no saved output file: cite only if re-run.
- Root cause of residual overconfidence (labelled HYPOTHESIS): unmodelled within-orbit (latitude/local-time) structure
  of model error; Phase 2 adds latitude-dependent error states. Drift was tested and ruled out as the cause.
- S_O handled by Schmidt consider analysis (Schmidt 1966; Bierman 1977) or ground-anchored estimation.

## Architecture / design choices (for the design-rationale table)
- 18-state Gauss-Markov EKF (14 active: N2 local-time harmonics off) incl. per-gas altitude slopes: per-gas model gaps (random walk, prior 20% from published error), common + per-gas AR(1)
  wiggles, gauge gain, FIPEX gain, C_D bias, S_O; ram-chamber gauge model n_c = n V cos(theta) sqrt(2 pi m / k T_c)
  (Bird 1994; confirmed by Grabe et al. 2010); Joseph-form updates; NIS gate 15.1; per-orbit drag.
- TESTED AND REJECTED (say so, with reason): adaptive/Kp-scheduled Q (bounded by an oracle test: no recovery gain);
  N2 local-time harmonics (worsened N2 on 2 of 3 truths: weak N2 leverage); in-flight S_O estimation WITHOUT a ground
  anchor (S_O and the model's O/N2 error are indistinguishable: identifiability algebra); dual-frequency drag without
  physics C_D in the filter (NEES 2.0).
- Twin-derived priors were replaced by literature priors after the first fraternal test (model gap 5% -> 20%): shows
  the method was stress-tested, not tuned to look good.

## Calibration / validation plan (Performance scores this)
[AUDIT FIX: rewritten for the NO-LEAK baseline]
- Ground (Phase 1): gauge N2/Ar/He calibration; atomic-O beam calibration of S_O to <=5% (required; INFICON has no
  AO data) or the same-beam gauge + FIPEX test fixing the S_O/f ratio (beam flux error cancels; algebra findings doc
  section M); pre-conditioning to O exposure (Cross et al. 1995); FIPEX gain/drift characterisation.
- Commissioning: >= 2 weeks; discard ~30 min after each gauge power-on (INFICON clean-up transient); shutter/wake zero
  checks (L8); cross-calibration against an accelerometer-density mission (GRACE-FO/Swarm conjunctions) to set the
  absolute level; host yaw manoeuvres to calibrate C_D accommodation (March et al. 2021; OCC allows host manoeuvres).
- In flight: gauge gain anchored by per-orbit drag + ground S_O; FIPEX cross-checked against gauge every 30 s and
  drag every orbit; S_O and C_D tracked as states.
- Phase 2: calibrated argon-leak gauge calibrator (see HARDWARE section) -> density ~5%.
- Validation: OSSE truth ladder; DE-2 replay; GRACE-FO held-out storm; Swarm/GRACE-FO conjunctions in flight.

## Requirements to state (FINAL Phase A, out/phase_a3/A1-A6.csv, 500 runs, harsh truth, frozen architecture
## WITH leak = register default; no-leak baseline row: density 5.2 / 5.8 / 6.8%). Density / O / N2 MAE p50, q/s/r.
Baseline (A1, 2000 runs): density 3.2/3.6/4.7, O 5.6/9.8/10.6, N2 10.3/15.5/14.4.
!! A1 (drag/C_D), A2 (S_O), A4 (gauge drift/noise) DO NOT transfer to the no-leak baseline (the leak pins the
!! gauge gain; without it C_D + S_O are the absolute anchor). Rerun queued: phase_a.py A1,A2,A4 --noleak ->
!! out/phase_a_noleak. Until then do NOT state "C_D insensitive" / "single-frequency GPS is enough" for baseline.
!! A3 (FIPEX), A6 (gas factors), outages transfer (composition is FIPEX-driven).
- S_O ground calibration DRIVES the product: 3% -> density 2.9/3.1/3.6; 5% (baseline) 3.2/3.6/4.7; 10% ->
  4.5/5.1/7.7, O 6.9/12.1/14.0; uncalibrated (16% bracket, consider) 5.7/5.4/5.9 but N2 recovery 16.5. Filter fooled
  (truth 10%, assumes 5%): 4.0/4.3/5.5. => REQUIREMENT: S_O known to <=5% by ground atomic-O calibration.
  INFICON (Nov 11 email): no atomic-O data for MAG084; expects N2-like behaviour; O-resistant materials => the S_O
  ground calibration is a required Phase 1 test (AO beam facility), not optional.
- FIPEX drift drives O: 0 -> O storm 6.6%; 1%/day 6.5%; 3%/day (baseline) 9.8%; 6%/day 12.5%. FIPEX gain prior
  5% -> quiet O 3.4% (vs 5.6%). => REQUIREMENT: FIPEX drift <=3%/day (goal 1%/day), unit gain known to <=12%.
- Gauge drift: 0.5%/day -> density storm 3.2%, N2 13.5%; 2%/day (baseline) 3.6 / 15.5; 5%/day 5.4 / 18.5.
  INFICON: "not seen major drift" long term (lab data, not statistical) => baseline 2%/day is conservative.
- Gauge noise 0.5-5% per 30 s: density 3.0-3.9% (insensitive). INFICON: no fluctuation at 1e-7 mbar beyond
  rounding (3-digit output) => our 1% is conservative.
- Drag: per-orbit noise 5-25% and C_D prior 5-25% all give density 2.8-3.7% storm (insensitive once gauge is
  calibrated); dual-frequency GPS no gain; daily-only drag fallback 3.6/3.6/4.9 => host needs only single-frequency
  GPS orbits.
- Outages (gauge 30 min / 6 h, FIPEX 1 h / 6 h): no material change.
- Gas factors (filter fooled): He +-25%, N +-10%: no change; all non-O +-5%: N2 quiet 9.3-14.2%. INFICON factors
  (p_eff = C x display): He C=5.9 -> sensitivity 0.17 (ours 0.18, inside the +-25% sweep); Ar C=0.8 -> 1.25 (ours
  1.29); O2 = air (ours 1.01). => our factors vendor-consistent.
- Gauge gain prior: INFICON says 30% is the MAXIMUM envelope (all sources, not per-unit calibrated); we used 30%
  as 1-sigma => conservative by ~3x; gain is estimated in flight anyway.

## FIPEX data sheet (Univ. Stuttgart IRS / HEFDiG, single-sensor, received Nov 11 2026)
- Sensor heated to ~1000 K; input 12-48 V; power < 4 W sensor (VLEO steady state) + < 2 W electronics = < 6 W total
  (more during heat-up; sequenceable).
- Mass: sensor head with holder 70 x 31 x 14 mm, ~20 g; electronics PCB 90 x 90 x 25 mm, ~70 g (~90 g total).
- Data: 12-byte word at up to 100 Hz (adjustable) = 1.2 kB/s max; we need 1 per 30 s (averaged) -> tiny downlink.
- Interface: custom cable to electronics; RS485 to host (custom possible).
- NOT in the sheet: accuracy, drift, noise, atomic-O sensitivity -> our O_GAIN_SD 30% (IRS call Nov 9) and FIPEX
  drift 3%/day stay labelled ASSUMPTIONS; Phase A shows FIPEX drift drives O accuracy -> Phase 1 characterisation.

## Vendor facts for the proposal (INFICON MAG084 email Nov 11 2026; attachments = MAG084/VGC094 manual pages)
- Accuracy 30% of reading = max envelope; gauges not individually calibrated (population characteristic curve).
- Repeatability 5% short-term (pressure cycling); long-term no major drift observed (not statistical).
- Linear below 1e-5 mbar; continuous output, no jumps; analog output (CP300/PE300 boards) for fastest unfiltered
  signal; controller 100 Hz internal, 10 Hz display.
- Temperature: via thermal transpiration (sqrt(T)) + wall outgassing; no self-heating; ignition "clean-up"
  pressure transient after power-on => ops: discard first ~30 min after power-on (C7 analysis basis, AUDIT-corrected:
  sqrt(T) at 300 K = 1.7% per 10 K, so a +-20 K wall swing -> ~+-3.3% gain; inside the swept 5% gauge-noise case;
  thermal control holds the swing smaller).
- Pumping speed 0.01-0.1 L/s (N2), changes with wear => small vs ram-chamber orifice conductance (check with CAD).
- Stray magnetic field < 0.05 mT beyond ~4 cm (shielded, GEMINI design) => host magnetometer/torquer
  compatibility point.
- Price: 15% university discount; volume pricing on request.

## C7 stress (analysis, not simulated - decided Nov 11): wall temperature (+-3.3% for +-20 K via sqrt(T)), pointing
## (10 deg -> ~1.5% via cos), filter mis-tuning (Q choice tested on 2 truths) all sit inside the Phase A swept
## ranges of gauge noise/drift and the "filter fooled" cases; stated as analysis in the proposal.
- Host asks: single-frequency GPS (dual = upside), attitude knowledge, geometry model, optional yaw manoeuvres.

## Resource needs
- Data: 30 s raw averages ~35 kB/day; raw 1 Hz 0.35-0.7 MB/day; processed 46-81 kB/day (L11).
- Compute: EKF ~2.1 kFLOP / 30 s, ~22 us on an STM32H7; smoother and S_O on the ground.
- Contamination (OCC requires it): all-metal CF chamber, no polymers, 150 C bake, sealed until orbit, baffle with no
  view of blankets, >= 2 weeks commissioning (L8). Outgassing negligible at 300 km after ~1 day.
- MAG084 magnet dipole = hosting risk (mech team to measure; mitigation and excluded hosts).

## Known issues to name with mitigations (K1-K11, findings doc R1)
- S_O not measured for the MAG084 (bracket 0.51 cross-section to 0.71 full recombination; Laher & Gilmore 1990; Newton & Horowitz
  1969); recombination products; gauge nonlinearity and mode jumps; ignition delay (60 s at 1e-8 mbar); discharge
  pumping; same-beam relative only; wall temperature (1.7%/10 K) and pointing (1.5%/10 deg); background;
  no MAG084 drift data; FIPEX drift and n^0.35 response (Eberhart et al. 2019).

## In-flight drift/sensitivity tracking (answer to "what about drift / S_O / 1 year")
- Every headline number already includes, in the truth: FIPEX drift 3%/day one-sided, gauge drift 2%/day, gains
  +-30% unknown, S_O drawn per run (5% calibrated; 16% bracket in the uncalibrated case), C_D bias + drift + O-physics,
  per-orbit drag noise 15%, sensor outages, harsh model error. The filter tracks gauge gain (anchored by per-orbit
  drag + ground S_O in the no-leak baseline), FIPEX gain (cross-checked vs gauge each 30 s and drag each orbit), S_O
  and C_D as states.
- Wording (draft, AUDIT-fixed for no-leak): "Sensor gains are tracked in flight: the gauge gain is anchored by host
  drag every orbit and by the ground atomic-O calibration, and FIPEX is cross-checked against the gauge and drag.
  A 1-year simulation is planned (Phase 2); the Phase 2 leak adds a direct gauge re-anchor."
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
- One-year drift not yet simulated (planned Phase 2).
- [AUDIT] Unlabelled assumptions to label when used: INFICON 30% envelope read as ~3-sigma; C9 "best estimate" drift
  values (optimistic assumption, not vendor); GRACE-FO bias removable; O+N2 mass fraction; 22 us EKF timing;
  outgassing negligible after ~1 day; independent O error; FIPEX "<=12%" requirement (Phase A read-off, not vendor).
- [AUDIT] Unverified citations (verify or drop before use): Newton & Horowitz 1969, Schmidt 1966 pages, MKS gas
  factors page, NIST SRD 107, Grabe 2010, Bird 1994 section, Lowe & D'Amico 2026, Licata 2022 content, LADEE NMS
  calibration-gas heritage (NGIMS has a sealed noble-gas reservoir, not a valved leak). Full audit:
  docs/claims_audit_2026-11-11.md.
- Outlier handling assumes median-of-30 preprocessing.
