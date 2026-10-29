# OSSE / Monte Carlo methods for ranking thermospheric sensor suites, deriving requirements, and choosing an altitude range

Scope note: the research ran under a tight tool budget (about 20 calls). Several primary PDFs (Dietrich et al. 2024 full text, Bruinsma et al. 2021 full text, Crisp et al. 2020 VLEO paper) could not be text-extracted or returned HTTP 403, so some numbers below come from search-result abstracts only. Items under "Inferences" that rely on standard textbook physics are marked as such and should be checked against an NRLMSIS 2.0/2.1 run in the team's own code before quoting them.

---

## 1. Published thermospheric/ionospheric OSSEs and how they are designed and scored

### Takeaway
The best published template is Dietrich et al. (2024, Space Weather). It used TIEGCM with a DART EnKF and 10 constellation configurations: 6 or 12 satellites, 520 or 800 km, 24° or 72° inclination. Its main result was that observation count and coverage drive skill: the mixed-inclination 520 km design won. For neutral density, the de facto scoring standard is Bruinsma et al.: observed-to-computed (O/C) density ratios, giving the mean ratio (bias), the standard deviation of the ratio (precision), and correlation. Storms are scored in 4 phases tied to minimum Dst, after de-biasing on the pre-storm phase.

### Cited Findings
**Dietrich et al. 2024, RO constellation OSSE (ionosphere, with a neutral-state spin-off)**
- Title: "Evaluating Radio Occultation (RO) Constellation Designs Using OSSEs for Ionospheric Specification". DOI 10.1029/2024SW003958. Authors are Dietrich, Matsuo, C.-Y. Lin, diLorenzo, C. C.-H. Lin and Fang (CU Boulder, NCU, NCKU, NOAA SWPC). — [NSF PAR](https://par.nsf.gov/servlets/purl/10608384); [ESS Open Archive preprint](https://essopenarchive.org/doi/full/10.22541/essoar.171412587.76701024/v1)
- Design: 10 RO constellation configurations, each with 6 or 12 LEO satellites, base altitude 520 or 800 km, and inclination 24° or 72°. Synthetic electron density profiles (EDPs) go into a coupled I-T model (TIEGCM) using the Ensemble Adjustment Kalman Filter in DART. — [NSF PAR](https://par.nsf.gov/servlets/purl/10608384)
- The paper says it is the first to fully account for forecast model error and Abel inversion error. In other words, the observation operator includes the retrieval error and is not idealized. — [NSF PAR](https://par.nsf.gov/servlets/purl/10608384)
- Result: wider EDP spatial coverage improves specification at 300 km and above. The constellation that combined low- and high-inclination orbits at 520 km did best, because it produced the most observations. — [NSF PAR](https://par.nsf.gov/servlets/purl/10608384)
- The same group found that using EDPs to update neutral states directly cut neutral temperature errors by about 70% and neutral wind errors by about 20%. — [NSF PAR search summary](https://par.nsf.gov/search/author:%22Dietrich,%20Nicholas%22)
- Dietrich's PhD thesis ("Physics-Based Approaches for Neutral Density Specification and UQ through Data Assimilation") extends this to neutral density through strongly coupled I-T assimilation and includes a full OSSE. — [CU Scholar](https://scholar.colorado.edu/downloads/8w32r784x)

**Constellation and coverage density estimation**
- MIT real-time density estimation (Gondelach & Linares 2020). It used TIE-GCM output as the "truth" density and estimated with a reduced-order model plus a sigma-point (unscented) Kalman filter. Results are reported for scenarios with different numbers of satellites, such as 5-orbit and 10-satellite cases. This is a fraternal-twin design: truth from TIE-GCM, a different estimator model, and observations from satellite positions. — [MIT DSpace](https://dspace.mit.edu/bitstream/handle/1721.1/135426/J25_2020.pdf?sequence=2&isAllowed=y)
- Gondelach & Linares 2021 (Space Weather): real-data assimilation of radar range and range-rate from 20 objects plus GPS positions from 10 commercial satellites, validated against Swarm densities. This shows a tens-of-objects scale is enough to constrain a reduced-order global model. — [MIT DSpace](https://dspace.mit.edu/bitstream/handle/1721.1/145414/Space%20Weather%20-%202021%20-%20Gondelach%20-%20Real%E2%80%90Time%20Thermospheric%20Density%20Estimation%20via%20Radar%20and%20GPS%20Tracking%20Data%20Assimilation.pdf?isAllowed=y&sequence=2)
- A US patent on in-situ density measurement simulated a Walker constellation estimating density plus spherical-harmonic coefficients. Density errors were under 1% of the largest density at each altitude, and error peaks fell in the largest gaps of the Walker constellation, so skill tracks coverage gaps directly. — [USPTO 11242162](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11242162)
- A Kyoto University study used public orbit data for about 1,200 Starlink satellites and tomography to make 2-D latitude/longitude density maps at about 482 km. This is a fleet-as-sensor proof of concept. — [summary](https://book.st-hakky.com/en/news/starlink-satellites-map-upper-atmosphere)
- Fitzpatrick et al., AMOS 2024 (CU Boulder): uncertainty in neutral density modeling and estimation is the main source of orbit-prediction error. — [AMOS 2024](https://amostech.com/TechnicalPapers/2024/Atmospherics_Space-Weather/Fitzpatrick.pdf)

**Mutschler / Spire / commercial assimilation**
- Mutschler, Axelrad & Matsuo (2020, Adv. Space Res.) "A Partially Orthogonal EnKF approach to atmospheric density estimation using orbital debris". It estimates density parameters jointly with the orbits of many debris objects, and the achievable density accuracy depends on measurement and sensor error. The search snippet gave no percentage. — [AMOS 2017 poster, Mutschler](https://amostech.com/TechnicalPapers/2017/Poster/Mutschler.pdf)
- Mutschler (SET) et al., "Solari", a commercial data-assimilative density model. It corrects a background model using LeoLabs radar tracking and Energy Dissipation Rates (EDRs). SBIR Phase I ended Feb 2025, Phase II began Aug 2025, and an initial version is due Aug 2027. — [COSMIC/UCAR abstract 2025](https://www.cosmic.ucar.edu/sites/default/files/2025-08/Mutschler_Abstract.pdf)
- IAC-24 paper: Spire constellation POD data will produce density estimates for assimilation, validated against historical HASDM. — [IAC-24 D5.3.3](https://iafastro.directory/iac/paper/id/82218/abstract-pdf/IAC-24,D5,3,3,x82218.brief.pdf)
- The Sutton CSDAP pilot found that day-to-day thermospheric variability can be extracted from Spire CubeSat GNSS POD. Densities agreed from satellite to satellite and followed HASDM trends, but validation was limited by scarce reference data and by low duty cycles early on. — [NASA Earthdata CSDAP pilot](https://www.earthdata.nasa.gov/sites/default/files/imported/CSDAP-Pilot-Sutton.pdf); [CPAESS 2020 presentation](https://cpaess.ucar.edu/sites/default/files/meetings/2020/presentations/mccarty-presentation.pdf)
- A physics-based assimilation of GNSS-POD-derived densities from small satellites. — [ESSOAr preprint](https://essopenarchive.org/doi/full/10.1002/essoar.10506143.2)

**Scoring framework (Bruinsma et al.)**
- Bruinsma, Sutton, Solomon, Fuller-Rowell & Fedrizzi (2018), "Space weather modeling capabilities assessment: Neutral density for orbit determination at LEO", Space Weather 16, 1806–1816. It was an initial, explicitly incomplete CCMC/ISWAT assessment covering NRLMSISE-00, JB2008, DTM2013, TIE-GCM and CTIPe. — [SWSC 2021 abstract page](https://www.swsc-journal.org/articles/swsc/abs/2021/01/swsc200061/swsc200061.html); [CCMC ISWAT G2A-01](https://ccmc.gsfc.nasa.gov/iswat/G2A-01)
- The metric comes from Bruinsma, Arnold, Jäggi & Sanchez-Ortiz (2017, GOCE). It uses the mean, standard deviation and RMS of the observed-to-model (O/C) density ratios, plus correlation. — [Bern BORIS](https://boris.unibe.ch/97761/)
- Storm extension (Bruinsma et al. 2021, SWSC, doi 10.1051/swsc/2021002):
  - Each storm is split into 4 phases relative to the time of minimum Dst: pre-storm, main, recovery and post-storm.
  - The O/C ratio in the pre-storm phase gives a scale factor. That factor de-biases the model in all four phases, which isolates storm-response skill from background bias.
  - Mean ratio, standard deviation and correlation are then computed per phase. — [SWSC](https://www.swsc-journal.org/10.1051/swsc/2021002)
- Bruinsma 2021 results: 13 storms, scored against CHAMP, GRACE and GOCE.
  - Every model degrades in storms, mainly through much larger standard deviations.
  - DTM2013, JB2008 and CTIPe show no significant average bias in any phase.
  - DTM2013 and TIE-GCM (Weimer-driven) are best over the whole storm.
  - NRLMSISE-00 underestimates storm densities systematically and significantly. — [SWSC](https://www.swsc-journal.org/10.1051/swsc/2021002)
- Eric Sutton's CCMC 2018 metrics talk is the origin presentation for the CCMC density metrics. — [CCMC PDF](https://ccmc.gsfc.nasa.gov/publicData/workshops/2018/03_Wednesday_PM/3c.EricSuttonCCMC_metrics_2018.pdf)

**HASDM benchmarks (what "good" looks like)**
- SET HASDM database assessment: mean absolute differences of 23.81% against CHAMP and 30.84% against GRACE-A accelerometer densities. HASDM matched these more closely than the empirical models compared. — [ESS Open Archive](https://essopenarchive.org/users/542408/articles/608441-qualitative-and-quantitative-assessment-of-the-set-hasdm-database)
- SWSC 2021 table: the standard deviation of yearly-mean density ratios for HASDM at 400 km is about 5.0% (vs JB2008) and 6.8% (vs DTM2013). The table notes partial exclusion of 2018–2019. — [SWSC table](https://www.swsc-journal.org/articles/swsc/full_html/2021/01/swsc210039/T2.html)
- HASDM assimilates tracking of about 90 calibration objects and is available in real time only to government users. That restriction motivates commercial alternatives. — [ESSOAr summary context](https://essopenarchive.org/doi/full/10.1002/essoar.10506143.2); [arXiv 2209.05597](https://arxiv.org/pdf/2209.05597)
- Swarm-C validation (2026, Chinese J. Space Sci.): mean bias about 12.5% with standard deviation of about 0.2 in the ratio during moderate-to-high solar activity, and a larger bias at low activity. — [CJSS 2026](https://cjss.ac.cn/en/article/doi/10.11728/cjss2026.01.2025-0012)
- NRLMSISE-00 calibrated with an EnKF (75 members) against GRACE accelerometer densities at about 410 km, then fed to TIE-GCM. This is a real-data analog of the team's "NRLMSIS + filter" architecture. — [Sci. Rep. 2022](https://www.nature.com/articles/s41598-022-05952-y)
- Assimilating accelerometer densities mainly improves densities near the satellite's own orbit. This is the vertical-representativeness problem for a single-altitude in-situ fleet. — [ResearchGate two-step assimilation](https://www.researchgate.net/publication/366156651_Improving_the_estimation_of_thermospheric_neutral_density_via_two-step_assimilation_of_in_situ_neutral_density_into_a_numerical_model)

### Inferences
- The team's OSSE should report the Bruinsma metric set so judges recognize it: mean O/C ratio, standard deviation of O/C (better in log space, ln(O/C)), correlation, and RMS. Score quiet periods separately from storms, and score storms with the 4-phase, pre-storm de-biased scheme. This maps cleanly onto the OCC "accuracy (bias) vs precision (scatter)" benchmark split.
- Useful baselines: HASDM gets roughly 5–7% std of yearly-mean ratio and roughly 24–31% mean absolute difference against accelerometers. NRLMSISE-00 is systematically low in storms. Targets "beats NRLMSIS by X% in storm main phase" and "approaches HASDM-class scatter" are both defensible framings.
- Dietrich's design is a ready-made factorial template: n_sats × altitude × inclination, with the observation operator's retrieval error included. Swap RO EDPs for in-situ density, pressure or drag sensors.

### Gaps
- Full-text quantitative results of Dietrich 2024 (RMSE reduction per configuration) were not extracted; the PDF was not text-readable in this environment.
- The "Spire/Mutschler OSSE (5–25% error)" figure in the brief was not found in any source. Searches turned up Mutschler's EnKF debris work, Solari, and Spire POD density pilots, but no OSSE reporting 5–25%. Treat that number as unverified until the primary paper is located.
- No source was found for the "AGU 2022 satellite coverage for density estimation" study by that description.
- WAM-DA validation metrics were not retrieved.

---

## 2. Best practices for OSSE credibility

### Takeaway
Using NRLMSIS as both truth and filter background is the classic "identical twin". Weather and ocean OSSE literature shows this overstates the benefit of new observations. Credible designs use a fraternal or different-model truth (TIE-GCM, WAM, DTM/JB2008-driven, or real CHAMP/GRACE/GOCE/Swarm densities) and a degraded estimator. They also calibrate the simulated sensor error model against real instrument data.

### Cited Findings
- The identical-twin problem: if the same model generates the observations and tests their effectiveness, the OSSE is overly optimistic and can reach wrong conclusions. — [NOAA repository OSSE document](https://repository.library.noaa.gov/view/noaa/27196/noaa_27196_DS1.pdf); [Atlas et al. 2015 MTS OSSE](https://www.aoml.noaa.gov/ftp/hrd/gopal/Latest_HWRF_PUBLICATIONS/Atlas-etal-MTS-OSSE-2015.pdf)
- Standard remedy: assimilate and forecast with a different model, usually one with lower accuracy and resolution than the nature run, so that realistic model error is present. — [ams.confex OSSE paper](https://ams.confex.com/ams/pdfpapers/30633.pdf); [Atlas CGMS](https://cgms-info.org/html/iww6/session5/Atlas1.pdf)
- Hoffman & Atlas (2016, BAMS, "Future Observing System Simulation Experiments") as cited by others:
  - OSSEs are a rigorous, cost-effective way to evaluate new observing systems and alternative deployments.
  - For quantitative accuracy, every OSSE component must be realistic: nature run, simulated observations and their errors, and the DA system. — [Copernicus OS 2019 supplement citing Hoffman & Atlas](https://os.copernicus.org/preprints/os-2019-85/os-2019-85-AC1-supplement.pdf)
- Halliwell et al. 2014 validated a fraternal-twin ocean OSSE: same model type, differently configured. A related study found identical twins overestimate error reduction from some observation types and underestimate it from others. The bias is observation-type-dependent, which makes it dangerous for ranking sensor suites. — [Halliwell 2014](https://www.aoml.noaa.gov/phod/docs/Halliwell_2014.pdf)
- A thermosphere precedent for a fraternal design: TIE-GCM as truth with a reduced-order estimator. — [MIT DSpace](https://dspace.mit.edu/bitstream/handle/1721.1/135426/J25_2020.pdf?sequence=2&isAllowed=y)
- Truth-data options with documented accuracy: CHAMP, GRACE and GOCE accelerometer densities (used by Bruinsma 2021), and Swarm-C. — [SWSC](https://www.swsc-journal.org/10.1051/swsc/2021002); [CJSS 2026](https://cjss.ac.cn/en/article/doi/10.11728/cjss2026.01.2025-0012)
- MSIS also misrepresents composition structure. CHAMP/GRACE helium near 500 km in winter at solar minimum ran well above MSIS predictions. A "truth" that differs from MSIS in composition is therefore physically realistic. — [AGU FM14 helium tracer](https://agu.confex.com/agu/fm14/webprogram/Paper2496.html)
- The OCC technical guidelines separate accuracy, precision and resolution (time cadence, or horizontal and vertical resolution for remote sensing). — [OCC Technical Guidelines](https://occ.nasatechleap.org/technical-guidelines/)

### Inferences
Recommended credibility ladder for the team:
- **(a) Identical twin.** NRLMSIS truth and NRLMSIS background. Use it only for code verification and as an upper bound.
- **(b) Perturbed-driver fraternal twin.** NRLMSIS truth driven with real F10.7/Ap. The filter's NRLMSIS gets smoothed, lagged or forecast drivers plus a stochastic multiplicative density field with correlation lengths of a few thousand km and hours. This is cheap on GPU for 100k Monte Carlo runs.
- **(c) Different-model truth.** JB2008 or DTM2013 (cheap empirical, GPU-able), or archived TIE-GCM/WAM runs.
- **(d) Real-data truth.** TU Delft CHAMP/GRACE/GRACE-FO/Swarm densities along their tracks, scored with the Bruinsma metrics. Rank sensor suites with (b) and (c). Report (a) only as a ceiling, and show that rankings are stable across (b), (c) and (d).

Sensor error model calibration:
- Draw gain, drift and noise priors from lab or flight heritage, not guesswork. Examples: ionization-gauge gain spread, temperature coefficient, outgassing transient, and accommodation-coefficient uncertainty for drag-derived density.
- Include a per-unit gain distribution and a time-varying drift. These are what make cross-calibration matter.

Reporting:
- Accuracy is the mean of ln(O/C), the bias after the filter.
- Precision is the standard deviation of ln(O/C) at native cadence.
- Resolution is the effective time or along-track scale. Estimate it from the filter's averaging kernel or the PSD of error vs truth.
- Report each against the OCC table (density: 20% accuracy, 10% precision, 30 s).

### Gaps
- The Hoffman & Atlas 2016 BAMS paper itself was not retrieved; its points come from secondary citations.
- No thermosphere-specific study quantifying how much identical-twin OSSEs overstate density-improvement was found.
- TU Delft density dataset version and accuracy specs were not retrieved in this pass.

---

## 3. Methods for deriving requirements from Monte Carlo

### Takeaway
No published thermosphere paper was found that derives in-situ sensor requirements with Sobol indices. The generic approach is mature, though. Use Saltelli-sampling Sobol indices (first-order and total) to rank which error terms (gain, drift, noise, host attitude, accommodation, coverage) drive density-estimate variance. Use Morris screening first to prune, then use spec sweeps to set thresholds. Fold the results into a weighted decision matrix with cost and SWaP.

### Cited Findings
- Sobol indices decompose total output variance D = Var[f] into contributions from individual inputs and their interactions, and are estimated by Monte Carlo. — [arXiv 1612.08423 (orbit UQ with Sobol)](https://arxiv.org/pdf/1612.08423)
- Saltelli sampling builds an unbiased, optimized sample of parameter space. Estimators typically use n+2 sample matrices to get both main (first-order) and total effects. — [arXiv 2509.07066](https://arxiv.org/pdf/2509.07066); [IDEAS/RePEc](https://ideas.repec.org/a/eee/reensy/v263y2025ics0951832025004375.html)
- Space-systems use: in a telecom-satellite multidisciplinary design study, total-order Sobol indices filter out low-impact uncertain variables, reducing the size of the design-under-uncertainty problem. This is the requirements-flowdown analog. — [arXiv 2607.19045](https://arxiv.org/pdf/2607.19045)
- A 2026 tether-net debris-capture study uses Sobol indices to rank which noisy-observation inputs drive outcomes, reusing a subset of the Monte Carlo dataset. Indices can be computed from existing Monte Carlo runs. — [arXiv 2606.07580](https://arxiv.org/pdf/2606.07580)
- Monte Carlo Sobol estimates carry their own sampling error (Sobol & Shukhman 2007), so small indices need confidence intervals before being treated as real. — [Unpaywall record](https://unpaywall.org/10.1515%2FMCMA.2007.005)
- Mutschler et al. 2020 found that density-estimate accuracy depends on measurement and sensor error. This qualitatively motivates a spec sweep. — [AMOS 2017 Mutschler](https://amostech.com/TechnicalPapers/2017/Poster/Mutschler.pdf)
- The OCC Phase 1 rubric scores four criteria, 1–5 each, with no published weights:
  - Relevance: density plus composition over "a clearly identified and extensive altitude regime", with evidence of improved model accuracy.
  - Performance: test data, a calibration plan, and realistic uncertainty.
  - Cost/scalability: unit cost "dramatically lower", plus a manufacturing method.
  - Flight readiness.
  The rubric never mentions simulation, so the OSSE must be framed as evidence for Relevance and Performance. — [OCC Evaluation Criteria](https://occ.nasatechleap.org/evaluation-criteria/)
- Phase 2 asks for documented "trade studies and rationale", worth 25 of 100 points. A Monte Carlo-backed trade study maps directly onto this. — [OCC Evaluation Criteria](https://occ.nasatechleap.org/evaluation-criteria/)
- OCC benchmarks are "target floors, not fixed requirements", and applicants may propose other targets with justification. — [OCC Technical Guidelines](https://occ.nasatechleap.org/technical-guidelines/)

### Inferences (recommended workflow for a 100k-run GPU Monte Carlo)
1. **Morris screening.** Use about 20 trajectories × (k+1) runs over all roughly 15–30 error and environment factors: noise σ, gain bias, gain drift rate, temperature coefficient, accommodation coefficient, attitude knowledge, timing, outages, host count, altitude, inclination, solar/geomagnetic regime, and filter Q/R mis-scaling. Drop factors with negligible μ* and σ.
2. **Sobol on survivors.** Saltelli/Jansen estimator with N ≈ 2^12–2^14 base samples × (k+2). For k = 8 that is about 40k–160k runs, which fits the 100k GPU budget. Compute S1 and ST with bootstrap CIs. Use log-error metrics, such as RMS of ln(O/C) and storm-phase std, as outputs. Run them separately for quiet and storm regimes, because the drivers differ.
3. **Spec sweeps.** For the 2–3 dominant factors, sweep one dimension at a time or on a 2-D grid. Find the "knee" where the system metric crosses the OCC floor, such as 10% precision. That value becomes the derived instrument requirement plus margin, typically 1.5–2×.
4. **Tolerance allocation.** Split the total error variance budget across factors in proportion to their Sobol shares and to cost-to-improve. Tighten the cheap-to-improve factors first.
5. **Robustness to filter mis-specification.** Deliberately mis-set the EKF R (×0.5, ×2) and Q, and ignore drift states in some runs. Report the degradation, and check NEES/NIS consistency. A suite whose ranking flips under mis-specification is fragile.
6. **Decision matrix.** Columns are simulated metrics (quiet RMS, storm-main-phase std, correlation, altitude coverage), unit cost, mass, power, volume, TRL, and contamination sensitivity. Map the weights onto the OCC Phase 1 criteria (Relevance, Performance, Cost/Scalability, Flight readiness). Show rank stability under weight perturbation, for example with Dirichlet-sampled weights.

### Gaps
- No thermosphere- or space-weather-specific example of Sobol- or Morris-based instrument requirement derivation was found.
- Saltelli's primer (Global Sensitivity Analysis: The Primer, 2008) and Morris (1991) were not retrieved but are the standard references.

---

## 4. Altitude-range drivers

### Takeaway
OCC defines VLEO as below 300 km and LEO as 300–800 km. Each applicant must state the altitude range where it meets performance. The rubric rewards an "extensive" altitude regime plus composition, but no specific band gets bonus points. Commercial VLEO hosts sit at about 250–380 km: Albedo operated at 350–380 km with a 274–275 km design, and Skeyeon targets about 250 km within a 180–350 km patent envelope. Lifetimes at 400 km range from months to years with solar activity. The He/O transition (about 450–500 km, lower in winter at solar minimum) is where storm density perturbations peak and where composition assumptions break drag-based density inversion.

### Cited Findings
**OCC rules**
- Benchmarks:
  - In-situ mass density, LEO or VLEO: accuracy 20% or better, precision 10% or better, resolution 30 s or faster.
  - Neutral pressure: 20% accuracy, 5% precision, 30 s.
  - Drag acceleration: 5% accuracy, 1% precision, 10 s.
  - Remote sensing (VLEO 90–300 km): 10% accuracy and precision, 5° horizontal and 10 km vertical resolution.
- Regime definitions are VLEO below 300 km and LEO 300–800 km. The rules require: "identify the regime and altitude range where its solution meets its stated performance".
- Solution requirements: hosted payloads only, at least 100 units, operation of at least 1 year, and contamination tolerance. Inclination and ground contact are undefined, so teams must state assumptions and show robustness. — [OCC Technical Guidelines](https://occ.nasatechleap.org/technical-guidelines/)
- The top Relevance rating requires density plus composition over "a clearly identified and extensive altitude regime". — [OCC Evaluation Criteria](https://occ.nasatechleap.org/evaluation-criteria/)
- Dates: Phase 1 registration closes 28 Oct 2026, submissions close 11 Nov 2026, and winners are announced Jan 2027. Up to 4 winners, up to $500k total each, and a no-cost flight test. — [occ.nasatechleap.org](https://occ.nasatechleap.org/); [NASA page](https://www.nasa.gov/directorates/stmd/prizes-challenges-crowdsourcing-program/nasa-techleap-prize-orbital-clarity-challenge/)

**Commercial VLEO hosts**
- **Albedo Clarity-1.** The constellation is designed for a 274 km circular orbit, with Clarity-1 planned at 320 km after thrusting down from 510 km through about 350 km. — [Albedo newsletter Jun 2025](https://albedo.beehiiv.com/p/bedo-newsletter-june-25)
  - The January 2026 retrospective says the satellite was measured multiple times at 350–380 km. Albedo says this supports a modeled 5-year lifespan at 275 km averaged over the solar cycle. — [Albedo blog](https://albedo.com/post/clarity-1-what-worked-and-where-we-go-next)
  - Launched 17 Mar 2025 on Transporter-13. — [BusinessWire](https://www.businesswire.com/news/home/20250317584103/en); [SatNow](https://www.satnow.com/news/details/3020-albedo-s-clarity-1-satellite-launched-to-orbit-on-spacex-s-transporter-13-rideshare-mission)
  - Wikipedia reports about 9 months of operation, then loss of comms, then uncontrolled decay through VLEO and reentry on 10 Jun 2026. This was not confirmed against a primary source. — [Wikipedia](https://en.wikipedia.org/wiki/Albedo_Space)
- **Skeyeon.** Its March 2026 patent covers VLEO at 180–350 km. — [BusinessWire Mar 2026](https://www.businesswire.com/news/home/20260324011028/en/Skeyeon-Secures-Key-Patent-for-Very-Low-Earth-Orbit-Satellite-Constellations-with-Onboard-Imaging-and-Direct-to-Ground-Data-Delivery-Enabling-Near-Real-Time-Earth-Observation)
  - SpaceNews coverage cites a constellation at about 250 km. — [EvoNexus/SpaceNews](https://evonexus.org/evonexus-portfolio-company-featured-on-the-cover-of-space-news/)
  - A 2016 patent covered 100–350 km. — [Wikipedia VLEO](https://en.wikipedia.org/wiki/Very_low_Earth_orbit)

**Lifetime and decay**
- At 400 km, lifetime ranges from about 3 months (low ballistic coefficient, high solar flux) to over 8 years (high ballistic coefficient, low flux). — [Crisp et al., arXiv 2007.07699](https://arxiv.org/pdf/2007.07699)
- Any satellite below 450 km has a post-mission lifetime under 25 years regardless of solar conditions. — [Crisp et al., arXiv 2007.07699](https://arxiv.org/pdf/2007.07699)
- At 400–500 km, lifetime is several years at solar minimum but only a fraction of that at solar maximum. — [arXiv 2508.19549](https://arxiv.org/pdf/2508.19549)
- MinXSS 3U CubeSat: below 620 km meets the 25-year rule. — [arXiv 1508.05354](https://arxiv.org/pdf/1508.05354)
- The FCC 5-year LEO deorbit rule applies. For a 1U CubeSat the lifetime is strongly launch-date dependent: 0.44 years for a 2022 launch vs 6.4 years for a January 2026 launch. — [MIT thesis, solar cycle and lifetime](https://dspace.mit.edu/handle/1721.1/163035)
- The Australian BoM gives lifetime curves below 300 km for F10.7 = 70 vs 250, at a mass-to-area ratio of 100 kg/m². Lifetimes scale linearly with M/A below 100. — [BoM SWS](https://www.sws.bom.gov.au/Educational/1/3/8)

**Composition and the He/O transition**
- The He/O transition sits near 500 km during the 2007–2009 minimum, with a winter helium bulge in CHAMP/GRACE data. The very low winter He/O transition comes from a cold, contracted thermosphere. — [AGU FM14](https://agu.confex.com/agu/fm14/webprogram/Paper2496.html); [EGU2014-14742](https://meetingorganizer.copernicus.org/EGU2014/EGU2014-14742.pdf)
- He in place of O at the same temperature increases the drag coefficient. This matters for drag-to-density inversion. — [AGU FM14](https://agu.confex.com/agu/fm14/webprogram/Paper2496.html)
- The largest storm-time density perturbation occurs near the He/O transition, with a weaker maximum near the O/N2 transition. Winter storm response is about 25% at GRACE altitudes vs about 60% at CHAMP altitudes. — [UCAR dataset: altitude variations in density response](https://data.ucar.edu/dataset/ce95c53b-3334-46d6-a5cb-2ae0b3c4c8aa); [UCAR impacts](https://impacts.ucar.edu/en/publications/altitude-variations-in-the-thermosphere-mass-density-response-to-/)
- During active conditions, He near about 450 km decreases while O increases. — [ckanprod UCAR](https://ckanprod.data-commons.k8s.ucar.edu/harvest/object/063bf41c-38fe-4b58-9b76-d24612583551/html)

**Gauge floors and in-situ sensing**
- Miniaturized ionization gauges work as ram-pressure sensors from the slip-flow region near 115 km up to the base of the exosphere. The ion current is proportional to chamber pressure, and the chamber pressure depends on the angle between the orifice and the ram direction. Two pairs of gauges are needed for 2-axis direction. — [NASA NTRS 19960000975](https://ntrs.nasa.gov/api/citations/19960000975/downloads/19960000975.pdf)
- LLITED: two 1.5U CubeSats, each carrying the MIGSI ionization gauge for neutral density. Orbit and technical difficulties forced a reprioritization of science. — [NSF AGS-1042815 / UCLA](https://grantome.com/grant/NSF/AGS-1042815)
- The CINDI neutral sensors failed when unexpectedly low neutral densities were encountered at solar minimum. No proven single instrument measures all needed neutral properties at 300–500 km within a CubeSat envelope. — [USPTO SANDS 11187827](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11187827)
- An alternative is the Broglio Drag Balance on UNICubeSAT, a direct drag-force measurement via plate displacement. — [UniBo CRIS](https://cris.unibo.it/handle/11585/89781)

### Inferences
These are standard-physics estimates, not from the sources above. Verify them with NRLMSIS 2.x in the team's code.
- **Density range.** Order-of-magnitude MSIS-class mass densities:
  - about 2–6×10⁻¹⁰ kg/m³ at 200 km
  - about 1×10⁻¹² (solar min) to 1×10⁻¹¹ (solar max) kg/m³ at 400 km
  - about 10⁻¹⁴ to 10⁻¹² kg/m³ at 600–800 km
  The solar-cycle swing grows with altitude, from about 2× at 200 km to over 10× at 500+ km. The OSSE should tabulate this directly from NRLMSIS for F10.7 = 70/150/250 and Ap = 4/15/100+.
- **Ram vs ambient pressure.** Dynamic ram pressure is ρv². At v ≈ 7.7 km/s and 400 km that gives about 6×10⁻⁵ to 6×10⁻⁴ Pa. Ambient static pressure p = nkT is roughly 10⁻⁶ to 10⁻⁵ Pa at 400 km. A ram-facing closed-source gauge therefore sees roughly an order of magnitude enhancement over ambient. That is why ram-facing gauges are viable to about 500–600 km at solar minimum but run into gauge floors, outgassing and self-contamination backgrounds (often 10⁻⁶ to 10⁻⁷ Pa for small hot- or cold-cathode gauges) at higher altitude and low solar activity. This is consistent with the CINDI failure at solar minimum.
- **Drag-based sensing scales the opposite way.** Drag acceleration a = ½ ρ v² C_D A/m is largest in VLEO, where host spacecraft (Albedo, Skeyeon) also fly. Drag-derived density in VLEO is SNR-favorable, but it is only as good as the C_D and accommodation model. Composition near the He/O transition adds C_D uncertainty.
- **Candidate operating band.** A defensible band for cheap in-situ density/pressure sensors is about 250–550 km. The lower end is set by commercial VLEO host altitudes (about 250–380 km) and host lifetime. The upper end is set by gauge SNR at solar minimum and by the He/O transition, which complicates mass-density inference from total-pressure gauges unless composition is measured. Show OSSE performance vs altitude explicitly across solar min/max to satisfy the "extensive altitude regime" criterion. Rubric credit is likely highest if performance holds through both VLEO (below 300 km) and LEO.
- **Host lifetime and the 1-year requirement.** At 300 km and below, a host without propulsion can decay in months near solar maximum. The 1-year operation requirement effectively pushes un-propelled hosts above about 400 km, or requires propelled VLEO hosts.

### Gaps
- Exact NRLMSIS density tables and ram-pressure numbers were not obtained from a citable source in this pass. Generate them in-house and cite NRLMSIS 2.0 (Emmert et al. 2021).
- No published lower-limit pressure figure for small CubeSat ionization gauges was found. The 115 km figure is an upper-pressure operating bound.
- The Crisp et al. 2020 figure values beyond the snippets above were not extracted.
- No other commercial VLEO hosts were researched in this pass (e.g., EOI Space Stingray, Redwire Phantom, Earth Observant). Gaps remain on their altitudes.

---

## 5. Fleet aspects: number of hosts, coverage for storm sampling, cross-calibration

### Takeaway
Published evidence suggests that observation count and coverage diversity dominate skill. Mixed inclinations beat single planes. Error peaks align with constellation gaps. Tens of tracked objects suffice to constrain reduced-order global models. OCC's at-least-100-unit premise implies a proliferated fleet where cross-calibration between hosts, and against a reference such as a well-characterized drag satellite or HASDM-class product, becomes a first-order design element.

### Cited Findings
- Mixed low- and high-inclination at 520 km beat other configurations because of higher observation counts; 6 vs 12 satellites were compared. — [Dietrich et al. 2024 via NSF PAR](https://par.nsf.gov/servlets/purl/10608384)
- Estimation error peaks coincide with the largest Walker-constellation gaps. — [USPTO 11242162](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11242162)
- Radar data from 20 objects plus GPS from 10 commercial satellites was enough for real-time global density estimation, validated with Swarm. — [Gondelach & Linares 2021](https://dspace.mit.edu/bitstream/handle/1721.1/145414/Space%20Weather%20-%202021%20-%20Gondelach%20-%20Real%E2%80%90Time%20Thermospheric%20Density%20Estimation%20via%20Radar%20and%20GPS%20Tracking%20Data%20Assimilation.pdf?isAllowed=y&sequence=2)
- HASDM uses about 90 calibration objects. — [arXiv 2209.05597](https://arxiv.org/pdf/2209.05597)
- About 1,200 Starlink satellites enabled tomographic density maps at about 482 km. — [summary](https://book.st-hakky.com/en/news/starlink-satellites-map-upper-atmosphere)
- Spire POD densities agreed from satellite to satellite and tracked HASDM. Cross-satellite consistency was itself used as a validation check. — [CPAESS 2020](https://cpaess.ucar.edu/sites/default/files/meetings/2020/presentations/mccarty-presentation.pdf)
- Accelerometer assimilation mainly improves density near the observing satellite's orbit, so vertical spread of hosts matters. — [ResearchGate two-step assimilation](https://www.researchgate.net/publication/366156651_Improving_the_estimation_of_thermospheric_neutral_density_via_two-step_assimilation_of_in_situ_neutral_density_into_a_numerical_model)
- Storm response differs strongly by altitude: about 60% at CHAMP vs about 25% at GRACE in winter. Single-altitude fleets will mis-represent storm vertical structure. — [UCAR](https://data.ucar.edu/dataset/ce95c53b-3334-46d6-a5cb-2ae0b3c4c8aa)
- OCC: at least 100 units, hosted only, and calibration satellites are ineligible. Cross-calibration must therefore come from hosts and from external references. — [OCC Technical Guidelines](https://occ.nasatechleap.org/technical-guidelines/)

### Inferences
- **Fleet-size sweep.** Sweep N_hosts over {5, 10, 25, 50, 100, 200}, with altitude and inclination drawn from a realistic commercial-host distribution (mostly SSO 500–550 km plus a VLEO subset at 250–380 km). Plot storm-main-phase std(ln O/C) and time-to-detect storm onset vs N. Expect diminishing returns. The knee is the defensible "how many units" number.
- **Storm sampling.** Storm main phases last hours. With 90-minute orbits, sampling the auroral/high-latitude response within about 1 hour of onset needs multiple planes or local times. Score storm detection latency and peak-capture error as separate metrics.
- **Cross-calibration in the EKF.** Make per-unit gain, and optionally drift, augmented states.
  - Use conjunction or crossover events, where two hosts pass near the same location and time, as relative-calibration constraints.
  - Anchor absolute scale to a reference: host POD/drag-derived density on a subset with known geometry, HASDM/Solari-class products, or TU Delft densities when a legacy mission overlaps.
  - In Monte Carlo, vary the per-unit gain spread and the crossover frequency to show how quickly fleet calibration converges.
  - Test identifiability. Common-mode gain error across all units is unobservable without an absolute anchor. Show this explicitly.

### Gaps
- No published thermosphere OSSE gives a minimum host count for storm sampling with in-situ sensors. The team's own sweep will be novel evidence.
- No published cross-calibration method for proliferated in-situ density sensors was found in this pass.
