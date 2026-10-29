# OCC: where we are and what's next
Last updated Oct 18, 2026. Covers everything from the start of the OSSE work through the hardware and balloon planning.

## Dates
| Date | What |
|---|---|
| Done | Registration |
| Optional | Launch 1: 30k ft test (HAB-150). Rehearsal for the software pipeline |
| ~Nov 1–4 | **Launch 2: 100k ft (HAB-1500).** The software target |
| **Nov 11, 5 pm ET** | Phase 1 submission (written answers with word limits, a visual PDF of at most 5 pages, a video of at most 90 s) |
| Phase 2 (~4 months) | Engineering model plus ground testing. Trade studies and design rationale are worth 25 of 100 points |

No other internal timeline: the work goes as fast as it can be done correctly.

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
| Composition | **FIPEX** (TU Dresden) solid-electrolyte O sensor | O, and O+O₂ (so O₂ by subtraction) | Availability, accuracy, degradation, power |
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
- **f) High voltage:** no HV board before Launch 2, so pivot to evidence:
  - **Heritage:** CCGs on Explorer 32 and on sounding rockets (Lehmacher 2013, 2026); kV detectors and supplies on small-satellite instruments.
  - **Design rules:** HV off through launch and outgassing, a pressure interlock, potting, current limiting.
  - **Phase 2 tests:** vacuum pump-down corona test + thermal-vacuum.
  - **Risk register entry.**
  - **Optional:** a COTS kV module + dummy load on the balloon as a labelled proxy.

## 8. Software and simulation plan (in order)
Built directly as simt scenarios. `fusion_osse.py` is the reference: every new feature gets a small-N check that both agree. Sensor numbers are settings with separate truth/filter values; no instrument-swap framework.

**Phase A: margin sweeps (first, because they set the requirements)**
1. **Realistic drag + drag-coefficient sweep:** day-averaged, 5–16% error plus a 7/15/25% drag-coefficient uncertainty, scaled by host area-to-mass. Tests whether "a bad gauge is fine" survives.
2. **S_O sweep (0–40%) + S_O as a filter state.**
3. **Quick spec sweeps:** drift, FIPEX accuracy, temperature effect, noise. Gives a "must be better than X" list to send early to INFICON and TU Dresden.

**Phase B: complete the models + the filter**
- **CCG:** chamber conversion, floor, nonlinearity, gaps.
- **FIPEX:** O and O+O₂, pointing response.
- **Drag:** day-averaged.
- **Filter:** optional S_O and He states, gap and outlier handling, accuracy/precision/resolution outputs, RMS percent error, effective density.

**Phase C: realism + filter tuning**
- **Baseline and truth:**
  - Real May 2024 storm, with NOAA forecasts for the baseline.
  - Harris-Priester in the filter, with MSIS on forecast inputs as the per-gas prior.
  - Real-data truth from TU Delft (CHAMP / GRACE-FO / Swarm).
- **Filter tuning:**
  - Q and R, using NIS/NEES
  - the drift trade
  - storm response (adaptive Q, rate state)
  - startup
  - EKF vs UKF
  - joint vs two-stage drag
  - host attitude changes
- **Real numbers in → final grid:** altitude × solar min/max × storm/quiet, with and without He. Output: the declared altitude ranges.
- **Stress tests:** mis-tuning, gaps, outliers.

**Phase D: compute**
- **Count:** operations and memory per update.
- **Precision:** float32 vs float64 stability in simt; use a Joseph-form or UD/square-root filter if needed.
- **C++:** port the filter core and match it against Python outputs.
- **Measure on hardware:** on the H753 at full clock **and** in a Vorago profile (100 MHz, float32, 64 KB cap).
- **Deliverable:** "X kB, Y µs per update, float32 within Z% of float64."

**Variable priority** (impact × obtainability):
1. Drag-coefficient uncertainty (literature + hosts)
2. S_O (no data: sweep and estimate)
3. CCG drift (INFICON)
4. FIPEX accuracy and degradation (papers / TU Dresden)
5. Per-unit calibration accuracy (INFICON)
6. Gas factors for O₂ and He (INFICON)
7. Temperature coefficient + gauge temperature swing (INFICON + thermal team)
8. Host area/mass and attitude knowledge
9. Pumping speed + chamber design
10. FIPEX pointing response
11. Nonlinearity
12. Startup gaps

Sweeps come first. Real numbers drop in at the end.

## 9. Compute and hardware
- **Onboard filtering isn't required by OCC.** The baseline is ground processing, with an optional light onboard filter (Harris-Priester + correction). Compute is tiny: a few kB and a few thousand math operations per 30 s. **Single-precision stability is the real constraint.**
- **Boards:**
  - **NUCLEO-H753ZI:** Cortex-M7, 480 MHz, double-precision FPU, 1 MB RAM. The flight-class stand-in; clock it to 300 MHz or scale timings by ~1.6×.
  - **NUCLEO-F446RE:** M4F, 180 MHz, single-precision only, 128 KB. Optional worst case.
- **Flight target:** SAMV71Q21RT (rad-tolerant M7, pin-compatible with the commercial SAMV71). **Conservative:** Vorago VA41630 (rad-hard M4, 100 MHz, single precision, 64 KB). **FPGA:** data handling only.

## 10. Balloon (Launch 2 is the one that matters)
- **Architecture:**
  - **T-Beam flight computer** (ESP32 + LoRa + GPS; sensors; SD log; telemetry).
  - **→ UART → H753 filter computer** (real-time filter; its own SD log of outputs, timing and memory).
  - **Heltec V3 ground station** (+ a 915 MHz Yagi).
  - **Backup tracker:** a second T-Beam on Meshtastic (or APRS if someone has a ham license).
  - **Separate batteries** for the T-Beam and the H753.
- **Software tests:**
  - sensor drivers, logging with GPS-time stamps, telemetry
  - **GPS airborne mode** (must be set, or GPS stops above ~18 km)
  - the analog filter (pressure + temperature + GPS → density + sensor biases), checked against a standard atmosphere and a NOAA sounding
  - real-time compute numbers
  - reset and gap recovery
  - post-flight replay in simt
  - the landing-prediction ensemble updated live (descent packets narrow it the most)
- **Not testable on the balloon:** the density measurement itself (10 mbar is far above the CCG's range), atomic O, radiation.

## 11. Questions out
- **INFICON:**
  1. Gas factors for O₂ and He, plus any atomic-O data
  2. Nonlinearity from 1e-8 to 1e-4 mbar (and whether the controller corrects it)
  3. What makes up the 30%, and the accuracy after per-unit calibration
  4. Drift per month or year
  5. Temperature coefficient (% per °C), head vs electronics, warm-up
  6. Effects of oxygen exposure
  7. Pumping speed for N₂, O₂ and He

  For each answer: measured, typical, or estimated?
- **FIPEX (team research, then TU Dresden):**
  - **From research:** outputs, elements, current-to-density conversion, pointing response, demonstrated accuracy, calibration, degradation, cross-sensitivity, response/warm-up, range, heater power, failure modes, public flight data.
  - **For TU Dresden:** availability/licensing, current specs, calibration service, volume pricing, flight data, SWARM-EX status, **calibrating our CCG in their atomic-O source**, export rules.

## 12. People
- **Shane Lowe** (snlowe@stanford.edu)
- **TU Dresden / Uni Stuttgart** (FIPEX)
- **CU Boulder SWARM-EX** (Pilinski, Thayer)
- **INFICON** (contact established)
- **LLITED/MIGSI team** (optional)

## 13. Where things live
- `fusion_osse.py`, `verify.py`: reference simulation and tests.
- `simt/examples/occ.py`, `validate_occ.py`, `sweep_occ.py`: fast GPU version.
- `reports/OCC sensor suite research.md` + `research_notes/OCC sensor suite research/`: deep research.
- Datasheets in Downloads: MAG084 (tiba71e1-a), STM32H753xI (DS12117), STM32F446xC/E (DS10693), Nucleo data briefs. Lowe paper PDF.
