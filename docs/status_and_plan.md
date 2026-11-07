# OCC: where we are and what's next
Last updated Nov 5, 2026. Covers everything from the start of the OSSE work through the hardware planning, the software studies, and the full phase plan (section 8). The balloon launches are cancelled (parts arrived too late); the filter is tested on the ground on the NUCLEO-H753ZI instead.

## Dates
| Date | What |
|---|---|
| Done | Registration |
| Mon Nov 9, 8 am | Call with Uni Stuttgart IRS (Löhle, Fasoulas): reworked FIPEX + absolute atomic-O calibration |
| Soon | INFICON call (MAG084 numbers) |
| **Nov 11, 5 pm ET** | Phase 1 submission (written answers with word limits, a visual PDF of at most 5 pages, a video of at most 90 s) |
| Phase 2 (~4 months) | Engineering model plus ground testing. Trade studies and design rationale are worth 25 of 100 points |

No other internal timeline: the work goes as fast as it can be done correctly.

## 0. The submission packet (official sample form, re-read Nov 7)
- **13 text sections, ~3,250 words total:** Technology description 50, Capabilities 250, Technology overview 350, **Technology performance 350**, Projected cost and scalability 350, Technology development status 300, Resource needs and accommodation 300, Flight demonstration and integration 150, Solution development plan 250, Intellectual property 200, Other considerations (optional) 150, Project plan 200, Budget narrative 200. Plus team info, budget line items, insurance question, YouTube URL.
- **Visual PDF:** one file, ≤5 pages, ≤10 MB. "Photos, illustrations, schematics, charts, graphs." Only "brief labels and/or basic text descriptions", minimum 10 pt; must not carry text that circumvents word counts. **No Gantt charts, schedules or budgets.** Extra pages or unrelated content = ineligible. It is a figure document, not a paper.
- **Video:** YouTube, ≤90 s, captioned, public or unlisted, embedding on. "Do not simply read a slide deck."
- **URLs:** allowed in Technology development status ("cite test results or other evidence"); must not be password-protected; "judges are not required to read this content", used "for due diligence." So a public technical report (full OSSE, number register, sources) is the place for depth, but every claim the score depends on must stand in the form text and the PDF.
- **No references section or appendix upload.** Citations go inline, sparingly; the full list lives in the public report.
- **Proof of citizenship/permanent residency** is required from an individual winner; an organization needs a US location of business.

## 1. What OCC actually rewards
- **Benchmarks for in-situ density:** 20% accuracy, 10% precision, a reading every 30 s. These are "target floors, not fixed requirements": trading performance for big cost or scale gains "can still be highly competitive."
- **Relevance:**
  - **5** needs density **plus composition** over "a clearly identified and **extensive** altitude regime."
  - **Density only** tops out at 4.
  - **Drag or pressure as an indirect route** tops out at 3.
- **Composition** = "individual number density of major neutral species."
- **Performance** needs quantitative evidence, with uncertainty that is "characterized and realistic," plus a calibration and validation plan.
- **Hard rules:** hosted payload only; no interference with the host; at least 1 year of operation; buildable in 100+ units, far below today's $1M–$10M instruments. No published size, weight or power envelope, so we state our own assumptions.

## 2. Suite (tentative)
| Channel | Instrument | Role | Main unknowns |
|---|---|---|---|
| Density, fast | **INFICON MAG084** cold cathode gauge in a ram-facing chamber | Fast relative density; sets precision | Gas sensitivity factors, atomic-O sensitivity (S_O), drift, temperature coefficient, nonlinearity, pumping speed, ignition |
| Composition | **FIPEX** solid-electrolyte O sensor (originally TU Dresden; now Uni Stuttgart IRS, reworked with absolute atomic-O calibration) | O, and O+O₂ (so O₂ by subtraction) | Absolute accuracy, unit-to-unit spread, degradation, flux-to-density/angle, power, availability |
| Absolute anchor, slow | **Host GPS drag** | An independent total-mass check | Drag-coefficient uncertainty (15–25%), host area-to-mass ratio |
| Helium | none in baseline | — | Model-supplied, fleet multi-altitude inversion, or a mini mass spec on some units (roadmap) |

**The CCG, seen from software:**
- **It outputs** one number per sample: chamber pressure "as if the gas were N₂."
- **Error model:**
  - **Offset:** ±30% (datasheet "typical accuracy"; what it's made of is unknown, so ask INFICON). Per-unit lab calibration may shrink it.
  - **Jitter:** ±5% repeatability.
  - **Slow:** drift and temperature effect (unknown).
  - **Range and gaps:** valid from 1e-8 to 5e-3 mbar; possible startup gaps.
- **Turning that into mass density outside takes four steps:**
  1. Pressure → molecules, using the chamber wall temperature.
  2. Correct the "as if N₂" assumption, using composition and the gas factors.
  3. Chamber → outside air, using satellite speed and attitude.
  4. Molecules → mass, using composition.

**N₂ is inferred:**
- Gauge reading minus FIPEX's O and O₂ leaves N₂ plus a little He.
- **That inference is weak on quiet days.** N₂ is ~10% of the air at 300 km, so a 5% FIPEX error becomes a ~24% N₂ error, and a 10% S_O error becomes ~47%.
- **It's strong in storms,** when N₂ is large (~1% error).
- Drag adds a second, independent route to N₂.

**FIPEX facts:**
- **Heat:** it heats itself with a built-in heater regulated to a fixed temperature. Eberhart 2015 says about **500 °C**; the team's "1000 K" figure needs a source.
- **Size and power:** the QB50-era sensor unit is ~15 g, with heating under 1.6 W and ~2–2.5 W for the whole electronics (design-era estimates).
- **Heritage:** ~19 months outside the ISS, plus rockets and QB50.
- **Open question:** thermal isolation from the CCG and electronics.
- **Published calibration (Stuttgart IRS):** a microwave plasma of pure O₂ produces atomic O, which expands through a pinhole into a vacuum chamber; a mass spectrometer measures the resulting molecular beam as the reference (Eberhart et al. 2015, AMT 8:3701; 2019, AMT 12:2445).
- **FIPEX measures flux, not density.** Converting flux to density needs a flow/aerodynamic correction (the 2019 paper computed it by numerical simulation).
- **WADIS-2 (2019) issues:** the data were unstable on the way up; electrode orientation mattered; individually calibrated sensors sometimes disagreed; the uncertainty of the flow correction was never given as a number. The "reworked absolute calibration" likely targets these; confirm on Nov 9.
- **Newer work:** faster response (eFIPEX, more porous electrode, ~2024). The SOURCE CubeSat (Stuttgart) carries 2 FIPEX sensors and was scheduled for 2025; whether it launched is unconfirmed.
- **Effect on our design:** the architecture doesn't change; only the FIPEX gain prior tightens if the calibration holds up. FIPEX O then becomes the anchor, which helps separate S_O from the CCG gain. The in-flight gain estimate stays as a safeguard against drift.

**RGA (Extorr XT100):** not for the payload. It's ~4 kg, up to ~60 W supply, and has no space heritage. Use it on the ground as the vacuum-chamber calibration reference (CCG gas factors, chamber composition).

## 3. Altitude and gases
- **The mix (MSIS):**
  - O and N₂ dominate 250–450 km.
  - He becomes large in winter at solar minimum (34% at 400 km, 72% at 500 km).
  - O₂ reaches 7–16% only in high-latitude storms.
  - High-latitude storms flip the mix (N₂ from 7% to 61% at 300 km).
- **Floor:** set by hosts (~250–380 km). **Ceiling:** set by the CCG's 1e-6 Pa floor. With a ram chamber, roughly ~500 km at solar minimum and ~650–700 km at solar maximum.
- **Draft claims:** density + O/N₂ at ~250–450 km; density only to ~500 km (solar min) and ~650 km (solar max); 700–800 km out of reach.
- **Our real chamber pressure range:** ~1e-8 to 3e-5 mbar.

## 4. Simulation so far, and its honest limits
| Result | Caveat |
|---|---|
| Fused storm density error ~3.4% (100k runs in simt) vs 26–36% for the model alone | Scales with the calibration errors I assumed (×0.25 gives 1.8%, ×2 gives 8.8%). The 26% depends on how badly the baseline's inputs were degraded (range 4–36%). Truth and baseline are both MSIS |
| Gauge + drag can't get composition; gauge + O sensor can | Fails at 450 km because of helium |
| Composition error is driven by sensor-gain drift in flight | Drops only when all three gains are fixed |
| Gauge-calibration sweep: fused ~3–4% up to a 40% gauge error | Likely anchored by drag's ±7% (optimistic). Untested |
| NIS ≈ 1, NEES 0.5 | Consistency of the code, not realism |

**Why:** the overall density level can't be told apart from the sensor gains, so absolute accuracy comes from the best-calibrated sensor. **Drift stability matters more than absolute accuracy.**

## 5. Lessons from Lowe & D'Amico (2026): use as a cross-check, not a template
- **What they did:** pure simulation; GPS-only UKF; estimates β (density × drag coefficient × area/mass), day-averaged. Error 16 / 9 / 5 / 6% (low / mean / high / storm) vs 58 / 39 / 13 / 29% for Harris-Priester with predicted flux.
- **That's not density error:** their drag coefficient was fixed and known.
- **What we take:**
  1. Realistic day-averaged drag with their error levels **plus** a separate drag-coefficient uncertainty
  2. NOAA forecasts as the honest baseline, on real dates
  3. Harris-Priester tables (Appendix B: exponent 4, 30° lag)
  4. The storm tuning trade
  5. Bias and scatter reported separately, plus **RMS percent error**
  6. **Effective density** (orbit/day-averaged) reported alongside local
  7. Test a **joint vs two-stage** filter: joint estimation cut their relative error from ±65% to ±8%
  8. His Table 3 as starting tuning values
  9. Host attitude changes: an attitude timeline plus extra process noise at changes
  10. **EKF vs UKF**
- **His 30 s update rate** was chosen for low onboard compute (TanDEM-X heritage).
- **Fleet:** a 2→9 satellite swarm didn't improve his absolute drag error, so keep fleet claims honest.
- **Positioning:** GPS-only drag gives day-averaged β with no composition. We add 30 s local density + composition, with drag as the anchor.

## 6. Corrections (don't repeat the old versions)
- MAG084 accuracy is 30% (N₂), not 4%. "Indoors only," +5 to +80 °C, NdFeB magnet, ≤3.3 kV.
- MIGSI is ~20% at 1 Hz, not "<10% at 100 Hz."
- The 58% LLITED figure is unverified (only from our copy of the paper).
- No commercial CCG has flown on a small satellite in orbit (sounding rockets only). No one has measured a gauge's atomic-O sensitivity.
- FIPEX runs at ~500 °C (per Eberhart 2015), not necessarily 1000 K.

## 7. Open problems
- **a) S_O (atomic-O sensitivity):**
  - **Effect:** a constant offset when composition is steady, but a ~14% apparent gain swing in storms (worked example).
  - **This is a software problem.** Estimate it in flight (it's shared by every unit's chamber, so pool it across the fleet), check separability first, or carry it as known uncertainty (a "consider" filter).
  - **Also:** sweep it to derive a requirement; the chamber could be designed for full recombination of O into O₂.
- **b) Storm lag and bias:** risk sits in the slow states. Candidate fixes: adaptive process noise (NIS- or Kp-driven), a rate state, IMM, an RTS smoother on the ground. Judge by storm-window bias.
- **c) Helium:** limit the claim to ~400–450 km. Fleet inversion only with simulation evidence. A mixed fleet with a mini mass spec is a roadmap item.
- **d) Fleet:** the per-unit claim stands alone. The fleet adds coverage, cross-calibration, S_O pooling and helium.
- **e) Hosts:** 2–3 reference hosts. Find the area-to-mass ratio below which the drag anchor weakens.
- **f) High voltage:** no HV hardware before submission, so pivot to evidence:
  - **Heritage:** CCGs on Explorer 32 and on sounding rockets (Lehmacher 2013, 2026); kV detectors and supplies on small-satellite instruments.
  - **Design rules:** HV off through launch and outgassing, a pressure interlock, potting, current limiting.
  - **Phase 2 tests:** vacuum pump-down corona test + thermal-vacuum.
  - **Risk register entry.**

## 8. Software and simulation plan (complete, in order)
**Rules:**
- Everything is built as simt scenarios in this repo (`osse/`). The reference is `simt/examples/occ.py`: it is already a validated port of `fusion_osse.py` (medians inside the original's 95% confidence intervals, `validate_occ.py`), and later simt changes reproduce it bit for bit. Every restructuring step must reproduce it exactly with the same seed and settings; every deliberate model change is reported as a change, with its effect.
- Every number is a setting with **separate truth and filter values**, tagged with exactly one kind (the tag answers "why should anyone believe this number?"):
  - **sourced** (datasheet, paper, constant): the citation
  - **vendor** (INFICON, Stuttgart): the email or recap; swept until it arrives
  - **research**: literature exists; find it and document it
  - **sweep**: truly unknown; no value is picked; the output is "must be better than X"
  - **choice**: our decision (orbit, host, run setup, tuning); the reasoning
  - **old**: inherited from the reference code with no source; must be replaced (says what it becomes)
- **No silent constants.** Sweep ranges only need to bracket the break point. Anything held fixed during a sweep uses its S/V value, or is run at both ends of its range if still unknown.
- **Datasheet specs without a stated meaning** (30% accuracy, 5% repeatability: 1σ or a bound?) are run both ways until the vendor answers; 1σ is the conservative reading.
- **OCC does not define accuracy and precision statistically.** We state ours: accuracy = bias, precision = 1σ scatter at 30 s, plus median and P90.
- **Every filter design choice** goes in a design-rationale table: the choice, the reason, the citation or derivation.
- **Report everything** as accuracy (bias), precision (scatter), resolution, RMS percent error and effective density, quiet vs storm, median + P90.
- **Log every run** with its assumptions.
- Working style: Claude writes small pieces and explains them; you place them, run them, and understand them.

### Phase 0: simt as a package (done)
- Package, tests, Kalman upgrades (`kf_update_scalar` with gaps, gating, Joseph form, NIS), `RollingMean`, `ar1_step`, time-series recording, `RunningStats`, bootstrap and paired comparisons, `grid` / `one_at_a_time` / `sweep` with resume. Pushed.
- On the working machine: `pip install -e ../simt` in this repo's venv and check `import simt`.
- Note: never `push` a NaN into `RollingMean` (it stays poisoned until it leaves the window); mask gaps first.

### Phase 1: the foundation (Study #1)
Restructure `simt/examples/occ.py` into the `osse/` package, reproduce it exactly, then replace every untagged number.
1. **`osse/atmosphere.py`:** the storm drivers (synthetic + real indices later), orbits (any altitude and inclination), MSIS truth and prior tables (cached), and the air speed relative to the rotating atmosphere.
2. **`osse/sensors.py`:** the CCG, FIPEX and drag measurement models. Each one has a truth version (makes fake readings) and a filter version (predicted reading + sensitivities).
3. **`osse/filter.py`:** the EKF pieces (predict, scalar update, optional states).
4. **`osse/metrics.py`:** accuracy / precision / resolution, composition errors, RMS percent error, effective density, NIS/NEES.
5. **`osse/scenario.py`:** the simt `Scenario` (`sample`, `init_state`, `step`, `score`).
6. **`osse/params.py`:** the number register. Every number in one place, tagged S/V/R/W/D/L with its source; V/W numbers left empty, each with its sweep range.
7. **Validation:** same settings and seed → bit-identical numbers to `simt/examples/occ.py`.
8. **Then replace the untagged numbers** (each is a reported model change):
   - gas factors (V; fallback R: published relative sensitivities)
   - atomic-O factor (W: the S_O sweep)
   - the hand-typed storm ap profile and F10.7 (R: real GFZ Kp/ap and F10.7)
   - the invented forecast lag and cap (R: the NOAA SWPC forecast archive; until then, labeled scenarios only)
   - CCG gain spread and drift (S: datasheet 30%, both readings; V: per-unit calibration and drift; W meanwhile)
   - FIPEX gain spread and drift (V: Nov 9; fallback R: WADIS-2 Table A1)
   - C_D error (R: needs a citation)
   - sensor noise (V; drag S: Lowe & D'Amico 2026)
   - the truth's AR(1) small-scale structure, 5%/600 s and 2%/900 s (R: measured density variability)
   - filter priors, Q and R (D: NIS/NEES consistency + model-vs-truth statistics)
   - drag: orbit-mean becomes day-averaged (S: Lowe); remove the `h_orbit ... * 0` leftover
9. **Structural fixes:**
   - Truth and prior are both MSIS (identical twin). Use a different model for truth (fraternal twin; JB2008 or DTM2020, availability to check), then real data in C3.
   - Explain the two unexplained results before the proposal: fixing only the O-gain drift raises density error to ~5%, and the ±2% sweep behaves oddly.

### Phase A: margin sweeps (Study #6, part 1)
Find which unknowns matter and how much margin we have.
- **Every sweep:** 10k runs per value; 250/300 km (plus 450 km where relevant); two filter versions, **"filter knows"** vs **"filter fooled,"** compared with `paired_bootstrap_ci` on the same seeds.
- **A0, observability first:** condition numbers for S_O vs gain, N₂ vs He, overall scale vs gains. This proves the filter can separate them before anything is swept.
- **A1, drag realism:** drag becomes day-averaged with a slowly varying estimation error (Lowe-like 5/9/16%) **plus** a drag-coefficient error (7/15/25%), with gauge accuracy 5% vs 30%. **Question:** does "a bad gauge is fine when fused" survive realistic drag?
- **A2, S_O:** truth vs filter mismatch of 0–40%. Two filters: S_O fixed vs S_O estimated in flight. Do the separability check first. **Question:** how bad is our biggest unknown, and can software fix it?
- **A3, spec sweeps (one at a time):**
  - CCG: drift, noise, gain (per-unit calibration quality)
  - FIPEX: absolute accuracy (2–30%), **unit-to-unit spread** (matters for the fleet), degradation, noise, warm-up gaps, flux-to-density/angle, gold channel only vs gold + platinum
  - **Temperature coefficient** (the 0.11%/°C in the inputs sheet has no source: V from INFICON, W meanwhile) with the orbital temperature cycle
  - Gas-factor uncertainty, nonlinearity
  - Pointing error, HV stability, gas mix

  Output: a ranking chart + "must be better than X" for each.
- **Phase A output:** a requirements list for the team, INFICON and Stuttgart, plus robustness lines for the proposal. When a vendor number arrives, read off the result at that value and do one confirming run.

### Phase M: mechanical / gas-flow simulations (Studies #9, #10)
Its outputs feed the sensor models in Phase B.
- **M1, test-particle Monte Carlo (TPMC) of the 2U housing:**
  - **How:** fire millions of virtual molecules (free-molecular flow; the ram beam at 7.7 km/s plus thermal spread, gas-dependent) at a simple payload/host geometry.
  - **Outputs:**
    - flux into each instrument vs **pointing angle** → the pointing tolerance
    - **shadowing/wake** between the CCG, FIPEX and host structures → placement rules
    - **baffle/orifice response** (inlet area, baffle length/diameter)
    - the CCG's **chamber-to-outside conversion** vs angle, with molecules bouncing inside the chamber
  - **Cross-check** against the drag-coefficient Response Surface toolkit / VLEO-DSMC.
- **M2, 2U placement optimizer:**
  - **Hard limits:** field at the magnetometer ≤ 100 nT, HV keep-out ≥ 65 mm, temperature limits (MAG084 ≥ 5 °C, FIPEX mount ≤ 120 °C), center-of-mass offset ≤ 2 cm.
  - **Then a weighted score:** field 30 / HV 25 / heater 20 / strap 15 / CoM 10.
  - **Inputs:** the mechanical sheet (sizes, masses, conductances, magnet field vs distance).

### Phase B: complete sensor models + filter (Study #7)
- **CCG:** the full chain (chamber pressure → molecules → gas correction → outside air → mass), the 1e-8 mbar floor, nonlinearity, ignition gaps, temperature drift, the angle response from M1.
- **FIPEX:** gold (O) + platinum (O+O₂) channels, angle response, degradation, warm-up gaps.
- **Drag:** day-averaged; host area-to-mass; attitude changes (timeline + extra process noise).
- **Filter:**
  - an S_O state (if separable), an optional He state, O₂ via FIPEX
  - gap and outlier handling
  - storm response (adaptive Q from NIS or Kp, a rate state)
  - drift-trade tuning
  - EKF vs UKF; joint vs two-stage drag
- **Self-calibration demo (#7):** plots of the filter learning the 30% gauge offset and S_O over time.

### Phase C: realism + validation (Studies #2, #3, #4, #5, #8)
- **C1, the honest baseline (#3):** the real May 2024 storm. Truth uses measured indices; the operators' model uses **NOAA's actual forecasts.**
- **C2, a different model in the filter:** Harris-Priester for density + MSIS on forecast inputs for the per-gas prior.
- **C3, real-data truth (#4):** fly along CHAMP / GRACE-FO / Swarm tracks with TU Delft's measured densities (composition truth still from a model).
- **C4, real numbers in:** INFICON, Stuttgart, thermal team. Unknowns stay as swept ranges.
- **C5, the headline (#2):** fused density + O + N₂ vs the 20/10/30 benchmark, quiet vs storm, at 250/300 km. **The main figure.**
- **C6, the coverage grid (#5):** 200–500 km in 25 km steps × solar min/medium/max × quiet/storm × 51.6° and ~97°, with and without He. Output: the **declared altitude ranges** for density and for composition.
- **C7, uncertainty validation (#8):** NIS/NEES, error-bar coverage, stress tests (mis-tuning, gaps, outliers).
- **C8, the full sensitivity ranking (#6, part 2):** all-at-once global sensitivity (Morris → Sobol) confirming the Phase A ranking.

### Phase D: onboard compute (Study #11)
- Operation and memory count; float32 vs float64 stability (Joseph-form or UD/square-root if needed).
- C++ port of the filter core, matched against Python.
- Measured µs and kB on the H753 (300 MHz-equivalent) + a Vorago profile (100 MHz, float32, 64 KB).
- **Ground hardware-in-the-loop test (replaces the balloon):** stream simulated sensor readings from the OSSE into the H753 over UART, run the C++ filter in real time, and compare its outputs and timing against Python on the same inputs.
- **Deliverable:** "X kB, Y µs/update, float32 within Z% of float64; fits a SAMV71Q21RT with margin."

### Phase F: fleet (Study #13)
- N hosts across altitudes and inclinations.
- **What it shows:** storm coverage, cross-calibration between units, S_O pooled across the fleet, multi-altitude helium inversion.
- **Kept as extra value:** the per-unit claim must stand on its own.

### Phase G: writing + figures (Studies #14, #15)
- **#14, calibration & validation plan:** vacuum chamber + **RGA as the composition reference** (S_O measurement, outgassing/thermal-vacuum), the atomic-O source (Stuttgart IRS, if they agree to test our CCG), the flight validation approach.
- **Number register appendix:** every number with its S/V/R/W/D/L tag and source.
- **#15, software architecture:** onboard vs ground, data products, latency, diagram.
- **Figures and text** for the PDF, the written sections and the video, mapped to the rubric. Results log in the workbook.

### Dependency order
Phase 0 (done) → Phase 1 → A0 → A → (M runs alongside) → B → C → final figures. D (including the ground hardware test) starts once the filter is stable. F after C. G throughout.

### Variable priority (impact × obtainability)
1. Drag-coefficient uncertainty (literature + hosts)
2. S_O (no data: sweep and estimate)
3. CCG drift (INFICON)
4. FIPEX absolute accuracy, unit-to-unit spread and degradation (WADIS-2 papers / Stuttgart, Nov 9)
5. Per-unit calibration accuracy (INFICON)
6. Gas factors for O₂, He and atomic O (INFICON)
7. Temperature coefficient + gauge temperature swing (INFICON + thermal team)
8. Host area/mass and attitude knowledge
9. Pumping speed + chamber design
10. FIPEX pointing response
11. Nonlinearity
12. Startup gaps

Sweeps come first. Real numbers drop in at C4.

### Software studies list (sent to the lead)
1. Simulation framework
2. Density & composition performance (main figure)
3. Storm comparison vs the operational model
4. Real-data validation
5. Altitude & solar coverage
6. Sensitivity & requirements
7. In-flight self-calibration
8. Uncertainty validation
9. Gas-flow / pointing study (2U housing)
10. 2U placement optimizer
11. Onboard compute (now includes the ground hardware-in-the-loop test on the H753)
12. ~~Balloon flight software demo~~ (cancelled; tell the lead)
13. Fleet study
14. Calibration & validation plan (written)
15. Software architecture (written)

## 9. Compute and hardware
- **Onboard filtering isn't required by OCC.** The baseline is ground processing, with an optional light onboard filter (Harris-Priester + correction). Compute is tiny: a few kB and a few thousand math operations per 30 s. **Single-precision stability is the real constraint.**
- **Boards:**
  - **NUCLEO-H753ZI:** Cortex-M7, 480 MHz, double-precision FPU, 1 MB RAM. The flight-class stand-in; clock it to 300 MHz or scale timings by ~1.6×.
  - **NUCLEO-F446RE:** M4F, 180 MHz, single-precision only, 128 KB. Optional worst case.
- **Flight target:** SAMV71Q21RT (rad-tolerant M7, pin-compatible with the commercial SAMV71). **Conservative:** Vorago VA41630 (rad-hard M4, 100 MHz, single precision, 64 KB). **FPGA:** data handling only.

## 10. Balloon: cancelled
Parts arrived too late for either launch. It added little to the proposal: the density measurement itself, atomic O and radiation couldn't be tested on a balloon anyway (10 mbar is far above the CCG's range). The ground hardware test on the H753 (Phase D) covers the real-time filter claim.

## 11. Questions out
- **INFICON** (priority order: 1–3 matter most for the proposal):
  1. Gas factors for O₂ and He, plus any atomic-O data and effects of oxygen exposure
  2. What makes up the 30%; **1σ or a bound?**; the accuracy after per-unit calibration
  3. Drift per month or year; the time span of the 5% repeatability
  4. Temperature coefficient (% per °C), head vs electronics, warm-up
  5. Nonlinearity from 1e-8 to 1e-4 mbar (and whether the controller corrects it)
  6. Pumping speed for N₂, O₂ and He
  7. Noise and output rate at low pressure; ignition time

  For each answer: measured, typical, or estimated? Can they send it in writing?
- **Stuttgart IRS, Nov 9** (priority order):
  1. What changed from the WADIS-2 calibration method; the absolute O uncertainty and its range
  2. Unit-to-unit consistency (individually calibrated sensors disagreed on WADIS-2)
  3. Did SOURCE launch; orbital data; drift over time and lifetime in atomic O
  4. Converting flux to density; angle response
  5. Is the new design eFIPEX; response time, noise, heater power, warm-up
  6. Gold/platinum channels (O vs O+O₂)
  7. **Can their atomic-O facility test our CCG?** (would measure S_O)
  8. Supply of 100+ units, rough cost, letter of support or collaboration

  Fallback for anything not shared: a labeled assumption, a sweep, and a Phase 2 test; their 2019 paper's calibration uncertainty is the citable starting point.

## 12. People
- **Shane Lowe** (snlowe@stanford.edu)
- **Uni Stuttgart IRS: Stefan Löhle, Stefanos Fasoulas** (FIPEX, now leading it; call Nov 9). TU Dresden no longer works on it.
- **CU Boulder SWARM-EX** (Pilinski, Thayer)
- **INFICON** (contact established)
- **LLITED/MIGSI team** (optional)

## 13. Where things live
- `fusion_osse.py`, `verify.py`: reference simulation and tests.
- `simt/examples/occ.py`, `validate_occ.py`, `sweep_occ.py`: fast GPU version.
- `reports/OCC sensor suite research.md` + `research_notes/OCC sensor suite research/`: deep research.
- Datasheets in Downloads: MAG084 (tiba71e1-a), STM32H753xI (DS12117), STM32F446xC/E (DS10693), Nucleo data briefs. Lowe paper PDF.
