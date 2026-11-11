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

## Caveats that must appear
- All OSSE numbers: 300 km, 51.6 deg, one storm (May 2024), 5 days, high solar activity.
- One-year drift not yet simulated (planned Stage 7).
- Outlier handling assumes median-of-30 preprocessing.
