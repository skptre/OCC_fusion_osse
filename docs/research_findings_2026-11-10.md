# Research findings, night 2 (Nov 10)

Overnight agents, wave 1 (items 1–12 from the Nov 9 list) and wave 2 (every angle to improve the numbers before the fraternal twin).

Tags:
- [TESTED]: ran it (script path + runs)
- [LIT]: cited (abstract/metadata checked unless stated)
- [DERIVED]: math shown
- [ASSUMPTION]: labelled guess

Scratch scripts are in `<scratch>/night2/<agent>/` (the Nov 9 session's scratchpad, not the repo). All numbers are identical-twin and preliminary unless stated.

## 0. Summary (filled in at the end)

TBD.

---

## L9. Making the absolute level defensible

### Verdicts

1. **GOOD: the datum argument [DERIVED].**
   - Scaling all n by k and every offset by −ln k leaves all three readings unchanged, so the common scale is unobservable.
   - The absolute uncertainty is the inverse-variance combination of *independent* anchors: σ_abs = (Σ 1/σ_j²)^−½.
   - Worked cases:

     | Anchors | σ_abs |
     |---|---|
     | drag 7% + gauge 30% + FIPEX 30% | 6.6% |
     | drag 10% + FIPEX 30% + MSIS 15% | 8.0% |
     | drag 10% + leak-calibrated gauge 5% + FIPEX 30% + MSIS 15% | 4.2% |
     | no drag (FIPEX 30% + MSIS 15%) | 13.4% |

   - Anchors with a shared error (the same beam, or one accommodation model across a fleet) count as one.
   - **Check (mine):** our `CD_SD` register value is 0.10, not the agent's 7%. With 10%, the first case becomes (100 + 11 + 11)^−½ ≈ 9.1%.
2. **GOOD at 300 km: host drag with a physics C_D is the best existing anchor.** About 5–10% with host geometry and attitude, 10–25% without.
   - Accommodation is ~0.9 at 300 km. Adsorbed O raises sphere C_D from 2.0 to ~2.3. Shape adds 20–30%; diffuse vs quasi-specular differ by 8–15% (Moe & Bowman 2005, AAS 05-258, full text read).
   - Sentman sphere [DERIVED]: ±0.05 in α gives ±3–5% in C_D (α 1.00/0.95/0.90 → C_D 2.12/2.26/2.35).
   - The large literature errors (~25%) are near 500 km (Bernstein & Pilinski 2022 SW doi:10.1029/2021SW002977).
   - Dataset rescalings:
     - Mehta et al. 2017 SW 15:558, doi:10.1002/2016SW001562: CHAMP 14–18%, GRACE 10–24%.
     - March, Doornbos & Visser 2019 ASR 63:213: geometry alone gave Swarm +32%, CHAMP 11%, GOCE 9%, GRACE 5%.
     - Bruinsma et al. 2023 ASR 72:5476: datasets differ by up to 30%.
   - So absolute density is uncertain at 5–15% for everyone, and a stated 5–10% is competitive.
3. **GOOD, new idea: an in-flight calibrated argon leak into the gauge [DERIVED; novel for a cold cathode gauge, no flight precedent found].**
   - The reading step Δn = Q/C_out from a known flow Q gives an absolute gauge gain. Error budget ~3–6% if the leak spec holds (unconfirmed). Daily pulses also track drift.
   - Sizing: 1 cm² orifice, C_out ≈ 10 L/s for Ar; Q ≈ 1×10⁻⁵ mbar L/s doubles the enclosure density. A 10-min pulse per day uses ~3.6 mg Ar per year.
   - Heritage in mass spectrometers: MAVEN NGIMS (Mahaffy et al. 2015 SSR 195:49, doi:10.1007/s11214-014-0091-1); LADEE NMS; a 1975 in-flight calibrator (Rev. Roum. Phys. 20:839, authors unconfirmed).
   - Risks: discharge mode jumps; escape geometry needs a DSMC check; the valve is a single point of failure (fail-closed); mass and power are a mech/budget call. It does not give S_O.
4. **BAD for absolute: ground atomic-O calibration.**
   - WADIS-2: +35/−28% (Eberhart et al. 2019, AMT 12:2445, doi:10.5194/amt-12-2445-2019, full text read). Dominated by the O⁺ cross-section (+13.5/−15.5%) and the sensor-signal term (+12.5/−25%).
   - FIPEX response is a power law I ∝ n_O^0.35, with per-sensor sensitivity.
   - TALIF methods carry >20% systematic error. No method is documented as better than ~15–20%.
   - The response factor of an instrument exposed to O grows with exposure (Cross, Koontz & Hunton 1995, JSR 32:496, doi:10.2514/3.26642), so a ground-measured S_O would drift unless the gauge is pre-conditioned.
   - **GOOD for the ratio [DERIVED]:** gauge and FIPEX in the *same beam* see the same flux Φ. The ratio g·S_O/f is then flux-free, which fixes the relative O response.
5. **BAD: FIPEX as the absolute anchor.**
   - In WADIS-2 flight, only 1 of 6 sensors (the rotated Aft-2) matched the 762 nm photometer.
   - The standard ram sensors were matched only after scaling photometer and MSIS by 0.15. The authors blame the 3 Hz spin plus the ~1 s gold response.
   - A ram-fixed mount (no spin) may avoid this, but a ±30% absolute calibration is undemonstrated in flight.
6. **BAD as anchors: hydrostatic shape, scale height, diffusive equilibrium [DERIVED].** These are homogeneous in n, so they fix T and relative composition, not the scale. The apogee zero point is additive only, though still useful for background and leakage.
7. **BAD at 300 km: Swarm / GRACE-FO conjunctions.** The references' own scale is uncertain (≤10–30%). The 490 → 300 km transfer amplifies a scale-height error ~3.5×. Use them for validation only.
8. **Gauge ground calibration [LIT].**
   - PTB 2003 (JVST A, doi:10.1116/1.1578654, abstract): inverted magnetrons less stable over 72 h than hot cathodes; similar long-term stability.
   - EURAMET 16NRM05: 1–3%, but for hot cathodes only.
   - So ground calibration gives the R_i ratios at a few %, while the gain shifts in orbit. Consistent with our 30% prior.

### Ranking of anchors

| Rank | Anchor | 1σ absolute | Verdict |
|---|---|---|---|
| 1 | Host drag with physics C_D + geometry/attitude | 5–10% (10–25% without) | GOOD |
| 2 | In-flight Ar leak into the gauge | 3–6% gauge gain + drift tracking | GOOD, novel; OSSE test needed |
| 3 | Ground gauge calibration in N₂/Ar/He | few % | Prerequisite for 2 |
| 4 | Joint gauge + FIPEX O-beam calibration | 20–35% absolute, ratio few % | GOOD for the ratio |
| 5 | FIPEX absolute | +35/−28% | BAD until Stuttgart's new number |
| 6 | Reference conjunctions | ≥10% + transfer | Validation only |
| 7 | MSIS prior | ~15–20% | Weak |
| 8 | Hydrostatic / diffusive / zero / ISR | none | BAD |

**Proposal datum wording (draft):** "Relative composition and density come from the sensors. The absolute scale is anchored by host drag with a physics-based C_D, and by in-flight gas-leak calibration of the gauge. It is combined by inverse variance with FIPEX's absolute calibration, a weaker third anchor. Ground O-beam calibration fixes the gauge-to-FIPEX O response ratio."

### Open questions

- OSSE test: daily leak observation y = b_g + ε at σ 5%. Does S_O stay identifiable?
- Stuttgart: their new calibration uncertainty; can they put a gauge and FIPEX in the same beam; O-exposure pre-conditioning.
- INFICON: R_Ar/R_N₂ stability; what the ±30% is made of.
- Leak supplier spec; host geometry and attitude.

---

## L6. Fraternal-twin truth: plan + FIRST RUN

Scripts: `L6/msis_versions.py`, `L6/n2_structure.py`, `L6/fraternal_run.py` (builds its own cache `L6/cache_v0truth/`; repo untouched). Results: `L6/fraternal_run.log`.

### First fraternal run [TESTED, 200 runs, seed 1, current GM filter; I re-read the log]

Truth = NRLMSISE-00 (pymsis `version=0`) on real drivers + wiggles. Prior = MSIS 2.1 on forecasts (bit-identical to the repo cache). The identical-twin run reproduces our baseline.

Fused MAE p50, identical → fraternal:

| | Quiet | Storm | Recovery |
|---|---|---|---|
| ρ | 4.6 → 12.3% | 4.4 → 10.4% | 6.8 → 13.1% |
| O | 4.2 → 11.4% | 9.7 → 16.6% | 4.9 → 11.2% |
| N₂ | 6.0 → 15.7% | 8.6 → 12.2% | 14.1 → 20.3% |

- For comparison, the prior's ρ MAE is 14.8 / 22.0 / 14.9%, and its N₂ MAE is 20.7 / 28.2 / 18.7%.
- NEES 3.1 → 6.7 (gap_O 7.9, gap_N₂ 10.2, gauge_gain 7.1, o_gain 9.5). NIS stays 1.0–1.2: the innovations look fine while the states are wrong.
- **All fused biases are negative, and about equal to the prior's bias** (quiet ρ: fused −12.3%, prior −13.1%). The filter barely moves the absolute level off the prior.
- **Verdict: BAD as it stands.** Density is still inside 20%; composition is outside 10%; the filter is overconfident.

**Why (my diagnosis; test running in `M1/p0_test.py`).** `P0_MSIS_SD` = (4.8%, 6.1%, 1.0%) was derived from the identical twin's ln(truth/prior), so it only knows about driver-forecast error. It tells the filter that the model is right to ~5%, while the gains are uncertain to 30% and C_D to 10%. So a 10–18% model offset gets assigned to the gains and C_D, not the atmosphere. This is an identical-twin artefact in our own tuning. The gap prior must come from published model-vs-data error (Bruinsma & Laurens 2024: 14.5–27% storm std, plus bias), not from the twin. With gap σ ≈ 20% and C_D 10%, drag should pull ~80% of the absolute offset out [DERIVED: 0.2²/(0.2² + 0.1²) = 0.8].

### How different are the two models? [TESTED]

ln(MSISE-00 / MSIS 2.1) at 300 km, mean / sd:

| | Quiet | Storm | Recovery |
|---|---|---|---|
| ρ | +0.100 / 0.028 | +0.128 / 0.036 | +0.113 / 0.032 |
| O | +0.067 / 0.009 | +0.103 / 0.015 | +0.086 / 0.010 |
| N₂ | +0.188 / 0.102 | +0.178 / 0.099 | +0.174 / 0.101 |
| He | −0.004 / 0.023 | +0.114 / 0.053 | +0.044 / 0.032 |

- **Structure:**
  - O is a pure offset.
  - N₂ is an offset plus a semidiurnal local-time term of amplitude 0.10 (re-fitted tides).
  - He has a latitude term.
- MSIS 2.0 vs 2.1 differ by exactly 0 for these species (2.1 only adds NO; Emmert et al. 2022 JGR 127, e2022JA030896).
- **BAD: MSISE-00 is a sibling, not a true fraternal twin.**
  - The storm *response* differs by only ~3%: ln(storm/quiet) ρ is +0.443 vs +0.415.
  - Real storm error vs data is 14.5–27% (Bruinsma & Laurens 2024, JSWSC 14:28, doi:10.1051/swsc/2024027).
  - On the March 2015 storm, peak enhancement vs MSIS 2.0 differs by −14% (DTM2020), +25% (JB2008), −15% (TIE-GCM) [DERIVED from Zhang et al. 2025, Front. Astron. Space Sci., doi:10.3389/fspas.2025.1644152].
  - So this truth tests the *offset* problem honestly but understates the storm-shape error by about 5×.

### Candidate truths

| Candidate | Composition | Access | Note |
|---|---|---|---|
| NRLMSISE-00 | full | pymsis `version=0`, done | sibling; offset test |
| DTM2020 (operational F10.7/Kp; research F30/Hp60) | H, He, O, N₂, O₂, N + σ | Fortran 90, github.com/swami-h2020-eu/mcm; needs gfortran | CNES licence: academic, non-commercial, no modification. Not accepted by the agent; **the user's decision.** Best second truth (Bruinsma & Boniface 2021 JSWSC 11:47). |
| JB2008, HASDM | density only | SET | HASDM for May 2024 unconfirmed |
| TIE-GCM / WACCM-X / GITM | full | CCMC Runs-on-Request, weeks | no May 2024 composition output found |
| GRACE-FO density | none | free, through 31 May 2024 | ~500 km, real data |
| GOLD ΣO/N₂ | column ratio | free | Evans et al. 2024 GRL 51, e2024GL110506 |

### Recommended ladder

1. MSISE-00 truth (done).
2. DTM2020 truth.
3. DTM2020 × data-scaled perturbations: GRACE-FO obs/model statistics for density; an O-vs-N₂ split through a ΔT∞ perturbation (Weimer et al. 2016 JGR doi:10.1002/2016JA022691), with amplitudes tied to Bruinsma & Laurens.
4. After the proposal: TIE-GCM structure from a CCMC run.

**What a reviewer accepts** (Hoffman & Atlas 2016, BAMS 97:1601, doi:10.1175/BAMS-D-15-00200.1):
- the truth has a different formulation, fitted to different data;
- the prior-vs-truth error distribution matches published model-vs-data σ (show the plot);
- the truth never uses filter internals;
- final checks are on real data (GRACE-FO, DE-2).

**Open questions (the user's decisions):**
- The DTM licence.
- Installing gfortran in the scratch dir or WSL.
- Downloading GRACE-FO.

---

## L7. DE-2 NACS real-data replay

Scripts and data: `L7/scripts/` (nacs_read.py, compare_generic.py, check_time.py), `L7/data/` (~64 MB). Results: `L7/compare_198209_350.txt`, `L7/compare_stormdays_350.txt`.

### Verdicts

1. **GOOD: the data are easy to get [TESTED].**
   - NASA SPDF `pub/data/de/de2/neutral_gas_nacs/`: NSSDC 81-070B-03E (1-s ASCII with orbit columns) and 03C (binary); daily CDFs on CDAWeb.
   - Species: O, N₂, He, N, Ar (cm⁻³, % error), with altitude/lat/lon/LT, 8 Aug 1981 – 15 Feb 1983.
   - Coverage ~19% of each day, with gaps up to 6 h. No O₂ or H; N is 77% empty.
   - WATS (temperature, winds) and orbit CDFs are in the same archive.
2. **GOOD for the proposal: real MSIS error is far bigger than our identical-twin gap [TESTED, alt <350 km, day means; I re-read `compare_stormdays_350.txt`].**
   - NACS/MSIS 2.1 − 1, storm days (ApD 59–199):

     | Species | Range |
     |---|---|
     | O | −23% … +29% |
     | N₂ | −42% … +15% |
     | He | −37% … +4% |
     | ρ | −26% … +11% |

   - 14 Jul 1982 (ApD 153): ρ −26%, N₂ −42%. 7–8 Sep 1982: ρ −25%, N₂ −39% (agent's figure, other output file).
   - NRLMSISE-00 is 15–20% further low; consistent with MSIS 2.0's ~10% O / ~20% N₂ reductions (Emmert et al. 2021, Earth Space Sci. 8, e2020EA001321).
   - **This is our first non-identical-twin number.** It confirms that real MSIS errors (tens of %, varying day to day) are much larger than the twin's ~5% prior gap. Expect our fraternal-twin results to be worse than now, and our *improvement over MSIS* to look larger.
3. **BAD: NACS is not an absolute truth.** The PI states a 25% absolute calibration error, and O assumes full recombination in the ion source (Carignan et al. 1981, Space Sci. Instrum. 5:429). So the replay tests whether the filter **tracks the shape of real departures** (relative), not the 20%/10% absolute targets. Day-to-day swings (e.g. O +29% → −23%) exceed what a constant scale could explain, so the departures are real.
4. **BAD, now fixed: the ASCII files have a midnight bug [TESTED, `check_time.py`].** Records after 00:00 UT carry the wrong day's positions. It made 6 Sep 1982 look 5× noisier (sd ln O ratio 1.02 → 0.18 after dropping those records). Any replay must screen for this.
5. **MIXED: circularity can be argued around.**
   - DE-2 helped build MSIS-86 (Hedin 1987 JGR 92:4649) and is carried into later versions.
   - But MSIS 2.x tuned its thermosphere to 1986–2005 orbit-decay densities (Emmert 2021 §3.1, §4.7), so 1981–83 lies outside its fitting period.
   - Circularity makes the prior *better* on this data, so any fusion gain is a lower bound.
   - Protocol: freeze the filter tuning before running; show MSIS 2.1 and NRLMSISE-00 priors side by side; repeat on AE-C.
6. **MIXED: the elliptical orbit.** The N₂ ratio changes with height (−5% at 285 km, −41% at 390 km). Use samples <350 km only, or 31 Jan–8 Feb 1983 (near-circular, 245–345 km, Kp 8 storm).
7. **BAD: no DE-2 drag product.** Simulate the drag reading from NACS, averaged over covered samples. Orbit-decay global means (Emmert 2009 JGR 114:A06315) give a coarse outside check only.
8. **GOOD: a second replay exists.** AE-C (1973–78, 15-s, on SPDF) has an accelerometer density plus two mass spectrometers (NACE, OSS) on the same spacecraft, so real density and composition together. Others: CHAMP/GRACE/Swarm (density only), GOLD/GUVI (O/N₂ column), ESRO-4.

**Recommended windows:**
- 3–10 Sep 1982: Kp 8.7, all three phases; already downloaded.
- 20–28 Nov 1982: densest low-altitude coverage.
- 31 Jan–8 Feb 1983: near-circular orbit.

**To build the replay:** an OSSE subclass with a gap mask, about a day of work. Needs the user's go; it's core work, so the user hand-types it.

**Open questions:**
- Is OMNI F10.7 adjusted or observed?
- Hedin 1987's data table (not read).
- Will reviewers accept a drag reading averaged over covered samples?

---

## L8. Gauge outgassing background

Scripts: `L8/bg_budget.py` (pymsis budget, not the OSSE filter), output `L8/bg_budget_out.txt`.

### Verdicts

1. **GOOD: at 300 km, outgassing is negligible after ~1 day [DERIVED + TESTED].**
   - Chamber-wall model from the CERN unbaked-metal law: b ≈ 2e-6/t[h] Pa. That is 8e-8 at 1 day, 1.2e-8 at 1 week, 2.8e-9 at 1 month; H₂ floor ~7e-10 Pa.
   - Ignoring it: density error <0.1%, N₂ <0.3%. **Our OSSE headline numbers are unaffected.**
   - My check: 2e-6/720 h = 2.8e-9 ✓. Against 300 km night ambient 8.6e-5 Pa, the background fraction is ~3e-5 ✓.
2. **BAD: at 400–500 km near solar min, composition breaks.**
   - N₂ is only 0.6–4% of the night-time gauge signal there, and gauge − FIPEX puts all of b into N₂ (δN₂/N₂ = f / N₂ share).
   - At F10.7 = 70 with b = 3e-9 Pa (1 month): N₂ +4% at 400 km, +32% at 450 km, >100% at 500 km. Density stays <2%.
   - Night ambient and N₂ share:

     | Case | Night ambient | N₂ share |
     |---|---|---|
     | 300 km F150 | 8.6e-5 Pa | 0.29 |
     | 400 km F70 | 1.85e-6 Pa | 0.04 |
     | 500 km F70 | 2.0e-7 Pa (below the 1e-6 Pa gauge floor) | 0.006 |

   - **This supports our composition claim range of 250–400 km.**
3. **BAD (corrects Nov 9 finding #8): day/night variation can NOT separate background from gain in practice [DERIVED + TESTED].**
   - Fisher matrix I = σ⁻²Σ[(1−f)², (1−f)f; (1−f)f, f²] is singular only if f is constant, so on paper it works. corr(ln g, ln b) ≈ −0.94.
   - But a model day/night shape error δln r gives a false background fraction δf_n = δln r/(1 − 1/r). The leverage is 1.6–3.2×, so a 5% shape error gives 8–16 points of false f. That is worse than ignoring b.
   - The identical twin hides this, since truth and prior share the shape. **Never let a free b be driven by day/night contrast.**
4. **GOOD: direct zero checks fix it.**
   - A shutter/flap over the orifice, closed 5–10 s every 5–10 min (chamber τ ~5 ms, ~2% duty), measures b directly.
   - Precedents [LIT, NSSDC AE data guides oss.txt/nace.txt/nate.txt]:
     - AE OSS and NACE subtracted the wake reading of each spin.
     - AE NATE had a movable baffle.
     - Explorer 17 used ram/wake (unconfirmed snippet).
     - AE OSS excluded its first month from high-precision use.
   - Host attitude manoeuvres are a backup.
5. **BAD (risk): the orbit-periodic thermal and sunrise-burst background is strong.**
   - Water on metal E ≈ 1 eV, so b changes ~14% per K of chamber temperature (±2 K → ±27%).
   - MSX saw ×100 water pressure when shadowed blankets were sunlit, even after 6 years. Rosetta exceeded 1e-8 mbar within seconds of a reorientation (Schirmer et al. 2023 A&A arXiv:2305.10107, review).
   - Fix: a chamber thermistor in the measurement model (Arrhenius term), and an orifice that cannot see host blankets.
6. **GOOD: defensible decay laws.**
   - 1/t for days, then t^−0.5 to t^−0.6 for months to years (MSX).
   - Rosetta COPS: desorption ∝ exp(−t/30 d) for ~200 days, then diffusion t^−0.5; 2e-9 → 7e-11 mbar over 1100 days (Hässig et al. 2011 ICST, doi:10.1109/ICSpT.2011.6064657; Schläppi et al. 2010 JGR 115:A12313, doi:10.1029/2010JA015734).
   - Lab: Chiggiato 2020 (arXiv:2006.07124): unbaked metal q ≈ 3e-9/t[h] mbar·L/s/cm²; water desorption 0.9–1.06 eV; venting erases the bake.

### Filter design (Phase B)

y = ln(g·S + b), with b = b0·(t/t1)^−α·exp[κ(T_c − T_ref)]·exp(ξ).

- New state: ln b0 (slow random walk).
- α and κ from TVAC + RGA, or carried as consider parameters.
- ξ: AR(1) or a robust update for sunrise bursts.
- Shutter readings: y = ln b, or a one-sided limit near the floor.
- O-induced wall chemistry ∝ O flux, so it folds into S_O. Let S_O random-walk faster in month 1.
- Test it only on a truth with a day/night shape error (fraternal).

### Mech-team rules

1. All-metal CF chamber with copper gaskets; **no polymers** in the chamber volume (1 cm² of neoprene → b ≈ 3e-4 Pa).
2. Bake ≥150 °C for 24 h (MAG084 is rated to 230 °C), then keep it sealed: a cover opened in orbit, or a dry-N₂ purge.
3. Orifice baffle with no view of blankets, panels or radiators.
4. Thermally isolated chamber with a 30 s thermistor.
5. Shutter if possible.
6. ≥2 weeks of commissioning, with host manoeuvres requested.

### Open questions

- INFICON: what sets the MAG084's 1e-8 mbar floor (leakage-current offset)? It may exceed outgassing. Also the re-ignition time.
- How LLITED MIGSI (a ram Bayard–Alpert gauge at ~430 km; Swanson et al. 2026 JGR doi:10.1029/2026JA035137, paywalled) handled background.
- Whether the host can manoeuvre.
- How large MSIS's day/night ratio error is.
- FIPEX zero offset (not studied).

---

## L11. Storm handling + onboard compute

### A. Storm handling

- **BAD: adaptive Q cannot fix the recovery weakness [DERIVED].**
  - Mehra, Sage-Husa, Kp/Hp30-scheduled Q and IMM all output one Q(t). At best they equal the oracle Q we already ran: storm N₂ +8.6 → +7.3%, recovery unchanged.
  - Recovery N₂ −14% is a bias (gauge-gain drift absorbed by gap_N₂), not a noise level.
  - Caveat: the oracle covered one Q shape only. A different correlation structure is not covered, and that is what driver states change.
  - Citations: Mehra 1970 IEEE TAC 15(2):175, doi:10.1109/TAC.1970.1099422; Sage & Husa 1969 (8th IEEE Symp. Adaptive Processes); Blom & Bar-Shalom 1988 IEEE TAC 33(8):780.
- **GOOD: Särkkä & Nummenmaa 2009 (IEEE TAC 54(3):596, doi:10.1109/TAC.2008.2008348) adapts R, not Q.** Use it for storm representation error (helps NEES). It does not fix recovery.
- **GOOD: every system that works in storms estimates drivers or temperatures [LIT].**
  - HASDM (Storz et al. 2005 ASR 36:2497, doi:10.1016/j.asr.2004.02.020).
  - Sutton 2018 IRIDEA, effective drivers, quiet + storm (SW 16:736, doi:10.1002/2017SW001785).
  - Morozov et al. 2013: F10.7 state in GITM EAKF; CHAMP bias 73 → 7%, independent GRACE 76 → 52% (JASTP 104:126).
  - Mehta, Linares & Sutton 2018 ROM + KF (SW 16:569, doi:10.1029/2018SW001840).
  - Gondelach & Linares 2020 (SW 18 e2019SW002356).
  - Weimer et al. 2020 (SW, doi:10.1029/2019SW002355).
  - Codrescu et al. 2022 TIDA (JSWSC 12:16).
  - Matsuo, Lee & Anderson 2013: density-only assimilation helps only locally (JGR 118:1339).
- **Driver-state hybrid [DERIVED, untested].** 2 driver states (δT∞ + boundary scale) mapped to the gas groups by the per-step MSIS Jacobian, plus small residual gap random walks. This ties N₂ to O and ρ, so a gauge-gain drift can't hide in N₂. **Fraternal truth only.** In the identical twin the gap *is* a driver error, so it would look too good.
- **BAD evidence gap: composition.** Operational systems validate density only. Composition evidence is synthetic (Codrescu, Fuller-Rowell & Minter 2004 SW doi:10.1029/2004SW000088; Minter et al. 2004 SW doi:10.1029/2003SW000006: <6% at 15% obs error) or mixed vs GUVI (Ridley et al. 2026 SW doi:10.1029/2025SW004925: O/N₂ RMS ~30%).
  - **Relevance point:** initialising thermosphere composition gives most of the storm-forecast benefit, ≥10% for 18 h (Chartier, Jackson & Mitchell 2013 JGR 118:7329, doi:10.1002/2013JA019034). In-situ composition is the data type operational systems lack.
- **Ranked recovery fixes:**
  1. Ground RTS smoother.
  2. FIPEX drift-rate state.
  3. Driver-state hybrid (fraternal truth).
  4. VB R adaptation.
  5. Hp30 instead of Kp.
  6. Drop Kp-Q/IMM as a recovery fix.

### B. Onboard compute (STM32H753, 480 MHz, DP FPU, 1 MB RAM)

- **GOOD: the EKF step [TESTED counts, matches simt to 3e-16, `L11/ekf_flops.py`].** ~2.1 kFLOP + ~10 exp/log per 30 s; ~22 µs; 2–3 kB RAM.
- **GOOD: the 7-filter bank.** ~15 kFLOP, ~0.2 ms, 15–20 kB. Run it on the ground anyway.
- **BAD onboard, fine on the ground: the RTS smoother.** ~6.5 kFLOP/step, but ~3 MB/day of history vs 1 MB RAM. A fixed-lag version needs ≥1 day of lag for the drag update.
- **GOOD, porting risk: MSIS 2.1 [TESTED on the PC, M7 DERIVED].** 86–90 µs/point on the PC; M7 ~0.7–4 ms (plan 10 ms), ≤0.03% CPU. The parameter file is 537 kB, 94.6% zeros (sparse ~36 kB). Fortran, so it needs a C port. Alternative: uplink a ~35 kB/day prior table.
- **GOOD: process on the ground [DERIVED; sampling rates are ASSUMPTIONS].** 30 s raw averages ~35 kB/day; raw 1 Hz 346–691 kB/day; processed product 46–81 kB/day. Onboard processing saves no bandwidth. Baseline: downlink raw, process on the ground, with the onboard EKF as an optional low-latency/event product.
- **Open:** host bytes/day; real sampling rates; real-board cycle counts; a C port of MSIS 2.1. Confirm citations: Blom & Bar-Shalom pages, JB2008 (Bowman 2008 AIAA 2008-6438), Yamazaki 2022 DOI, RTS 1965, Bierman 1977.

---

## L10. Hostile-reviewer pass (red team)

Script: `L10/prior_bias_test.py`; outputs `L10/prior_bias.csv`, `L10/prior_bias.log`. 200 runs, seed 1. f = 1.0 reproduces `out/phase_a/A1.csv` exactly.

### What the judges score (OCC pages, fetched Nov 10)

- **Phase 1 criteria, each scored 1–5:** Relevance, Performance, Cost and scalability, Flight readiness. Five reviews per submission.
- **Benchmarks:** in-situ mass density 20% accuracy / 10% precision / 30 s.
- **The 10% composition benchmark is for remote sensing at 90–300 km.** In-situ composition is "valued but not required". So we should declare our own composition targets, not adopt 10%.
- **Hard rules:**
  - hosted payload only, no host interference
  - contamination tolerance must be addressed
  - daily data volume and peak rate stated
  - ≥1 year of operation
  - ≥100 units
  - state the altitude range where we meet our numbers

### Biggest finding [TESTED]: the fused density follows the prior's scale error almost 1:1

Truth tables multiplied by a factor f; density bias p50:

| Case | Prior bias (quiet / storm / recovery) | Fused bias (quiet / storm / recovery) | NEES |
|---|---|---|---|
| f = 1.0 | −4.0 / −10.9 / −2.0% | −4.6 / −4.1 / −6.8% | 3.1 |
| f = 1.25 | −23.2 / −28.8 / −21.6% | −21.5 / −19.7 / −21.5% | 5.3 |
| f = 0.80 | +20.0 / +11.3 / +22.5% | +16.1 / +14.5 / +10.6% | 3.7 |
| truth = prior | +0.8 / +0.9 / +0.8% | −0.4 / −1.2 / −2.5% | 0.71 |

- **Cause (same as my L6 diagnosis, found independently):** `P0_MSIS_SD` and `Q_MSIS_SD` are derived from the twin's own truth-vs-prior tables, so the filter trusts MSIS to ~5% and treats daily drag (6% noise + 10% C_D) as the weaker source.
- The baseline's one-sided bias is mostly inherited from the prior. With truth = prior it nearly vanishes.
- The "10–14% → 4–7%" gain is mostly the filter removing the synthetic AR(1) wiggle, whose statistics it is given exactly.
- **Fix under test:** `M1/p0_test.py` (gap P0 from a real error climatology).

### Attacks, ranked

**Fatal unless handled:**
- **Identical-twin numbers as the headline.** Lead with fraternal numbers; show the twin as "sensor-limited performance".
- **The MAG084 magnet on small hosts.** About 14 A·m² and 4e-4 N·m in a 30 µT field [DERIVED, magnet volume 15 cm³ ASSUMED]. OCC forbids host interference. Needs a measured dipole (or INFICON's figure), a mitigation (counter-magnet, shield, distance), and a list of excluded hosts. This is for the mech team.

**Major:**
1. **The filter knows the truth's statistics:** same AR(1) τ/σ, P0/Q from the twin, R equal to the true noise, identical measurement equations. Needs one mis-tuned run (R ×2 and ×0.5, wiggle τ/σ off 2×, climatology P0).
2. **Clean Gaussian sensors:** no outliers, gaps, attitude error, wind or background. Needs one "dirty sensor" stress run.
3. **One storm, 5 days, 300 km, high solar activity.** State that plainly, and cap the composition claim at 400 km (L8).
4. **FIPEX response form.** Our code is linear in n_O. Eberhart 2019 reports I ∝ n_O^0.35 with per-sensor sensitivity. With exponent 0.35, a 5% current noise is ~14% in n_O [DERIVED]. Ask Stuttgart whether the reworked sensor is linear; say which units `O_NOISE` and `O_GAIN_SD` are in.
5. **Drag truth is too kind:** constant C_D, white noise. Real C_D moves with adsorbed O (2.0 → ~2.3), so it shifts in storms.
6. **Drift over one year.** "≲0.5%/day" read literally is 180% in a year. Restate it as drift between calibration anchors, and run a 30-day case.
7. **Uncertainty wording.** "Honest, validated uncertainty" is contradicted by NEES 3.1 (6.7 fraternal). NIS can't see unobservable directions.
8. **S_O bank margin is thin:** neighbouring grid points differ by 1.2–2.3 nats out of ~63,000. Untested against gas-factor or composition-shape error (E1 is testing this). S_O is also not constant: it grows with O exposure (Cross et al. 1995).
9. **Ram pointing on a host we don't control.** No attitude in the model.
10. **One-year life in atomic O:** fluence ≈ 2.4e22 atoms/cm² per year at 300 km [DERIVED]; no FIPEX drift data exists.
11. **Host altitude vs the one-year rule.** An unpropelled host at 300 km decays ~3 km/day [DERIVED] and lasts weeks. Real hosts sit at 480–550 km, where our composition claim does not hold. Name propelled VLEO hosts, or state what we deliver at 450–500 km (density only).
12. **FIPEX supply:** a single university lab, $80k × 100 = $8M (still far below $1M each). Needs a production-rate statement.
13. **No model-improvement evidence** (only the idea). Best citation: Chartier et al. 2013.
14. **"HASDM / accelerometers already give density."** Answer: same absolute anchor, plus 30 s resolution, eclipse coverage and composition. Don't claim better absolute density.
15. **"He, O₂, N credibly inferred"** comes from a separate static fit, not the filter. Label it model-based inference.

**Minor:** 200 runs make P90 noisy; only 32 phases; GOLD and SWARM-EX are complementary; the argon leak should be a Phase 2 trade study, not a baseline claim.

### Internal inconsistencies to fix in our docs

| # | Where | Problem |
|---|---|---|
| I1 | §7a strength #5 | "Honest, validated uncertainty" vs NEES 3.1 / 6.7 |
| I2 | §7a strength #2 | "Unchanged from 12% to 30% FIPEX": no sweep varies `O_GAIN_SD` alone |
| I3 | §7a strength #3 | "84% of gain uncertainty removed": `a0_observability.py` uses 4 runs |
| I4 | `params.py` | `P0_MSIS_SD`, `Q_MSIS_SD` tagged "sourced" but derived from the twin |
| I5 | `GAUGE_NOISE` 0.01 | Datasheet repeatability is 5%; A4 swept only 0.5–3% |
| I6 | `sensors.py` FIPEX | Linear in code vs power law 0.35 in the cited paper |
| I7 | §7b item 7 | Names `ATMOS_COVARIANCE`, which is not in `params.py` |
| I8 | Nov 9 findings §1e vs §4.2 | Zanetti & D'Souza dated 2015 and 2013 |
| I9 | `sources.md` Eberhart row | Says Table A1 not pulled; L9 has now read it |
| I11 | §8 C5 | The 10% composition target is a remote-sensing benchmark |
| I12 | §4 table | "NEES 0.5" is from the old filter |
| I13 | §7a "inside 20%/10% in all windows" | True for the twin only |
| I16 | Nov 9 findings §0.8, §3 | Day/night separation of background, now shown invalid (L8) |
| I17 | Header | "Last updated Nov 5" |

### Top 10 before submission

1. Replace the density headline: fraternal numbers plus the datum statement (absolute from drag C_D, ~8–10%; precision 1–2%).
2. Fix the uncertainty wording; report error bars inflated by √NEES until the filter is fixed.
3. Magnet: measure or obtain the dipole; state mitigation and excluded hosts.
4. Altitude and hosts: name reference hosts; composition 250–400 km, density-only above.
5. Remove or back the three untested strengths (I2, I3, the easy-test S_O numbers).
6. Stress the S_O bank once (gas factors, fraternal truth).
7. Resolve the FIPEX response form with Stuttgart.
8. Add OCC-required items: data volume (L11), contamination paragraph (L8), power and mass table.
9. Relevance case: Chartier 2013, "same anchor, more information"; label He/O₂/N as model-based.
10. Supply and lifetime: Stuttgart production rate; Phase 2 atomic-O fluence test.

---

## E1. S_O likelihood bank: aliasing, days needed, mixture, fraternal twin

Scripts: `E1/e1_batch.py` (batched bank), `E1/e1_an.py`, `E1/e1_extra.py`, `E1/e1_bank.py` (cross-check). Tables: `E1/an_task1.txt`, `an_task2.txt`, `an_frat.txt`. The batched copy reproduces `out/a2b/fipex30_drift.log` to every printed digit.

### Verdicts

1. **BAD (most important): the S_O bank fails on the fraternal twin [TESTED, 100 runs].**

   | Truth S_O | Estimate P10 / p50 / P90 | Bias | rms |
   |---|---|---|---|
   | 0.56 | 0.45 / 0.45 / 0.79 | −0.030 | 0.138 |
   | 0.66 | 0.45 / 0.45 / 0.84 | −0.098 | 0.183 |
   | 0.77 | 0.45 / 0.47 / 0.85 | −0.176 | 0.244 |

   - The estimate sits at the bottom grid edge. Picking makes composition *worse* than fixed 0.56 (truth 0.66: quiet N₂ 24% → 29%, NEES 57 → 206).
   - Caveat: this used the twin-derived P0 (~5%), which we now know is wrong. A retuned filter is untested (queued in M1).
   - **"S_O estimated in flight to ±0.05" is not defensible as it stands.** See the identifiability algebra below for why.
2. **GOOD: O₂ ±10% and He ±25% do not alias** (S_O shift ≤0.003).
3. **BAD: atomic N aliases.** N ±10% moves S_O by ∓0.036 (5.5%), as much as the statistical rms, though N carries only 1.4% of the gauge signal. Mechanism unexplained; flagged risk.
4. **Neutral: a common non-O scale is exactly degenerate with S_O [DERIVED + TESTED].** ΣR·n = c·((S_O/c)·n_O + ΣR⁰n). ±5% shifts S_O by −0.032 / +0.034 (predicted −0.031 / +0.035). The bank measures S_O *relative to the non-O factors*.
5. **BAD: more days do not help.** Day 1 (quiet) already gives rms 0.04. Storm days add a systematic +0.03 to +0.04 bias. Day 5 rms is 0.046–0.049.
6. **BAD: neither a parabola fit nor a weighted mixture removes the cost at truth 0.56** (quiet N₂ 6.0% fixed vs 7.7–8.6%). It is the price of an 8% S_O uncertainty, not a picking artefact. **GOOD:** the mixture's uncertainty is honest in the twin (NEES 2.1–2.5).
7. **GOOD: the A2b likelihood is computed correctly.** About 90% of the S_O discrimination is in the FIPEX innovations. The likelihood is shallow: adjacent grid points differ by 0.3–3 units out of ~63,000.

---

## M. Identifiability algebra: what the three sensors can and cannot fix [DERIVED, mine]

Two main gases (O, N₂), three sensors, constant unknown scales:

- FIPEX: y₁ = f·O
- drag (if resolved along the orbit): y₂ = c·(16·O + 28·N)
- gauge: y₃ = g·(S·O + N)

Eliminating O and N: **y₃ = a·y₁ + b·y₂**, with a = g·(S − 16/28)/f and b = g/(28c).

- The data fix only **a** and **b**: two numbers. The unknowns are four: f, c, g, S. So **two external anchors are needed**, not one:
  1. an absolute anchor (C_D, or a calibrated gauge gain), and
  2. a composition anchor: either S, or the FIPEX-to-gauge ratio f/g.
- In the identical twin, the model's O/N₂ ratio acted as the hidden composition anchor (the prior matched the truth to ~5%). That is why the S_O bank "worked" there, and why it collapses on the fraternal twin. A constant model O/N₂ error δ is exactly equivalent to S → S·e^(−δ).
- **So in flight, S_O and the mean O/N₂ model error cannot be separated without a ground calibration.** The honest claim is one of:
  - S_O known from the ground → the flight data measure the O/N₂ ratio independent of the model; or
  - f/g known from a same-beam ground calibration (L9: the beam flux cancels, so a few % is plausible) → both S_O and O/N₂ follow.
- **Near-coincidence worth knowing:** the gauge's gas factors are close to mass ratios (R_i vs m_i/28: O 0.56 vs 0.571, O₂ 1.01 vs 1.14, He 0.18 vs 0.14, N 0.58 vs 0.50). So the static gauge is almost a mass-density sensor: a ∝ (S − 0.571) ≈ 0.
  - Good: gauge density is robust to composition and to S_O (matches Phase A: density unaffected by S_O).
  - Bad: the gauge carries almost no composition information by itself. Composition = FIPEX O against the density scale, so N₂ error ≈ (O mass share / N₂ mass share) × the error in f relative to the density scale ≈ 2× at 300 km.
  - The ram-chamber weighting (S_i·√m_i) changes the O/N₂ weight ratio to ~0.42, which moves it away from 0.571 and gives the gauge some composition leverage. Phase B's ram model matters more than we thought.
- **Consequence for the design:** the single most valuable calibration for composition is the **same-beam gauge + FIPEX ratio** (plus the gauge's N₂ gain). The FIPEX absolute calibration (30%) then stops mattering.

---

## M1–M3. My fixes on the fraternal truth [TESTED, 100 runs each, seed 1]

Scripts and logs: `M1/p0_test.py`, `M1/ratio_test.py`, `M1/corr_test.py` (+ `.log`, `.json`). Truth = NRLMSISE-00 (L6 cache); prior = MSIS 2.1 on forecasts. Only parameter overrides or subclasses; repo untouched. MAE p50, quiet / storm / recovery.

| Case | ρ | O | N₂ | NEES |
|---|---|---|---|---|
| Fraternal, twin-derived gap prior (~5%) | 12.8 / 11.1 / 13.7% | 11.5 / 17.7 / 13.1% | 15.1 / 12.1 / 20.0% | 6.7 |
| Gap prior 10% | 10.6 / 8.3 / 11.3% | 9.4 / 15.2 / 10.2% | 13.7 / 10.9 / 18.1% | 6.2 |
| **Gap prior 20%** | **6.6 / 6.2 / 7.1%** | 6.8 / 11.1 / 8.3% | 11.4 / 11.3 / 15.1% | 6.1 |
| Gap prior 30% | 8.4 / 7.4 / 7.0% | 8.2 / 10.3 / 8.0% | 11.8 / 12.2 / 14.8% | 6.4 |
| Gap 20% + C_D 5% | 5.9 / 4.9 / 5.6% | 6.4 / 9.3 / 6.9% | 11.4 / 11.1 / 14.1% | 6.1 |
| **Gap 20% + gauge gain 5%, drift 0.2%/day (leak-calibrated)** | **3.4 / 3.5 / 3.3%** | 4.0 / 9.0 / 6.2% | 8.8 / 9.4 / 13.2% | 6.6 |
| Gap 20% + leak gauge + C_D 5% | 3.2 / 3.0 / 2.8% | 3.9 / 8.1 / 5.9% | 8.9 / 9.5 / 13.7% | 6.6 |
| Gap 20% + both gains 5% (independent) | 3.5 / 4.2 / 6.9% | 3.6 / 8.8 / 6.5% | 10.2 / 12.2 / 15.7% | 6.1 |
| Gap 20% + gauge/FIPEX ratio known to 3% | 7.3 / 6.0 / 7.8% | 7.1 / 11.2 / 8.7% | 11.3 / 11.5 / 14.4% | 5.9 |
| Gap 20% + ratio 3% + low drifts (0.5%/day) | 6.8 / 5.5 / 7.4% | 7.3 / 10.5 / 10.1% | 10.3 / 8.8 / 12.7% | 15.5 |
| Gap 20%, T-mode correlated prior (0.12 + 0.05) | 7.1 / 7.5 / 8.8% | 5.9 / 9.8 / 6.9% | 13.9 / 11.8 / 16.4% | 6.0 |
| Identical twin, old prior | 5.1 / 4.7 / 7.6% | 4.5 / 9.9 / 5.3% | 6.2 / 8.4 / 15.8% | 3.1 |
| Identical twin, gap prior 20% | 5.8 / 6.1 / 6.8% | 5.6 / 8.9 / 7.3% | 6.5 / 10.1 / 13.9% | 3.1 |

### Verdicts

1. **GOOD: the realistic gap prior (20%) roughly halves the fraternal density error** (12–14% → 6–7%) and removes most of the bias (−12% → −2 to −5%). It costs little in the identical twin (5.1 → 5.8% quiet). 20% is the best of 10/20/30 here, and it is defensible from Bruinsma & Laurens 2024 (14.5–27%). **This is the first change to make in `params.py`** (`P0_MSIS_SD`, re-tagged as sourced from the literature, not the twin).
2. **GOOD, strongest lever found: an absolutely calibrated gauge (5%, low drift), i.e. the in-flight argon leak (L9).** Density 3.3–3.5% in all windows on the fraternal truth; O 4–9%; N₂ 9–13%. It beats a better C_D (5%), and beats 5% on both gains without the drift tracking.
3. **BAD: the gauge-to-FIPEX ratio calibration did not help N₂** (3% and 10% ratio give the same result as none). Reason [DERIVED]: the gauge at 300 km is O-dominated. N₂ is only ~20–30% of its signal, so a ratio error is amplified by 1/(N₂ share) ≈ 3–5×: 3% → 10–15% in N₂. The ratio would need to be known to <1%. My algebra in section M is right, but the leverage is poor at 300 km. N₂ should do better at lower altitude and in storms, where its share is larger.
4. **BAD: the physics-correlated (temperature-mode) prior gave no gain** on this truth.
5. **BAD: NEES stays ~6 in every fraternal case, and rises to ~15 with low sensor drift.** The process noise `Q_MSIS_SD` is also twin-derived, so the filter cannot follow the truth's 10% semidiurnal N₂ structure and stays overconfident. Next test: Q from a real error climatology, plus an N₂ local-time term.
6. **N₂ floor.** N₂ stays at 9–15% in every case tried. At 300 km it is limited by the gauge's small N₂ share, not by calibration of any single sensor. Honest composition claim at 300 km: O to ~4–9%, N₂ to ~10–15%, on this (mild) fraternal truth.

### What this means for the proposal

- Lead with: absolute density ~6–7% with drag alone, ~3–4% with a leak-calibrated gauge (fraternal truth, labelled as a sibling model).
- Do not claim in-flight S_O estimation without a ground anchor (E1, M).
- State composition honestly: O better than 10%; N₂ 10–15% at 300 km, improving at lower altitude and in storms.

### Still to run (stopped by the usage limit)

- S_O bank on the fraternal truth with the 20% gap prior.
- Q from a real climatology; N₂ local-time (semidiurnal) state.
- Leak calibration modelled as a daily observation, not a tight prior.
- DTM2020 truth (needs the user's licence decision).
- E2 (biases, consider filter, RTS smoother) and W1–W4 (hardware anchors, bias-aware methods, drag cadence, drift bounds from analogues): agents interrupted, to resume.

## M4. Process noise (Q) on the fraternal truth [TESTED, 100 runs, gap P0 = 0.20; `M1/q_test.py`]

MAE p50, quiet / storm / recovery:

| Case | ρ | O | N₂ | NEES |
|---|---|---|---|---|
| Q ×1 (from M1) | 6.6 / 6.2 / 7.1% | 6.8 / 11.1 / 8.3% | 11.4 / 11.3 / 15.1% | 6.1 |
| Q ×2 | 7.0 / 6.2 / 7.4% | 7.0 / 10.8 / 7.4% | 12.8 / 11.4 / 16.5% | 4.8 |
| Q ×4 | 7.1 / 6.4 / 8.0% | 6.8 / 8.4 / 6.6% | 16.0 / 11.1 / 17.5% | 3.3 |
| Q ×8 | 7.1 / 6.7 / 7.6% | 7.2 / 5.9 / 6.6% | 25.0 / 12.1 / 21.4% | 2.0 |
| Q N₂ ×4 only | 6.6 / 6.2 / 7.6% | 6.7 / 8.5 / 6.0% | 14.0 / 10.8 / 17.4% | 3.1 |
| Q ×4 + leak gauge | 3.3 / 3.2 / 3.5% | 3.9 / 6.6 / 4.8% | 11.0 / 8.4 / 14.3% | 3.6 |
| **Q ×4 + leak gauge + FIPEX drift 0.5%/day** | **3.3 / 3.2 / 3.7%** | **3.8 / 4.1 / 4.5%** | 10.1 / 7.8 / 12.3% | 5.7 |

### Verdicts

- **MIXED: larger Q makes the filter more honest (NEES 6.1 → 2–3) but hurts N₂.** N₂ quiet goes from 11% to 16–25%. More process noise lets gap_N₂ wander, and the gauge's weak N₂ leverage can't pin it down. Q ×2–4 is the reasonable trade.
- **GOOD: best combination so far.** Gap prior 20%, Q ×4, leak-calibrated gauge, FIPEX drift ≤0.5%/day:
  - density 3.2–3.7% in all windows
  - O 3.8–4.5% in all windows
  - N₂ 8–12%
  - on the fraternal truth
- **BAD: N₂ remains the weak product** at ~8–12% (above 10% in quiet and recovery). The fix has to be physics or hardware: more N₂ leverage (W1's ideas), lower altitude, or a ram-chamber model.
- The remaining NEES is in gap_N₂ (2.6–3.3). Every other state is now honest (0.5–1.8).

---

## R1. External research: MAG084 atomic-O response (user's research AI, Nov 10)

Full brief: the user's upload `MAG084_Atomic_Oxygen_Research.md` (37 references). Verdict: **BAD for certainty, GOOD for defensibility.** No direct S_O measurement exists for the MAG084 or any comparable gauge; no MAG084 drift rate exists. But we now have traced sources for every bracket we use, and a list of known issues to name in the proposal.

### What changes for us

1. **The S_O bracket is now traced, not assumed.**
   - Lower end ~0.51: O/N₂ ionization cross-section ratio at 70 eV (Laher & Gilmore 1990 JPCRD 19:277 for O; NIST BEB for N₂). It ranges 0.51–0.64 over 25–200 eV, and a discharge gauge has a broad electron distribution.
   - Upper end ~0.71: full O → O₂ recombination in the chamber gives S_O₂/√2 = 0.707 (O₂ leaves √2 slower; Newton & Horowitz 1969, NASA TN D-5447, App. A).
   - The old "0.77" upper end is **untraced**. Replace it with 0.71.
   - **Gettering or adsorption can push the response below 0.5** (Geoprobe: Bayard–Alpert gauges removed nearly all O; Pelz & Newton 1967).
   - Our `SO_SD` = 0.16 around 0.56 still covers 0.5–0.71 within 2σ (ln: −0.11 / +0.24). Keep the value; change the source text.
2. **Gas factors: INFICON-adjacent values** (IKR084/085/086 manual, low-pressure region): He S = 0.169 (we use 0.18), Ar 1.25 (we use 1.29), O₂ 1.0 (we use 1.01). No atomic O, N or H factors exist. The differences are small; cite IKR as the closest-product source.
3. **Ram formula confirmed.** The brief derives the same equation (Grabe et al. 2010, DLR): O 48.9× and N₂ 64.7× at 300 K wall. Wall temperature: 10 K error ≈ 1.7%. Pointing: 10° → 1.5%, 30° → 13.4%. These go into the C7 stress tests.
4. **The N₂ amplification formula matches our identifiability finding:** δN₂/N₂ = −(a_O n_O / a_N n_N₂)(δa_O/a_O). A 10% O-response error gives 19% N₂ error at O/N₂ = 5.

### Known issues to carry (name each in the proposal with a mitigation)

| # | Issue | Our handling now | Mitigation / when |
|---|---|---|---|
| K1 | S_O never measured; 0.5–0.71, could be lower (gettering) | Consider analysis, `SO_SD` 0.16 | Ground O-beam test of the **assembled** chamber + gauge (Phase 2); parked S_O stage |
| K2 | O recombination and reaction products (CO, CO₂, H₂O) make S_O time-dependent; exposure conditioning (Cross 1995) | Not modelled | Pre-conditioning; slow S_O random walk in month 1; separate parameters (survival, products) in Phase 2 |
| K3 | Gauge nonlinearity I ∝ p^N, N ~1.1–1.4 historically; mode jumps (Li & Jousten 2003) | Gauge modelled log-linear | Calibration curve from INFICON; outlier/step handling (Phase B robustness) |
| K4 | Ignition delay: 6 s at 1e-7, 60 s at 1e-8, 300 s at 1e-9 mbar (IKR manual) | Not modelled | Keep the discharge on; gap handling (Phase B robustness) |
| K5 | Discharge pumping: steady density × C/(C + S_p) | Folded into gain | Known orifice conductance; ground test |
| K6 | Leak gas bypassing the inlet calibrates a different transfer function | `LEAK_NOISE` 5% | Add a geometry/transmission term; inject through the inlet path if possible |
| K7 | Same-beam gauge + FIPEX calibration gives only a relative transfer (with power-law response) | — | State as a relative calibration in the cal/val plan |
| K8 | Chamber wall temperature and pointing errors | Assumed known | C7 stress tests (1.7%/10 K, 1.5%/10°) |
| K9 | Spacecraft-generated background (Apollo CCGE: day contamination ~100× night) | L8 budget: negligible at 300 km after ~1 day | Shutter/wake zero checks; mech rules (L8) |
| K10 | No MAG084 drift data | `GAUGE_DRIFT_SD` assumption + Phase A sweep | Requirement ≲0.5%/day from Phase A; leak tracking |
| K11 | FIPEX drift; response power law n^0.35 | Linear model + drift sweep | User's FIPEX research doc at the parked stage |

### INFICON questions (highest value first)

1. Any atomic-O beam data on the MAG084 or its electrodes.
2. The exact current-to-pressure relation, and whether the IKR gas factors apply.
3. The I(p) calibration curve and its modes.
4. Whether O₂/N₂ mixtures add linearly.

(Full list of 12 in the brief.)

---

## B-robust. Gaps, outliers, NIS gate [TESTED by the user, 100 runs, fraternal truth, consider mode, ram gauge, filter only]

| Case | ρ quiet / storm / recovery | quiet N₂ | storm O | NEES | rej gauge / FIPEX |
|---|---|---|---|---|---|
| clean, no gate | 8.1 / 8.0 / 10.4% | 18.9% | 8.5% | 1.36 | 0 / 0 |
| clean, gate 15.1 | 8.1 / 8.1 / 10.4% | 18.8% | 8.6% | 1.35 | 1e-4 / 1e-4 |
| gaps | 9.3 / 8.4 / 10.1% | 19.6% | 8.1% | 1.43 | 1e-4 / 1e-4 |
| outliers 1e-3 × 0.3, no gate | 8.4 / 7.6 / 11.3% | 21.1% | 8.3% | 1.42 | 0 / 0 |
| outliers, gate | 8.4 / 7.8 / 11.1% | 20.6% | 8.2% | 1.43 | 5e-4 / 7e-4 |
| gaps + outliers, gate | 7.6 / 7.1 / 9.9% | 19.3% | 8.6% | 1.49 | 4e-4 / 7e-4 |

- **GOOD:** the clean, no-gate case reproduces the ram/consider row exactly.
- **GOOD, strong evidence of honest uncertainty:** in clean runs the gate rejects 1.0e-4 of readings. That is exactly the false-alarm rate chi-square predicts for p = 1e-4, which it only does if the innovations are correctly scaled.
- **GOOD: robust to gaps** (density +1 point at worst) **and to outliers** (+1–2 points N₂). Run-to-run noise at 100 runs is about ±1 point, which is why gaps + outliers looks slightly better than gaps alone.
- **BAD (understood): the gate catches only about half the gauge spikes**, and an uncaught spike then knocks out good FIPEX readings (rej_o 1e-4 → 7e-4).
  - Cause [DERIVED]: the consider S_O term adds a permanent (O share × 0.16)² ≈ 0.006 to the gauge innovation variance, so √S ≈ 0.08. A 0.3 spike is then only ~3.7σ, under the 3.9σ gate.
  - That term is a constant bias, not step-to-step noise.
  - **Fix (design, no code needed now):** form each 30 s product as the **median** of the ~30 raw 1 Hz samples, not the mean. That removes isolated spikes before the filter sees them, and is standard robust preprocessing. Longer mode jumps are level shifts, handled as gain changes (K3).
- **Defaults:** `GAPS=True` (conservative), gate on, `OUTLIER_RATE=0` (median preprocessing argued). Phase B core is complete.

---

## W3. Drag anchor: cadence and C_D realism (agent, research only; PDF text in scratch `night2/W3/`)

**Verdicts:**
- **GOOD:** at 250–350 km, GPS drag can give density about once per orbit (~5% dual-frequency, ~15% single-frequency), not just daily.
- **BAD:** the absolute level does not improve past the C_D floor (~5% with known geometry and attitude; 10–25% unknown). Better GPS doesn't fix it; only physics C_D does.
- Orbit-resolved drag adds almost no composition leverage (section M).

**Random (non-C_D) density error at 300 km [DERIVED from the anchors below]:**

| Window | Dual-frequency (2–5 cm orbits) | Single-frequency CubeSat (0.3–1 m) |
|---|---|---|
| 10 min | 5–30% | unusable |
| 1 orbit | 4–8% | 10–25% |
| 3 h | 3–6% | 7–15% |
| 1 day | 2–4% | 5–9% (Lowe & D'Amico 2026) |

Altitude scaling ∝ 1/ρ: about 3× better at 250 km, about 5× worse at 400 km. White-noise floor [DERIVED]: σ_a ∝ σ_r·N^−½·T^−2.5; at an orbit or longer, receiver noise is negligible and correlated orbit and force-model errors dominate.

**Anchors:**
- Ray et al. 2023 (AMOS): POD-accelerometry <10% for windows ≤8 h; EDR needs >1e-6 m/s² and <2.5 cm noise.
- van den IJssel et al. 2020 (ASR 65:1758, doi:10.1016/j.asr.2020.01.004): Swarm GPS densities at ~20 min.
- Constant et al. 2024 (arXiv:2408.16805): short-window absolute values are no better than a model across 45 storms (median error 27.8% POD-accel vs 21.5% NRLMSISE-00); their value is tracking changes.
- Bowman & Moe 2005 (AAS 05-257): daily EDR 2–4% at solar max.

**C_D realism:**
- Moe & Bowman 2005 (AAS 05-258) sphere tables at 300 km: accommodation α 0.93 → 0.98 and C_D 2.31 → 2.18 (solar min → max). d ln C_D/dα ≈ −1.2.
- Storm drop in O → C_D +2–5% at 300 km [DERIVED; Langmuir-form coverage; K unconfirmed].
- Within-orbit ±10% at 450–500 km (March et al. 2021 JSWSC 11:54, doi:10.1051/swsc/2021035).
- Attitude changes C_D by tens of %.
- **In-flight α calibration by yaw slews**, as Swarm May 2014 did (α 0.80–0.90, March 2021). This works below ~450–500 km at high activity, which is our regime. Propose deliberate yaw manoeuvres.
- Achievable C_D: spheres ~3%; known host geometry and attitude 4–5%; unknown 10–25%.

**Recommended model:**
- Drag reading = ln(window-mean ρ) + ln C_D error + ε; per-orbit window, ε 5% (dual) or 15% (single); fallback daily 6%.
- C_D truth = constant bias + O-adsorption term + slow random walk 1%/day.

**Hardware notes:**
- NovAtel OEM719: 31 g, 1.3 W, L1/L2.
- MEMS/servo accelerometers: bias 20–60× the drag signal, so not an absolute anchor.
- TLE global average (Emmert 2009) and Starlink ephemerides (550 km): validation only.

**Proposal wording (draft):** "Host GPS drag gives density every orbit (~5% dual-frequency). Its absolute level is set by a physics-based C_D (O-adsorption accommodation, α calibrated by yaw manoeuvres, March et al. 2021), about 5% with known host geometry: the mission's absolute density datum."
