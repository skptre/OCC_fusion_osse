# Anchor cheap gauges with oxygen and drag

The proposed architecture works, with one condition. "One density channel plus a couple of composition channels that also help the density estimate" holds up only if at least one composition channel is **species-selective**. A ram-facing ionization gauge and host drag cannot separate oxygen from nitrogen, because at 300-500 km both sensors effectively count oxygen. The team's own OSSE (team result) gives a condition number of about 120-150 for gauge plus drag and about 1.7 once an O sensor is added. The suite that is cheap, flight-backed and defensible today has three parts:

- a ram-facing gauge in a spherical accommodation chamber for fast total number density;
- a FIPEX-type solid-electrolyte sensor for atomic oxygen;
- the host's GNSS orbit-derived drag, which costs nothing and acts as the slow absolute anchor.

Of the major species, **helium is the only one no cheap flown instrument measures directly**. That gap, together with the gauge's pressure floor, makes **roughly 250-450 km** the honest altitude band for "density plus composition". Density-only performance could extend to about 500 km at solar minimum and about 650 km at solar maximum. This scope fits what OCC rewards. Relevance 5 explicitly requires "density together with composition" over "a clearly identified and extensive altitude regime" ([OCC evaluation criteria](https://occ.nasatechleap.org/evaluation-criteria/)), and no in situ composition has been measured since Dynamics Explorer 2 in the early 1980s ([Bruinsma et al. 2023](https://par.nsf.gov/servlets/purl/10500438)).

The OSSE's headline number needs reframing before it goes in a proposal. The 3.4% fused storm-time error scales with the *assumed* calibration priors, and a back-of-envelope check below shows why. The fused absolute accuracy is set mostly by the best-calibrated anchor, which today is the assumed ±7% drag coefficient, not the gauge. The defensible claims are therefore three: accuracy traceable to calibration, precision set by gauge repeatability, and composition separated by the O channel. The OSSE should show each claim as a curve across calibration and prior-degradation assumptions, not as a single number.

## OCC rewards composition and coverage, not just a density number

OCC's technical guidelines name mass density as the lead measurand. Pressure and drag acceleration are accepted as routes to density, and composition, meaning "individual number density of major neutral species", is "valued but not required" ([OCC technical guidelines](https://occ.nasatechleap.org/technical-guidelines/)). The benchmark numbers are explicitly **"target floors, not fixed requirements"**. NASA's Doug Rowland said at the info session that a solution trading performance for "substantial gain in cost or scalability can still be highly competitive" ([info-session transcript p.4](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)).

| Type | Measurand | Regime | Accuracy | Precision | Resolution |
|---|---|---|---|---|---|
| In situ | Mass density (composition preferred) | LEO or VLEO | ≤20% | ≤10% | ≤30 s |
| In situ | Neutral gas pressure | LEO or VLEO | ≤20% | ≤5% | ≤30 s |
| In situ | Drag acceleration | LEO or VLEO | ≤5% | ≤1% | ≤10 s |
| Remote | Major-species density (NO, O2, N, O) | VLEO 90-300 km | ≤10% | ≤10% | 5° horiz., 10 km alt. |
| Remote | Temperature profile | VLEO 90-300 km | ≤10% | ≤10% | 5° horiz., 10 km alt. |

Source: [OCC technical guidelines](https://occ.nasatechleap.org/technical-guidelines/), with the numbers confirmed verbatim in the [transcript](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf).

The rubric caps the architecture choice before performance is even considered. **Relevance 5** requires density together with composition over an extensive altitude regime, plus a "specific, well-evidenced case for how the data would improve model accuracy or fill known coverage gaps". Density alone, or density plus composition over a narrow span, caps at 4. Pressure or drag alone caps at 3 ([OCC evaluation criteria](https://occ.nasatechleap.org/evaluation-criteria/)). An applicant argued that drag assimilation does not use composition and asked NASA to change the rubric. NASA declined, describing composition as "the composition that produces that density" ([transcript p.12-13](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)). That framing fits the architecture: composition channels that *produce* the density estimate are exactly the kind NASA described.

**Performance 5** requires quantitative evidence that the benchmarks will be met, with "expected uncertainty characterized and realistic". A missing calibration plan pushes the score toward 2. The hard constraints are:

- the solution must be a hosted payload;
- it must include flying hardware;
- deployables must be retained;
- it must not interfere with the host;
- it must operate for at least one year;
- it must be buildable in quantities of 100 or more at a cost "far below" the $1-10M per copy of current instruments.

No mass, power, EMI, total-dose or magnetic envelope is published, so applicants state their own assumptions ([OCC technical guidelines](https://occ.nasatechleap.org/technical-guidelines/)). Phase 2 then scores "trade studies and the rationale for the chosen approach" at 25 of 100 points ([transcript p.7](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)). That makes the OSSE trade study scorable evidence twice: in Phase 1 and again in Phase 2.

The science gaps come from the review OCC itself links, Bruinsma et al. 2023. The bulk of composition data dates from the 1970s-80s, and **"in situ composition measurements have not been taken since the Dynamics Explorer 2 mission"**. Density datasets from different missions "typically disagree 5-20%", reaching 45% at 800 km. Data are sparse below about 250 km and above 550 km, and above 500 km models can be assessed only against orbit-mean densities. Only two Kp=9 storms have occurred since 2000, each seen by one or two satellites. Gas-surface interaction choices alone can shift the drag coefficient by up to 20% ([Bruinsma et al. 2023](https://par.nsf.gov/servlets/purl/10500438)). Bruinsma also explicitly recommends running OSEs and OSSEs to justify new data streams, which gives the team's simulation a citable mandate.

The table below maps each gap to the kind of measurement that fills it, and to what a cheap hosted suite can realistically claim.

| Gap (source) | Measurement type that fills it | What a cheap suite can claim |
|---|---|---|
| No in situ composition since DE-2; Bruinsma asks for "simultaneous" density plus O2, N2, O, He ([Bruinsma 2023](https://par.nsf.gov/servlets/purl/10500438)) | Species-selective number densities: n(O), n(N2), n(He) | n(O) from a FIPEX-type sensor. n(N2) from gauge minus the O contribution. n(He) only with a mass spectrometer or multi-altitude fleet inversion |
| Datasets disagree 5-20%, up to 45% at 800 km ([Bruinsma 2023](https://par.nsf.gov/servlets/purl/10500438)) | Traceable absolute calibration and fleet cross-calibration | Per-unit vacuum-chamber calibration, crossover cross-calibration between hosts, drag anchor |
| Few high-resolution data below ~250 km and above ~550 km ([Bruinsma 2023](https://par.nsf.gov/servlets/purl/10500438)) | In situ sensing on VLEO hosts; drag or high-sensitivity sensing high up | VLEO is easy for gauges (high pressure). Above ~500 km at solar minimum the gauge floor binds (see the pressure table below) |
| Tiny storm database; models worst in storms; NRLMSISE-00 "systematically and significantly underestimates" storm densities ([SWSC 2021](https://www.swsc-journal.org/10.1051/swsc/2021002)) | Continuous ≤30 s in situ sampling on many hosts and local times | Gauge at ~1 Hz on 100+ hosts, scored storm phase by storm phase |
| Drag coefficient / GSI uncertainty, 20-30% ([Bruinsma 2023](https://par.nsf.gov/servlets/purl/10500438)); ~25% near the O-He transition ([Bernstein et al. preprint](https://essopenarchive.org/doi/full/10.1002/essoar.10508667.1)) | In situ O partial pressure (sets surface AO coverage and accommodation) and mean molecular mass | O sensor plus gauge-and-drag m̄ constrain C_D. This is the clearest "composition helps density" mechanism |
| No continuous low-latency stream for assimilation ([Bruinsma 2023](https://par.nsf.gov/servlets/purl/10500438)) | Host-downlinked, low-data-rate time series | Small data volume via host downlink, which OCC provides |

## Gauges have flown cheaply; oxygen sensors barely; helium not at all

The flight record splits cleanly by measurand. Total-density gauges have a long, cheap heritage. Species-selective oxygen sensing rests on essentially one instrument family. Helium-capable small instruments exist, but their science return is poor or unpublished. The table uses the evidence levels from the research notes: FLIGHT means data returned, FLOWN-NO-DATA means launched without published results, and CLAIM or DATASHEET means vendor or pre-flight statements.

| Instrument (flight) | Measures | SWaP | Demonstrated / stated performance | Cost | Evidence and failures |
|---|---|---|---|---|---|
| **UNH MIGSI** Bayard-Alpert hot-cathode gauge, LLITED-A/B 1.5U CubeSats, ~514×496 km, 97.4°, 2023-2024 | Chamber pressure → total density, wind | 0.6 kg, 0.5U, 2.73-3.5 W on +5/+12 V, ~6 cm spherical chamber ([eoPortal](https://www.eoportal.org/satellite-missions/llited)) | Range 1e-8 to 1e-3 Torr (team slides) or 1e-2 Torr (eoPortal); **1 Hz**; 20% accuracy; precision stated inconsistently as 0.1% or 10%; needs ≤1° ram pointing ([eoPortal](https://www.eoportal.org/satellite-missions/llited); [LLITED slides 2026](https://spdf.gsfc.nasa.gov/pub/data/aaa_smallsats_cubesats/llited/documents/LLITED-presentation-2026-00325.pdf)) | Not found | FLIGHT. A solar-cell anomaly cut power below 50% of expected, forcing reduced duty cycle and campaigns. Wrong deployer door gave the wrong orbit. ~7 years from proposal to launch ([NASA S3VI](https://www.nasa.gov/smallsat-institute/community-of-practice/lessons-learned-from-the-llited-mission/)). L2 data public on SPDF |
| **Aerospace Corp. Streak gauge** (COTS miniature BA sensors) | Total density | Not given | ~1 year of orbital data; 1 kHz suborbital variant; "crude composition" mode ([AVS 2006](https://www2.avs.org/symposium2006/Papers/Paper_VT-WeA3.html); [Clemmons 2009](https://findscholars.unh.edu/display/publication448950)) | Not found | FLIGHT. MIGSI's ancestor |
| **Commercial cold-cathode gauges**, Lehmacher/Clemson rockets (2013; 2019-2024 campaigns) | Density and temperature profiles 90-325 km | Not given | Seven profiles; storm-time density up to +50% at 140 km ([Lehmacher 2026 abstract](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2026JA035338); [Lehmacher 2013](https://www.researchgate.net/publication/258794665_Multiple_neutral_density_measurements_in_the_lower_thermosphere_with_cold-cathode_ionization_gauges)) | COTS heads | FLIGHT (suborbital only). Gauge models not retrieved. Explorer 32 flew Redhead magnetrons in 1966 ([Explorer 32](https://en.wikipedia.org/wiki/Explorer_32)). **No orbital CubeSat flight of a commercial cold-cathode gauge found** |
| **QQ-Satellite OAD** ionization gauge + dual-frequency GNSS POD, 73.8 kg sphere, ~520 km, 2021 | Gauge density and POD density | 73.8 kg spacecraft | POD density shows an "approximately 18.77%" difference (referent unclear) and 52.99% 1σ during a storm ([Sun et al. 2022](https://doi.org/10.3390/rs14163873)) | Not found | FLIGHT. The closest gauge-plus-POD analogue. Jin et al. 2025's gauge-vs-POD numbers were not retrieved |
| **SpEED Demon** MEMS accelerometers + ion gauge (ERAU rocket 2022) | Drag density | Small | MEMS drag density within 10% of gauge and MSIS at 80-100 km; useless above ~100 km ([ERAU](https://portfolio.erau.edu/en/publications/mesosphere-lower-thermosphere-neutral-density-measurements-from-l/)) | Low | FLIGHT (suborbital). Shows MEMS cannot sense orbital drag |
| **FIPEX** solid-electrolyte O / O+O2 sensor (TU Dresden / IRS Stuttgart) | n(O) and O2 | Small; heater power ~1 W is unverified | ISS EuTEF **572 days** from 2008 ([ESA](https://www.esa.int/Space_in_Member_States/Germany/Gefahr_im_Orbit_Hochreaktive_Sauerstoffatome)); WADIS-1 rocket at **100 Hz**, <9 m resolution, lab-calibrated against an AO source ([Eberhart et al. 2015](https://amt.copernicus.org/articles/8/3701/2015/)) | Not found. Commercial derivative "VacuSen" from ESCUBE ([ESA](https://www.esa.int/ESA_Multimedia/Images/2011/04/VacuSen_sensor)) | FLIGHT on ISS and a rocket. QB50 CubeSats FLOWN-NO-DATA (no published results). SWARM-EX (FIPEX + Langmuir probe) launch unconfirmed ([Gunter's](https://space.skyrocket.de/doc_sdat/swarm-ex.htm)). **No accuracy figure published** |
| **ORMADD** erodible-film AO detector, TAUSAT-1 3U, 2021 | Integrated AO fluence | mW-class | Average AO flux "comparable" to SPENVIS ([BIU](https://cris.biu.ac.il/en/publications/measurements-of-material-erosion-in-space-by-atomic-oxygen-using-/)) | Very low | FLIGHT. Consumable and slow; not a 30 s density channel |
| **QB50 INMS** (MSSL/UCL) | O, O2, N2, NO | 2U-class host | 9 launched; **1 returned data**, for one month (ESA) or six months (MSSL poster) ([ESA indico](https://indico.esa.int/event/340/contributions/5813/)) | Not found | Mostly failed. Student-bus failures dominated: 9 of 36 QB50 satellites were dead on arrival |
| **GSFC ExoCube INMS** | H, He, N, O, N2, O2 | **1.3U, 570 g** | Gated TOF, M/ΔM ≈ 10, thermionic source; produced flight data in 2015; later flew on Dellingr. Outgassing contaminates H ([NTRS](https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20160010304.pdf); [AGU FM15](https://agu.confex.com/agu/fm15/webprogram/Paper84629.html)) | Not found | FLIGHT, few published numbers. The only small flown instrument that covers He |
| **NRL/GSFC WINCS (SWATS)** | Winds, temperature, O, N2, ions | 7.6×7.6×7.1 cm, ~1.3 W, 0.75-0.85 kg | Flew on ISS and STPSat-3 (2013), SENSE, CADRE ([AGU FM14](https://agu.confex.com/agu/fm14/webprogram/Paper7513.html); [eoPortal CADRE](https://eoportal.org/satellite-missions/cadre)) | Government-built, no catalog price | FLIGHT; no composition results found published |
| **UNICubeSAT Broglio drag balance** | Drag force | ~1 kg design | 20% expected; needed perigee ≤350 km ([IAC-09](https://iafastro.directory/iac/archive/browse/IAC-09/D1/1/4859/)) | n/a | **Never flew.** The launched UniCubeSat-GG swapped in booms and was never heard from ([Gunter's](https://space.skyrocket.de/doc_sdat/unicubesat-gg.htm)) |
| **Host GNSS POD drag** (Spire, Mutschler/SoleiTool) | Orbit-averaged density | Zero added SWaP | Satellite-to-satellite consistency; tracks HASDM ([CSDAP pilot](https://www.earthdata.nasa.gov/sites/default/files/imported/CSDAP-Pilot-Sutton.pdf)) | Free if the host has a receiver | FLIGHT. Averaged over the arc, not a 10 s drag product |

Catalog cold-cathode heads are what make 100+ units plausible. An **MKS 423 I-Mag head lists at $431-569** on MKS's site and $685-837 at Ideal Vacuum, and a **Pfeiffer IKR 361 C runs about $2,070-2,277** ([MKS](https://www.MKS.com/f/423-i-mag-cold-cathode-vacuum-sensors); [Ideal Vacuum](https://idealvac.com/en-bs/MKS-423-I-Mag-Cold-Cathode/pl/34-1932-472); [AJVS](https://www.ajvs.com/library/Pfeiffer_Vacuum_PKR_361_IKR_361.pdf)). Cold-cathode electronics run under 1 W, have no filament to wear out, and current versus pressure follows a power law with exponent about 1.0 between 1e-4 and 1e-9 Torr. They come with costs: 2-6 kV, a magnet, striking delays from seconds at 1e-6 Torr to hours at 1e-10 Torr, sensor-to-sensor matching of only 20-25%, and repeatability of about ±5% ([SRS app note](https://www.thinksrs.com/downloads/pdfs/applicationnotes/IG1hotapp.pdf)).

Hot-cathode BA gauges are linear, with 1-2% repeatability. They draw more power, and filament life is "many thousands of hours", which is only about 0.1-0.5 years of continuous operation against a one-year requirement (analysis). Hot filaments also chemically alter O and O2 ([SRS app note](https://www.thinksrs.com/downloads/pdfs/applicationnotes/IG1hotapp.pdf)).

**The team's tentative MAG084 head, as specified on its datasheet (team-supplied):**

| Parameter | Datasheet value (tiba71e1-a, 2024) |
|---|---|
| Range | 1e-8 to 5e-3 mbar |
| Accuracy | **30% of reading (N2, typical)**. The team slide's "4%" is wrong |
| Repeatability | 5% |
| Operating temperature | +5 to +80 °C (standard cable) |
| Environment note | "use indoors only" |
| HV / current | ≤3.3 kV, ≤600 µA |
| Gas-correction factors | None on the datasheet |
| Controller | Needs the VGC094 rack controller: 15 W, 1.5 kg, 0.5 kg head, about $8,000 including controller (team slide) |

That controller is not flyable. A flight version needs a custom HV supply and electrometer, which is the route Lehmacher's rocket gauges took. The web page confirms the NdFeB magnet sits in a closed, shielded magnetic circuit and that the head is radiation-tolerant to 1e7 Gy ([INFICON MAG084](https://inficon.com/en/products/vacuum-gauge-and-controller/mag084)).

### The real altitude limit is the gauge floor, not the gauge ceiling

The research notes contained an order-of-magnitude chamber-pressure table built from generic moderate-activity densities. The team's own NRLMSIS 2.1 calculation supersedes it (team result; equinox, ap=4, thermalized ram chamber at Tw=300 K). The comparison shows the notes' table roughly matches **solar-maximum** conditions and is about an order of magnitude too optimistic at 400-600 km for solar minimum.

| Altitude | Solar min F10.7=70, ram chamber (Pa) | Solar max F10.7=200, ram chamber (Pa) | Notes' generic estimate (Pa, converted from Torr) | vs MAG084 floor 1e-6 Pa |
|---|---|---|---|---|
| 200 km | 1.2e-3 | n/a | ~1.3e-3 | Far above |
| 300 km | 7.7e-5 | 3.5e-4 | ~2.7e-4 | ~77× / 350× floor |
| 400 km | 8.6e-6 | n/a | ~6.7e-5 | ~9× floor at solar min |
| 500 km | 1.3e-6 (marginal) | 2.2e-5 | ~2e-5 | **1.3×** / 22× floor |
| 600 km | 2.9e-7 (below) | n/a | ~6.7e-6 | Below at solar min |
| 700 km | n/a | 2.0e-6 (marginal) | n/a | Marginal at solar max |
| 800 km | n/a | 7.3e-7 (below) | ~0.7-1.3e-6 | Below |

Without a chamber, ambient pressure falls below the floor from about 400 km (team result). That confirms the notes' point that **ram compression in an accommodation chamber is mandatory, not optional**. The flux-balance enhancement is roughly 64× for N2, 48× for O and 24× for He at Tw=300 K (analysis in notes). Two consequences are easy to miss.

First, MIGSI's 1e-8 Torr floor is about 1.3e-6 Pa, essentially the same as the MAG084's 1e-6 Pa. A flown hot-cathode design therefore buys **no altitude ceiling advantage**. LLITED's ~500 km operation coincided with the active phase of solar cycle 25, which is consistent with the solar-max column.

Second, spacecraft outgassing near the gauge can add a background of order 1e-7 to 1e-6 Pa early in a mission (analysis in notes). At 500 km and solar minimum that equals the signal. NASA's CINDI neutral sensors are a cautionary precedent: they "failed when unexpectedly low neutral densities were encountered at solar minimum" ([USPTO 11187827](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11187827)).

## Gauge plus drag sees one number; the oxygen channel sees a second

Every sensor in the suite measures a weighted sum over the same hidden species densities. The weights decide what can be separated:

- **Drag** weights species by mass: He:O:N2 = 4:16:28.
- **An N2-calibrated ionization gauge** weights by ionization cross-section. He is 0.16-0.19 relative to N2 = 1, and O2 is 0.90-1.01 ([SRS gas-correction note](https://cornestech.co.jp/wp-content/uploads/2022/01/App_IG1BAgasapp.pdf); [Physics Today table](https://aip.brightspotcdn.com/PTO.v25.i8.40_1.online.pdf)). Gauge sensitivity to atomic O **has never been measured**. A 1966 NASA report already called it a cross-section estimate whose error was hard to bound ([NTRS 19660028088](https://ntrs.nasa.gov/api/citations/19660028088/downloads/19660028088.pdf)).

At 300-500 km oxygen dominates both sums, so the two rows point in nearly the same direction. With an effective O weight near 0.5, the angle between gauge and drag rows in the (O, N2) plane is only about 3-4° (analysis in notes). The team's condition number of 120-150 for gauge plus drag is that same geometry, computed. Adding the O sensor's row, which is (1, 0, 0) in (O, N2, He), drops it to about 1.7 (team result).

The literature agrees on the structural point. Both mature methods for inferring composition from cheap data needed a *second, independent* constraint besides one mass-density stream:

- Mehta, Linares & Sutton fit modal species fields to CHAMP/GRACE density *plus* GUVI column O/N2 ([GFZ index](https://www-app2.gfz.de/grace-references/b2hd-2019SpWea..17.1364M.html)).
- Thayer et al. and Liu et al. separated He from O using CHAMP and GRACE at *two altitudes*, finding winter He 30-70% above NRLMSISE-00 at solar minimum ([EGU2014-14742](https://meetingorganizer.copernicus.org/EGU2014/EGU2014-14742.pdf)).

A third measurement is therefore the price of composition, not a nice-to-have.

### Why the fused accuracy tracks the calibration priors (analysis)

Write the team's EKF in its own log-correction coordinates: x = [ln c_O, ln c_N2, ln c_He, ln g_gauge, ln g_O, b_CD]. The linearized measurement rows are:

| Sensor | ln c_O | ln c_N2 | ln c_He | ln g_gauge | ln g_O | b_CD |
|---|---|---|---|---|---|---|
| Gauge | w_O | w_N2 | w_He | 1 | 0 | 0 |
| O sensor | 1 | 0 | 0 | 0 | 1 | 0 |
| Drag | f_O | f_N2 | f_He | 0 | 0 | 1 |

Here w_i are the gauge-signal fractions S_i·n_i/Σ S_j·n_j, and f_i are the mass fractions. Because the w_i sum to 1 and the f_i sum to 1, a common shift δ in all three species corrections changes each measurement by exactly δ. That shift is indistinguishable from moving all three sensor gains together.

**The absolute scale of density is therefore unobservable from the data alone.** It is pinned only by the priors on g_gauge, g_O, b_CD and the background model, roughly in inverse-variance combination: 1/σ² ≈ 1/σ_gauge² + 1/σ_O² + 1/σ_CD² + 1/σ_prior².

A rough check with σ_CD = 7%, σ_gauge = 30%, σ_prior ≈ 30% and an assumed σ_O ≈ 20% gives σ ≈ 6%. That implies a median absolute error near 4%, close to the team's 3.4%. Scaling all priors by 0.25 or 2 moves this estimate to roughly 1.2% and 8%, close to the team's 1.8% and 8.8%. This explains two team results:

- The fused error barely moves as gauge calibration error goes from 2% to 40% (team result), because the ±7% C_D prior dominates the sum.
- The naive gauge alone crosses the 20% target at about 30% calibration error (team result), which is exactly the MAG084 datasheet accuracy.

The team's untested hypothesis, that the drag channel's C_D assumption anchors absolute density, is close to a mathematical consequence of the filter's structure. It is easy to confirm: rerun with the C_D prior at 15% and 25%.

The same algebra explains the team's composition finding. If the gains random-walk in flight, a common-mode drift between them is never observed, so it leaks into the species split. That is why O-share error falls from about 3 and 9 percentage points to about 1.1 and 1.5 points at 300 and 450 km only when all three gains are fixed (team result).

The derived instrument requirement is **gain stability (drift per orbit or per day), more than absolute gain accuracy**. Cold-cathode repeatability of about ±5% and insulator contamination from sputtering ([SRS app note](https://www.thinksrs.com/downloads/pdfs/applicationnotes/IG1hotapp.pdf)) are the numbers to characterize, along with FIPEX ageing, which is unpublished.

### The ±7% drag anchor is optimistic where it matters

Bruinsma reports drag-force differences above 30% between models, up to 20% from the gas-surface-interaction choice alone, and up to 15% from the computational method ([Bruinsma et al. 2023](https://par.nsf.gov/servlets/purl/10500438)). Inter-satellite comparisons suggest diffuse-reflection modelling biases density by about 25% near 500 km and the O-He transition ([Bernstein et al. preprint](https://essopenarchive.org/doi/full/10.1002/essoar.10508667.1)). Scale differences between thermospheric datasets mostly trace back to geometry and GSI modelling ([Mehta et al. 2022](https://link.springer.com/article/10.1007/s12567-022-00434-3)).

A planning band of **5-10% below 400 km, rising to 15-25% near 500 km**, is more defensible than a flat ±7% (analysis in notes). It is also worse for an arbitrary commercial host than for a sphere like QQ-Satellite.

This is where the composition channel earns its "also helps density" role. AO adsorbed on surfaces sets energy accommodation, explained by Langmuir adsorption with an O binding energy of about 5.7 eV ([Pilinski dissertation](https://scholar.colorado.edu/asen_gradetds/37/)). Adsorbed AO masks material differences near 200 km, and material properties "slowly emerge" higher up as coverage falls ([Moe & Bowman 2005](https://spacewx.com/wp-content/uploads/2024/02/AAS_2005_258_Surface_Effects_on_CD_of_Spheres.pdf)). An in situ O partial pressure therefore feeds three things: surface coverage, then accommodation, then the host C_D. That tightens the very prior that anchors absolute density. No published paper quantifies this C_D error reduction, so it is an open niche the OSSE can fill.

## Recommended suite: gauge plus FIPEX plus host drag, He as an upgrade

The recommended architecture is three channels with deliberately different jobs: fast relative total density, species selectivity, and slow absolute anchoring. Cold cathode versus hot cathode stays an open variable to be decided by the OSSE on lifetime, power and cost. Accuracy should not decide it, because the fusion makes the result insensitive to gauge calibration.

| Role | Baseline choice | Why | Alternatives / fallbacks |
|---|---|---|---|
| **Fast density channel** (30 s or faster, sets *precision*) | Ram-facing ionization gauge in a closed spherical accommodation chamber (O recombines to O2 on the walls), with a wall thermistor for Tw | Cheapest flown density sensor class. Flux balance gives n_c/n_a analytically. A closed source makes O read as O2 with a known gas factor ([NTRS 19870016743](https://ntrs.nasa.gov/api/citations/19870016743/downloads/19870016743.pdf)) | (a) **Cold-cathode head** (MKS 423-class at about $0.5k, or a MAG084 head) plus custom <1 W HV electronics: cheap, no filament, but no orbital CubeSat heritage, ignition delay, kV corona risk during ascent, and 20-25% unit scatter. (b) **MIGSI-type miniature BA**: orbital heritage, linear, but about 3 W and filament life versus a one-year requirement (needs dual filaments and duty cycling) |
| **Species channel** (breaks the O/N2 degeneracy) | FIPEX-type solid-electrolyte O / O+O2 cell | Only cheap flown species-selective sensor: 572 days on ISS, 100 Hz on a rocket | ESCUBE "VacuSen" procurement route. If unavailable: a second gauge with a different O response (open source) is unflown and weak. Erodible-film actinometers are too slow and consumable |
| **Absolute anchor** (sets *accuracy*) | Host dual-frequency GNSS POD drag, plus host attitude and geometry | Zero added SWaP; flown at scale (Spire, QQ-Satellite) | Without a host GNSS receiver: per-unit chamber calibration against a spinning-rotor or reference gauge becomes the anchor. Fleet crossovers fix relative gains, but common-mode error stays unobservable without an absolute reference |
| **He channel** (makes composition "extensive" above about 450 km) | None in baseline; claim He as model-constrained | No cheap flown He-selective sensor | (a) Fleet multi-altitude inversion à la Thayer/Liu, testable in the OSSE. (b) ExoCube-class INMS (1.3U, 570 g, M/ΔM ≈ 10) as a premium variant, with poor QB50 reliability precedent |

### Pseudocode analogy: three log streams with different weights

To a software person, the suite is three monitoring streams over the same hidden state, each with its own blind spots. The gauge is a high-rate counter with an unknown scale factor. Drag is a slow, audited total. The O sensor breaks out one category. No single stream can reconstruct the breakdown, but together they can, provided their weights differ.

```python
# Hidden truth at the spacecraft (what we want): n = {O, N2, He}   [m^-3]
# MSIS-like prior gives n_prior; the filter estimates log-corrections c and sensor gains.

def gauge(n):     # fast (1 Hz), cheap, ±30% absolute gain, ~5% repeatable
    return g_gauge * ram_factor * (S_O2_eff*n.O/2 + 1.0*n.N2 + 0.18*n.He)   # O->O2 on walls

def o_sensor(n):  # species-selective: the tie-breaker
    return g_O * n.O

def drag(n):      # slow (orbit-arc average), absolute through C_D
    return (CD_true / CD_model) * (16*n.O + 28*n.N2 + 4*n.He) * AMU

# Degeneracy, in code terms: at 400 km, gauge() and drag() are both ~ k*n.O,
# so two equations collapse to one.  o_sensor() adds an independent row.
# Scale ambiguity: multiply every n by s and divide every gain by s -> identical readings.
#   => absolute density = whichever of {g_gauge, g_O, CD_model, prior} is best calibrated.

for t in timeline:
    x, P = ekf.predict(x, P, Q_adaptive(Kp))          # inflate composition noise in storms
    for z, h in [(gauge_meas, gauge), (o_meas, o_sensor), (drag_meas_if_arc_done, drag)]:
        x, P = ekf.update(x, P, z, h)
    rho = sum(m_i * n_i(x))                           # mass density: the OCC lead measurand
    report(rho, n_O, n_N2, n_He, sigma_from(P))       # composition is a by-product of producing rho
```

The same pattern appears in navigation fusion, which may be more familiar. The gauge plays the role of an IMU: high-rate, good relative precision, drifting scale. Drag plays GPS: slow, absolute. The O sensor plays the magnetometer: it resolves an axis the other two cannot see. Remove the magnetometer and heading becomes unobservable; remove the O sensor and the O/N2 split does. Remove the slow absolute sensor and everything is relative.

### Feasibility verdict, honestly scoped

Density plus O and N2 composition is feasible and well-conditioned from roughly the VLEO host floor up to about 450 km. Commercial VLEO hosts operate around 250-380 km: Albedo's Clarity-1 was measured at 350-380 km against a 274 km design, and Skeyeon targets about 250 km ([Albedo](https://albedo.com/post/clarity-1-what-worked-and-where-we-go-next); [EvoNexus/SpaceNews](https://evonexus.org/evonexus-portfolio-company-featured-on-the-cover-of-space-news/)). That band spans OCC's 300 km VLEO/LEO boundary, which supports the "extensive" Relevance claim.

Above about 450 km the baseline loses composition, because He matters and the team's estimator fails there (team result). It then loses density margin at solar minimum near 500 km, where pressure is about 1.3× the floor. Above about 550 km at solar minimum the cheap gauge suite cannot address Bruinsma's 700-800 km gap, and the proposal should say so rather than imply coverage.

The one-year life requirement interacts with altitude. At 400 km, lifetime ranges from about 3 months to over 8 years depending on ballistic coefficient and solar flux ([Crisp et al.](https://arxiv.org/pdf/2007.07699)). The low end of the band therefore depends on a propelled host.

## Ranking suites and choosing altitude with the OSSE

The OSSE's job in the proposal is to turn "we think composition helps" into the "specific, well-evidenced case" Relevance 5 demands, and into the trade study Phase 2 scores. It can only do that credibly if the ranking survives harder truth models than the one used to build the filter.

The team currently uses NRLMSIS truth with an MSIS prior on degraded drivers. That is a perturbed-driver twin: it shares MSIS's composition structure, so it cannot represent errors like the 30-70% winter He excess. Identical-twin OSSEs overstate the benefit of new observations, and the bias is **observation-type-dependent** ([Halliwell 2014](https://www.aoml.noaa.gov/phod/docs/Halliwell_2014.pdf); [NOAA OSSE document](https://repository.library.noaa.gov/view/noaa/27196/noaa_27196_DS1.pdf)). That makes it dangerous specifically for *ranking* suites.

The procedure below runs from cheapest to most expensive, so most candidates are eliminated before the Monte Carlo budget is spent.

| Stage | What it does | Pass/fail rule or output |
|---|---|---|
| **0. Credibility ladder** | Run every ranking on (a) identical twin, for code verification and as a ceiling; (b) perturbed-driver twin (current setup) plus a stochastic multiplicative density field; (c) different-model truth (JB2008 or DTM2013, GPU-cheap); (d) real tracks (TU Delft CHAMP/GRACE/GRACE-FO/Swarm densities) ([notes' ladder; Bruinsma 2021](https://www.swsc-journal.org/10.1051/swsc/2021002)) | Report (a) only as a bound. A ranking counts only if it is stable across (b)-(d) |
| **1. Hard gates** | Per candidate instrument and altitude: chamber pressure ≥ 10× floor at the design F10.7 (team NRLMSIS table); host lifetime ≥ 1 year; per-unit cost and SWaP within the stated host envelope; flight evidence level; operating temperature range (note MAG084's +5 to +80 °C and "indoors only") | Binary. Fail means drop, or derate the claimed band |
| **2. Observability screen** | Fisher information / condition number of the stacked Jacobian (table above) per altitude 200-600 km, F10.7 70/150/200, season, Ap, with gains as states. Cheap and analytic | Keep a suite at an altitude only if κ falls below a threshold (for example 10) and the per-species CRLB is under the target. This is where gauge+drag (κ≈120-150) and He above 450 km fall out |
| **3. Monte Carlo scenario grid** | Suites S0 prior only, S1 drag only, S2 gauge, S3 gauge+drag, S4 gauge+O, **S5 gauge+O+drag**, S6 S5+TOF He, S7 TOF+drag. Gauge type is a parameter (cold vs hot cathode error models). Altitudes 250-600 km in 50 km steps; F10.7 {70, 150, 200}; quiet, G3, G5; equinox and solstice; 2-3 inclinations/LTANs | Bruinsma metrics: mean ln(O/C) as **accuracy**, std ln(O/C) as **precision**, correlation, RMS. Storms in 4 phases relative to min Dst after pre-storm de-biasing ([Bruinsma 2021](https://www.swsc-journal.org/10.1051/swsc/2021002)). Composition: n(O), n(N2), n(He) errors and O/N2 error |
| **4. Robustness sweeps** | Calibration priors ×0.25 to ×2; C_D prior 3-25%; effective O gauge weight / recombination efficiency 0.3-1.0; gain random walk on/off and its rate; prior-degradation level (team: 4-36%); outgassing background and decay; attitude error; filter R and Q mis-set ×0.5 and ×2, with NEES/NIS checks | Plot metric versus each assumption. Any suite whose rank flips inside plausible ranges is "fragile" and gets flagged |
| **5. Requirement derivation** | Morris screening over 15-30 factors, then Saltelli/Jansen Sobol (S1, ST with bootstrap CIs) on survivors; then 1-D/2-D spec sweeps on the 2-3 dominant factors ([Sobol MC](https://arxiv.org/pdf/1612.08423); [Saltelli sampling](https://arxiv.org/pdf/2509.07066)) | The knee where the metric crosses the OCC floor, divided by a 1.5-2× margin, becomes the instrument spec (for example a maximum gain drift per day) |
| **6. Decision matrix** | Columns: quiet and storm-main precision, accuracy, composition error, altitude band passing all gates, unit cost, mass, power, heritage. Map onto the four unweighted rubric criteria; perturb weights with Dirichlet sampling | Winner equals the most frequent rank-1 across weight draws *and* truth levels (b)-(d) |

Altitude selection falls out of the same grid. For each suite, the claimed band is the **intersection** of four sets:

- altitudes passing Stage 1 at the design solar condition;
- altitudes where Stage 2's condition number stays below threshold for the species being claimed;
- altitudes where Stage 3's fused metrics meet the OCC density row (≤20% accuracy, ≤10% precision at ≤30 s) in both quiet and storm-main phases;
- altitudes where that result survives Stage 4's plausible-range sweeps.

```python
def claimed_band(suite, solar):                     # solar in {min, mid, max}
    ok = []
    for h in range(200, 650, 50):
        if p_chamber(h, solar) < 10 * suite.gauge.floor:          continue   # Stage 1: SNR
        if host_lifetime(h, solar) < 1.0:                         continue   # Stage 1: OCC life
        if cond_number(suite, h, solar, species=claimed) > K_MAX: continue   # Stage 2
        m = monte_carlo(suite, h, solar, storms=[quiet, G3, G5])              # Stage 3
        if not meets_occ(m, acc=0.20, prec=0.10, cadence=30):     continue
        if not robust(suite, h, solar, sweeps=STAGE4):            continue   # Stage 4
        ok.append(h)
    return contiguous(ok)  # state separately: density-only band vs density+composition band
```

Report two nested bands: a wider "density" band and a narrower "density + O/N2" band. Then state how each moves between solar minimum and maximum. That answers the transcript's instruction to identify "the altitude range within that regime where their solution meets its stated performance" ([transcript p.4](https://occ.nasatechleap.org/wp-content/uploads/2026/09/NASA-TechLeap-Orbital-Clarity-Challenge_Information-Session-transcript-092226.pdf)) without overclaiming.

Two framing corrections make the OSSE results more defensible. First, compare against strong baselines as well as the degraded prior. HASDM's standard deviation of yearly-mean density ratio is about 5.0% at 400 km ([SWSC 2021 table](https://www.swsc-journal.org/articles/swsc/full_html/2021/01/swsc210039/T2.html)). A Starlink-assimilating WAM run reported 6.6% RMS, though that is a poster, not a peer-reviewed result ([CPAESS SWW 2026](https://cpaess.ucar.edu/abstract-2026-sww/multi-month-thermospheric-neutral-density-nowcast-and-forecast-using-multiple-low)). A claim like "3.4% versus 26%" invites the response that the 26% is a function of how badly the drivers were degraded, which the team's own 4-36% sweep proves.

Second, distinguish in situ estimation along the host track from global model improvement. Assimilated in situ densities mainly improve the model near the observing orbit ([two-step assimilation](https://www.researchgate.net/publication/366156651_Improving_the_estimation_of_thermospheric_neutral_density_via_two-step_assimilation_of_in_situ_neutral_density_into_a_numerical_model)). The Dietrich et al. constellation OSSE found observation count and coverage diversity dominated skill: a mixed-inclination 520 km design won ([Dietrich et al. 2024](https://par.nsf.gov/servlets/purl/10608384)). A fleet-size sweep over 5-200 hosts with a realistic host-altitude mix would be novel evidence; no published in situ thermosphere OSSE gives a minimum host count. Minter et al.'s composition Kalman-filter OSSE, under 6% error from 15%-error observations, is the only published composition benchmark to quote alongside ([EarthRef](https://earthref.org/ERR/84356)).

### Instrument numbers the simulation needs

Each entry below should come from a datasheet, a flight paper or a lab measurement, never a guess. Where no source exists, it should be swept across a range rather than fixed.

| Channel | Parameters (current best source or status) |
|---|---|
| **Gauge** | Range floor and ceiling (MAG084 1e-6 to 0.5 Pa; MIGSI ~1.3e-6 Pa floor). Absolute gain error and unit-to-unit scatter (30% datasheet; 20-25% inverted magnetron). Repeatability (5%). Noise at 1 Hz. Gain drift or random-walk rate (**unmeasured, top priority**). Temperature coefficient. Power-law exponent and knee (~1.0 down to 1e-9 Torr). Gas factors He 0.16-0.19, O2 0.90-1.01, effective O (**unmeasured**; sweep with recombination efficiency). Ram/angle response and pointing tolerance (MIGSI ≤1°). Chamber Tw and accommodation. Outgassing background and decay time. Ignition delay. Duty cycle; filament life (hot cathode) |
| **O sensor** | Sensitivity to O versus O2 (Au/Pt cell pair). Absolute calibration accuracy (**unpublished**). Noise and bandwidth (100 Hz demonstrated). Gain drift and ageing over 1 year (**unpublished**; ISS ran 572 days). Angular response (~180° FOV). Heater power (~1 W, unverified). Temperature dependence |
| **Drag / host** | C_D prior by altitude (5-10% below 400 km, 15-25% near 500 km). Host area-to-mass and attitude knowledge. POD noise and fit-arc length (sets effective cadence). Maneuver frequency. Whether the host carries a dual-frequency receiver |
| **Fleet / orbit** | Host altitude, inclination and LTAN distribution; N_hosts; crossover frequency for cross-calibration; data latency; payload duty cycle (LLITED fell below 60%) |
| **Cost / SWaP per unit** | Head price ($0.43-2.3k catalog), electronics, chamber, per-unit calibration labor. The notes' $2-6k recurring estimate is an unsourced estimate, not a quote |

## Unverified numbers and open questions

The items below must not go into the submission as fact until resolved. Several came from earlier team materials or from search-result summaries rather than primary text.

| Item | Status |
|---|---|
| MIGSI "<10% at 100 Hz" (earlier team materials) | **Not supported.** Sources give 1 Hz and 20% accuracy; 100 Hz belongs to LLITED's PIP plasma probe ([LLITED slides](https://spdf.gsfc.nasa.gov/pub/data/aaa_smallsats_cubesats/llited/documents/LLITED-presentation-2026-00325.pdf)) |
| "LLITED: NRLMSISE-00 58% storm underestimate" | Per the team's copy of Swanson et al. 2026 (DOI 10.1029/2026JA035137); **unverified by this research**, because the paper returned HTTP 403 |
| MAG084 "4% accuracy" (team slide) | **Wrong**: datasheet says 30% of reading (N2, typical). "Use indoors only" and the +5 °C minimum need a vendor conversation or a qualification plan |
| Gauge sensitivity to atomic O; chamber O→O2 recombination efficiency | Never measured in available sources; sweep in the OSSE and plan a lab measurement |
| FIPEX accuracy, power, lifetime drift, unit cost, licensing | Not published in sources found; SWARM-EX launch unconfirmed |
| Team hypothesis "drag C_D anchors absolute density" | Strongly implied by filter structure (analysis above); confirm with a C_D-prior sweep. The ±7% value itself is optimistic near 450-500 km |
| QQ-Satellite "~19%" gauge-vs-GPS | Sun et al. report 18.77% but the comparison referent is unclear; do not cite as gauge-vs-POD |
| "Spire/Mutschler OSSE 5-25%", "~50% storm O/N2 drop", HASDM "2-10%" | No primary source found |
| O-He transition height versus F10.7 | Not found citable; compute from NRLMSIS 2.1 and cite the model |
| No orbital flight of a commercial cold-cathode gauge on a small satellite | Search found none; a heritage risk for the MAG084/MKS 423 route |
| Phase 1 winner date | Website says January 2027; info session said December 2026 |
| Notes' pressure table | Superseded by the team's NRLMSIS 2.1 calculation |

## Conclusion

The research changes what the "density channel" is for. In a fused suite the gauge buys precision and cadence, the O sensor buys separability, and absolute accuracy comes from whichever calibration is most trustworthy. Today that is an assumed drag coefficient, which the literature says is uncertain by 15-25% exactly where helium starts to matter. The most valuable next simulations and lab work are therefore not better gauge specs. They are three things: a C_D-prior sweep, a measured gain-drift rate for the chosen gauge and O cell, and a lab measurement of how the chamber converts atomic oxygen. Each attacks a term that the observability algebra shows is otherwise invisible.

The strategic implication for the proposal is to lean into a credible, nested claim: density from VLEO to roughly 500 km, and density plus O/N2 from VLEO to roughly 450 km. Present helium and 700-800 km as upgrade paths through a mass spectrometer or multi-altitude fleet inversion, not as current capability. That scoping is honest about the cheap-instrument flight record. It also hits the two things the rubric and Bruinsma most want: composition back in situ for the first time since the early 1980s, and many hosts sampling storms continuously. Its credibility then rests on an OSSE whose rankings visibly survive truth models other than MSIS.
