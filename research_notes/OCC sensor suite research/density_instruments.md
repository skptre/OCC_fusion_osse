# Low-cost in-situ neutral density / pressure instruments for the thermosphere (small-sat, sounding rocket, hosted payload)

Evidence labels used throughout: **[FLIGHT]** = flight-demonstrated, **[GROUND]** = lab/ground test, **[DATASHEET]** = vendor spec, **[CLAIM]** = proposal/announcement/secondary claim, **[INFERENCE]** = my own calculation or reasoning.

Research run: 2026-10-11. Two key 2026 papers (Swanson et al. 2026 JGR, DOI 10.1029/2026JA035137; Lehmacher et al. 2026 JGR, DOI 10.1029/2026JA035338) returned HTTP 403 and could not be read in full. Their numerical results are listed under Gaps.

---

## Q1. Hot-cathode (Bayard-Alpert) ionization gauges: MIGSI/LLITED, Streak, earlier ram gauges

### Takeaway
MIGSI (UNH, PI J. Clemmons) is the main flown CubeSat hot-cathode density gauge. It is a Bayard-Alpert sensor in a roughly 6 cm spherical accommodation chamber, with 0.6 kg, 0.5U, about 3 W of payload power, a range of 1e-8 to 1e-2 (or 1e-3) Torr, 1 Hz sampling, and a stated 20% accuracy. It flew on LLITED (two 1.5U CubeSats, launched April 2023, 350-500 km, reentered August 2024). It descends from the Aerospace Corp. Streak gauge, which used miniature commercial BA sensors. The figures the brief quoted ("<10% sensitivity, 100 Hz") do not match any source I found: 100 Hz belongs to LLITED's PIP plasma probe, and MIGSI is listed at 1 Hz.

### Cited findings
- **MIGSI design [FLIGHT/CLAIM]:** It has three parts: a Bayard-Alpert sensor, an accommodation chamber, and a controller. It measures pressure inside the chamber. It is a modified version of the Aerospace Corp. ionization gauge that flew on STREAK. The aperture must face ram, which requires a 3-axis-stabilized spacecraft aligned within 1° of the velocity vector. — [eoPortal LLITED](https://www.eoportal.org/satellite-missions/llited)
- **MIGSI SWaP [CLAIM, pre-flight table]:** 0.6 kg, 0.5U volume (electronics board about 10 x 9 x 1 cm, chamber about 6 cm spherical), 2.73-3.5 W average payload power on a +5/+12 V bus, 60% orbit duty cycle planned. — [eoPortal LLITED](https://www.eoportal.org/satellite-missions/llited)
- **MIGSI performance [CLAIM]:** Range 1e-8 to 1e-2 Torr, accuracy 20%, 1 Hz sampling, about 400 m horizontal cell size, TRL 4 pre-flight with heritage from the LAICE CubeSat. eoPortal is internally inconsistent: the text gives 0.1% precision and the requirements table gives 10%. — [eoPortal LLITED](https://www.eoportal.org/satellite-missions/llited)
- **MIGSI range, mission team slides (Feb 2026) [FLIGHT team doc]:** "Ionization Gauge measures pressure; convert to density and neutral wind measurements; Measurement range: 10^-3 to 10^-8 torr". The same slides give 100 Hz for the PIP Langmuir probe, not for MIGSI. — [Bishop et al., LLITED presentation, 12 Feb 2026 (OTR 2025-00325)](https://spdf.gsfc.nasa.gov/pub/data/aaa_smallsats_cubesats/llited/documents/LLITED-presentation-2026-00325.pdf)
- **LLITED orbit and timeline [FLIGHT]:** Launched 15 April 2023 (16 April per the slides) on SpaceX Transporter-7 from Vandenberg. The planned orbit was 496 km circular at 96.5°. The actual orbit was about 513.8 x 495.7 km, 97.4°, nearly sun-synchronous, LTDN 22:30, because the "wrong deployer door" was activated. Deployment was 15 May 2023, payload commissioning finished 8 Sep 2023, and the mission ended in late August 2024. The spacecraft lost 8-12 km of altitude in the week of the May 2024 Gannon storm. — [LLITED slides 2026](https://spdf.gsfc.nasa.gov/pub/data/aaa_smallsats_cubesats/llited/documents/LLITED-presentation-2026-00325.pdf); [eoPortal](https://www.eoportal.org/satellite-missions/llited)
- **LLITED failure modes and lessons [FLIGHT]:**
  - A solar cell anomaly cut power to below 50% of the expected level. This forced lower payload duty cycles, near-daily commanding, and focused campaigns. LLITED-B collected MIGSI and PIP data; LLITED-A mainly PIP.
  - Planned differential-drag separation maneuvers became impossible.
  - Ground stations in Maine and Hawaii were lost.
  - Programmatics: proposal 2016, COVID shutdown, a canceled second launch, and delivery/launch slips meant about 7 years from proposal to launch.
  - Team lesson: "Initial phrasing and focus of science questions/objectives essential for adaptability."
  - Sources: [eoPortal](https://www.eoportal.org/satellite-missions/llited); [LLITED slides](https://spdf.gsfc.nasa.gov/pub/data/aaa_smallsats_cubesats/llited/documents/LLITED-presentation-2026-00325.pdf); [NASA S3VI webinar page](https://www.nasa.gov/smallsat-institute/community-of-practice/lessons-learned-from-the-llited-mission/)
- **LLITED MIGSI science uses [FLIGHT]:** October 2023 partial eclipse neutral profiles compared with MSIS; high-latitude neutral density over a solar rotation; coincidence with PIANO/ISS; May 2024 storm. Level-2 MIGSI data are public in netCDF on NASA SPDF. — [LLITED slides](https://spdf.gsfc.nasa.gov/pub/data/aaa_smallsats_cubesats/llited/documents/LLITED-presentation-2026-00325.pdf)
- **Swanson et al. 2026 [FLIGHT, results not retrieved]:** D. J. Swanson, H. Liu, R. Bishop, J. H. Clemmons, S. Debchoudhury et al., "High Latitude Thermosphere and Ionosphere Density Response to the May 2024 Geomagnetic Storm Observed by the LLITED CubeSat Mission," JGR Space Physics 131(7), June 2026, DOI 10.1029/2026JA035137. Analysis code is on Zenodo ("djswanson/LLITED: LLITED May 2024 Storm"). The method compares storm-time and quiet-time observations and checks them against empirical and physics-based models. — [Zenodo record](https://zenodo.org/records/18622925); [amisr.com bib](https://amisr.com/publications/r.+bishop/); [Swanson PBASE report](https://www.isee.nagoya-u.ac.jp/dimr/PBASE/report/2024/Diana_Swanson_E.pdf)
- **Streak heritage gauge [FLIGHT]:** Clemmons et al., "The Ionization Gauge Investigation for the Streak Mission," Space Sci. Rev. 145, 263-283 (2009), DOI 10.1007/s11214-009-9489-6. Streak (STP-R1, DARPA) was a very-low-LEO satellite whose instruments reportedly included an ion gauge and an atomic oxygen sensor. — [UNH FindScholars](https://findscholars.unh.edu/display/publication448950); [Gunter's Space Page, Streak](https://space.skyrocket.de/doc_sdat/streak.htm)
- **Aerospace BA gauge family [FLIGHT]:** "Bayard-Alpert Gauges for Space Research" (Clemmons, AVS 2006) describes two variants of one design built around small commercial off-the-shelf BA sensors to minimize spacecraft resources. The custom controller provides high-precision, high-rate sampling and DC filament regulation.
  - The suborbital variant samples at 1 kHz, with an accommodation chamber whose response lies between a planar aperture and a pitot tube.
  - The orbital variant uses a planar-aperture accommodation chamber and high-reliability electronics, and returned about 1 year of orbital data (Streak).
  - A special mode gives crude composition information.
  - The commercial sensor model is not named in the abstract.
  - Source: [AVS 53rd Symposium, VT-WeA3](https://www2.avs.org/symposium2006/Papers/Paper_VT-WeA3.html)
- **Flight data analysis with DSMC [FLIGHT]:** Sun, Cai, Boyd, Clemmons, Hecht, "Computational Analysis of High-Altitude Ionization Gauge Flight Measurements," J. Spacecraft & Rockets (2006). — [UMich Deep Blue](https://deepblue.lib.umich.edu/items/8af0e657-378b-48da-b6f5-8564c7172b4a/full)
- **Rocket hot-cathode heritage (CONE) [FLIGHT]:** CONE is a spherical hot-cathode gauge flown more than 20 times since the 1990s, with a design range up to about 1 mbar. — search summary of [science.gov cold-cathode topic page](https://www.science.gov/topicpages/c/cold+cathode+gauges.html) (secondary source)
- **Generic BA behavior [DATASHEET/vendor app note]:**
  - Collector current is linear in pressure. A mid-range sensitivity factor works from 1e-9 to 1e-4 Torr, with nonlinearity under ±25% across the range.
  - Repeatability is 1-2%. Accuracy better than ±50% needs individual calibration.
  - The controller alone can add up to ±15% error.
  - Filament life is "many thousands of hours" unless damaged by ion bombardment, overpressure, or chemistry. ThO2-coated Ir filaments are favored.
  - Hot filaments react with gas and change its composition, which matters for O and O2.
  - Electronics are more complex and power-hungry than for cold-cathode gauges.
  - Source: [SRS, Hot vs. Cold Ionization Gauges app note](https://www.thinksrs.com/downloads/pdfs/applicationnotes/IG1hotapp.pdf)
- **Miniaturization penalty [patent background]:** Shrinking BA electrode geometry well below standard size cuts sensitivity markedly and degrades accuracy and long-term stability. Long electron paths with small grids require high grid transparency. — [US patent 6198105 (mini ion gauge, multiple collectors)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6198105)
- **Commercial miniature BA heads exist [DATASHEET]:** MKS/Granville-Phillips "Mini Ion Gauge" and InstruTech hot-cathode products. I did not confirm prices or which head MIGSI uses. — [MKS Mini Ion Gauge](https://www.mks.com/f/mini-ion-gauge-vacuum-sensor); [InstruTech ion gauges](https://www.instrutechinc.com/products/ionization-vacuum-gauges)

### Inferences
- [INFERENCE] MIGSI is the closest flown analogue to a mass-producible hosted density gauge: 0.6 kg, 0.5U, about 3 W, and a range that covers the expected ram-chamber pressure at 200-800 km (see Q4). Its 3 W draw, mostly filament heating, and its need for 1° ram pointing are the main integration burdens for a hosted payload.
- [INFERENCE] The ±1° pointing requirement means a hosted payload on a host that does not fly ram-aligned would need either attitude knowledge plus an angular-response model, or a chamber with a wider acceptance angle.
- [INFERENCE] Filament life: thousands of hours (ground claim) is roughly 0.1-0.5 years of continuous operation. Duty cycling, as LLITED did at 60% or less, and dual filaments are the usual mitigations. Iridium filaments, especially ThO2- or Y2O3-coated, tolerate oxygen better than tungsten. That matters because the gauge sees about 1e-6 to 1e-5 Torr of O and O2 in the chamber.

### Gaps
- No MIGSI unit cost, filament material, or exact commercial BA head part number was found.
- No flight-demonstrated MIGSI accuracy versus MSIS or other truth was retrieved. The Swanson et al. (2026) abstract and storm enhancement numbers could not be fetched (HTTP 403). The "<10% sensitivity, 100 Hz" figures in the brief could not be sourced.

---

## Q2. Cold-cathode / inverted magnetron / Penning gauges, and suitability of INFICON MAG084, Pfeiffer IKR, MKS 423

### Takeaway
Commercial cold-cathode gauges have flown many times on sounding rockets (Lehmacher/Clemson, 90-325 km, 2013 to 2026) as cheap density sensors in spherical antechambers, and Redhead cold-cathode gauges flew on Explorer 32. I found no CubeSat flight of a commercial cold-cathode gauge. For a 100+ unit build, cold-cathode heads are attractive: about $430-$2,300 per head, no filament, and simple, under-1 W electronics. The drawbacks are 3-6 kV HV, a magnet, ignition delay at low pressure, nonlinearity with discontinuities, and only about 30% stated accuracy. These are workable but need per-unit calibration.

### Cited findings
- **Rocket flights with adapted commercial cold-cathode gauges [FLIGHT]:**
  - Lehmacher, Gaulden, Larsen, Craven (2013), "Multiple neutral density measurements in the lower thermosphere with cold-cathode ionization gauges" (JGR). A commercial gauge was adapted as a low-cost instrument with a spherical antechamber so it operated in molecular flow over 90-200 km.
  - Three roll-stabilized payloads each carried two gauges, one for upleg ram and one for downleg ram.
  - Density profiles were integrated below 125 km to obtain temperature.
  - Sources: [ResearchGate](https://www.researchgate.net/publication/258794665_Multiple_neutral_density_measurements_in_the_lower_thermosphere_with_cold-cathode_ionization_gauges); [science.gov](https://www.science.gov/topicpages/c/cold+cathode+gauges.html)
- **Lehmacher, Larsen, Kaeppler (2026), JGR, DOI 10.1029/2026JA035338 [FLIGHT]:** Seven temperature and number-density profiles from four auroral rocket campaigns, 2019-2024.
  - Two types of COTS ionization gauges were used, with apogees of 145-325 km.
  - Absolute density depends on the ram factor for supersonic rarefied flow and on the transition to continuum flow.
  - Results: up to +200 K near 120 km and up to +50% density at 140 km during disturbed conditions.
  - Gauge models were not retrieved (403).
  - Source: [AGU abstract page](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/2026JA035338), via search snippet
- **Satellite cold-cathode heritage [FLIGHT]:** Explorer 32 (1966) carried three cold-cathode magnetron (Redhead) density gauges. — [Wikipedia: Explorer 32](https://en.wikipedia.org/wiki/Explorer_32)
- **Embry-Riddle SpEED Demon (August 2022) [FLIGHT]:** An ionization gauge on the main payload cross-validated MEMS accelerometer densities. — [ERAU Discovery Day](https://commons.erau.edu/cgi/viewcontent.cgi?article=1746&context=discovery-day)
- **Cold-cathode physics and limitations [DATASHEET/app note]:**
  - Crossed E and B fields: 2-6 kV and 1-2 kG.
  - Typical range is 1e-2 to 1e-9 Torr; claims below 1e-9 Torr deserve "extreme caution."
  - Current vs. pressure is a power law. The exponent is about 1.0 from 1e-4 to 1e-9 Torr and jumps to 1.25 or more between 1e-9 and 1e-10 Torr (the "magnetron knee"). Spurious discontinuities occur, least in inverted magnetrons.
  - Repeatability about ±5%; sensor-to-sensor matching 20-25% for inverted magnetrons; vendors often specify accuracy within a factor of 2.
  - Striking delay ranges from seconds at 1e-6 Torr to hours at 1e-10 Torr. Strikers (edge emitters, radioactive sources, UV) or switching on at higher pressure mitigate it.
  - Electronics are under 1 W, with HV current limited to about 0.1 mA. Stray fields from inverted magnetrons are a few gauss.
  - Failure modes: insulating films from polymerized hydrocarbons, and sputtered metal causing insulator leakage.
  - Source: [SRS Hot vs. Cold app note](https://www.thinksrs.com/downloads/pdfs/applicationnotes/IG1hotapp.pdf)
- **INFICON MAG084 [DATASHEET]:**
  - Inverted magnetron with a double ionization chamber; range 1e-8 to 5e-3 mbar.
  - Accuracy 30% of reading (N2); repeatability 5% (N2).
  - NdFeB magnets in a closed magnetic circuit with a shielding enclosure; tolerates short exposure to 600 mT.
  - Ignition aid on the anode for faster low-pressure ignition. Bakeable to 230 °C; radiation tolerant to 1e7 Gy.
  - Wetted materials: stainless steel, Al2O3, Ag, Mo.
  - Requires the external VGC094 controller (cable up to 100 m). Part numbers 399-849 (DN40 ISO-KF) and 399-850 (DN40 CF-F).
  - The web page states no HV value, mass, or power. The 3.3 kV figure in the brief is unconfirmed.
  - Source: [INFICON MAG084 product page](https://inficon.com/en/products/vacuum-gauge-and-controller/mag084)
- **INFICON IKR084/085/086 [DATASHEET]:** About ±30% of reading at 25 °C; gas-dependent. — [INFICON IKR08x manual](https://www.inficon.com/media/4508/download/IG9048BEN_A_Web.pdf?v=1&inline=true)
- **Unit prices [DATASHEET/retail]:**
  - MKS 423 I-Mag cold-cathode sensor (head only) on MKS's own site: $431 (NW25 KF), $453 (1 in. tube), $497 (NW40 KF), $569 (2.75 in. CF). A second group lists $1,026-$1,131; I did not resolve what distinguishes it.
  - Ideal Vacuum lists the same heads at $685-$837.
  - Pfeiffer IKR 361 C (ceramic-coated, KF25) costs about $2,070-$2,277 at AJVS.
  - Sources: [MKS 423 I-Mag](https://www.MKS.com/f/423-i-mag-cold-cathode-vacuum-sensors); [Ideal Vacuum 423](https://idealvac.com/en-bs/MKS-423-I-Mag-Cold-Cathode/pl/34-1932-472); [AJVS Pfeiffer](https://www.ajvs.com/library/Pfeiffer_Vacuum_PKR_361_IKR_361.pdf)

### Inferences
- [INFERENCE] **MAG084 suitability.** The range (7.5e-9 to 3.8e-3 Torr) covers the ram-chamber pressures from about 200 km to roughly 700 km (Q4). Near 800 km at solar minimum the pressure approaches or falls below the low end and the magnetron knee, so accuracy degrades.
  - It is a vacuum-flange laboratory head (DN40), bakeable and radiation hard, but heavy for a CubeSat. Its mass is not on the web page; DN40 all-metal heads usually weigh a few hundred grams or more, unverified.
  - It needs a separate VGC094 rack controller. A flight version would need a custom HV supply and electrometer, the same approach Lehmacher's team used.
  - The NdFeB magnet's stray field matters for host magnetometers and magnetorquers, and it creates a residual dipole torque. The MAG084's closed circuit and shield are advantages here.
- [INFERENCE] Cold-cathode advantages for a 100+ build: no filament wear-out, much lower power (under 1 W versus about 3 W for MIGSI), and heads at $0.4-2k. Disadvantages: kV HV in vacuum, which brings corona and arcing risk at intermediate pressures during ascent, so turn-on must be delayed until outgassing is done. Ignition at about 1e-7 Torr may take seconds to minutes; this needs an ignition aid or a strike during early-orbit outgassing. Each unit needs its own calibration curve because of power-law response and 20-25% unit-to-unit scatter.
- [INFERENCE] An MKS 423 or similar head (about $500) plus a custom controller is plausibly the cheapest route to a gauge-based hosted density sensor, but it has not flown on CubeSats. Rocket heritage (Lehmacher) is the evidence base.

### Gaps
- No orbital (CubeSat or ISS) flight of a commercial cold-cathode gauge was found. I could not confirm whether any 2010s-2020s CubeSat flew one.
- The specific commercial gauge models used by Lehmacher (2013, 2026) were not retrieved.
- MAG084 HV, mass, power, and price were not published on the web page. MKS 423 and Pfeiffer IKR/IMR specs were not fetched in detail. Agilent heads were not researched.

---

## Q3. Gas correction factors, including atomic oxygen; O recombination; ram-to-ambient conversion

### Takeaway
BA relative sensitivities are well tabulated: N2 1.00, O2 1.01, He 0.18, H2 0.46, Ar 1.29, CO2 1.42, with 10-20% uncertainty. The sensitivity to atomic oxygen has never been well measured; space gauges estimate it from ionization cross-section ratios. Instrument design handles this by letting O recombine to O2 on the chamber walls (a "closed source"). The chamber then holds a thermally accommodated O2/N2/He mix at wall temperature, and density follows from flux balance (the ram factor).

### Cited findings
- **BA relative sensitivity (gas correction) factors [DATASHEET, relative to N2 = 1.00]:** He 0.18, H2 0.46, N2 1.00, O2 1.01, Ar 1.29, CO2 1.42.
  - Literature discrepancy is no more than about 10% for common gases and a little over 20% for less common ones.
  - Factors are pressure dependent, so individual calibration with the specific gas is recommended.
  - The industry standard source is R. L. Summers' NASA compilation. Rg is approximated by the ratio of ionization cross sections at 150 eV.
  - Source: [SRS Gas Correction Factors app note](https://cornestech.co.jp/wp-content/uploads/2022/01/App_IG1BAgasapp.pdf)
- **Cold-cathode gas factors [DATASHEET]:** Gas-dependent like BA gauges, but specified as N2-equivalent. The MAG084 page gives no non-N2 factors. — [INFICON MAG084](https://inficon.com/en/products/vacuum-gauge-and-controller/mag084)
- **Atomic oxygen sensitivity [GROUND/historic]:** A NASA report on satellite-borne gauges states that ionization gauge sensitivity to atomic oxygen had not been measured. It estimated the value from the ratio of ionization cross sections, called that the best available approach, and said an error estimate would be hard because O is too reactive to predict inside a gauge. — [NASA NTRS 19660028088](https://ntrs.nasa.gov/api/citations/19660028088/downloads/19660028088.pdf)
- **O recombination and chamber design [GROUND/review]:** Recombination of O on ion-source surfaces is a major issue. "Closed" sources force complete recombination inside an accommodation volume, so O is measured as O2 with predictable calibration. "Open" sources minimize surface contact. — [NASA NTRS 19870016743](https://ntrs.nasa.gov/api/citations/19870016743/downloads/19870016743.pdf)
- **Ram factor and antechamber [FLIGHT]:**
  - A gauge facing supersonic flow reads high, because directed kinetic energy adds to thermal energy. Spherical (Paterson-probe-type) antechambers are used, and a computed ram factor corrects the reading.
  - Ram-factor profiles agreed very well with empirical ratios of ionization gauge to falling-sphere densities in the MLT, quantified with Monte Carlo (DSMC) and wind tunnel work.
  - Sources: [ERAU Graves CEDAR 2023](https://daytonabeach.erau.edu/-/media/files/daytona-beach/college-of-arts-and-sciences/research/sail/graves-cedar-2023.pdf); [Rapp et al., Ann. Geophys. 19, 571 (2001)](https://opac.geologie.ac.at/ais312/dokumente/copernicus.org/angeo-19-571-2001.pdf); [DSMC extraction paper](https://www.researchgate.net/publication/253097963_Extraction_of_neutral_gas_parameters_from_ionization_gauge_measurements_in_the_lower_thermosphere_using_DSMC_calculations)
- **Accommodation chamber principle [GROUND/NASA]:** The collected ion current is proportional to the chamber pressure, and chamber pressure relates to the ambient state through the ram flux balance. — [NASA NTRS 19960000975 (satellite anemometer)](https://ntrs.nasa.gov/citations/19960000975)

### Inferences
- [INFERENCE] **Orbital ram-to-ambient conversion.** For a chamber with a thin orifice facing ram at speed V about 7.6 km/s, with gas fully accommodated to wall temperature Tw, the balance is: inflow n_a·V·cos(θ) (hypersonic limit, speed ratio V/v_mp of about 7-8 for O at 1000 K) equals outflow n_c·c̄_w/4, with c̄_w = sqrt(8kTw/πm).
  - Result: n_c/n_a ≈ 4V·cosθ / c̄_w. At Tw = 300 K, c̄_w is about 476 m/s for N2, 445 for O2, 630 for O, and 1260 for He.
  - So n_c/n_a is roughly 64 for N2, 48 for O, and 24 for He. If O fully recombines (2 O → O2), the chamber number density for that component halves relative to O-atom inflow.
  - Chamber pressure is p_c = n_c·k·Tw. Composition (from a model such as MSIS) is therefore needed to convert the reading. This uncertainty is a large share of the 20% accuracy figure.
- [INFERENCE] Taking O → O2 recombination as complete, with Rg(O2) = 1.01 and Rg(He) = 0.18, the gauge is nearly blind to He. Above about 600 km at solar minimum, where He dominates, total-density retrieval needs a model-based composition correction and becomes less accurate.
- [INFERENCE] Hot filaments convert O and O2 chemically (CO, oxides on surfaces), which adds drift. Cold-cathode gauges avoid filament chemistry, but sputtered or oxidized cathode surfaces still change sensitivity over time.

### Gaps
- No modern measured value of ionization gauge sensitivity to atomic O relative to N2 was found. I found no flight paper quantifying the O recombination efficiency of the MIGSI or Streak chamber walls.
- Cold-cathode gas correction factors (He, O2, Ar, H2) for MAG084 or MKS 423 were not retrieved.

---

## Q4. Ambient and ram-chamber pressures, 200-800 km, versus gauge ranges

### Takeaway
At Tw = 300 K, ram-chamber pressures run from about 1e-5 Torr at 200 km to about 1e-8 Torr at 800 km. MIGSI's flown range (1e-8 to 1e-3 Torr) covers this with little margin at the top of the altitude band. The MAG084 (7.5e-9 to 3.8e-3 Torr) covers the same band nominally, but cold-cathode accuracy and ignition degrade near 1e-8 to 1e-9 Torr.

### Cited findings
- MIGSI range 1e-8 to 1e-3 Torr (team slides), or 1e-8 to 1e-2 Torr (eoPortal). — [LLITED slides](https://spdf.gsfc.nasa.gov/pub/data/aaa_smallsats_cubesats/llited/documents/LLITED-presentation-2026-00325.pdf); [eoPortal](https://www.eoportal.org/satellite-missions/llited)
- MAG084 range 1e-8 to 5e-3 mbar. — [INFICON](https://inficon.com/en/products/vacuum-gauge-and-controller/mag084)
- Cold-cathode gauges: range 1e-2 to 1e-9 Torr; exponent knee between 1e-9 and 1e-10 Torr; striking takes seconds at 1e-6 Torr and hours at 1e-10 Torr. BA gauges: 1e-3 to 1e-10 Torr, linear. — [SRS app note](https://www.thinksrs.com/downloads/pdfs/applicationnotes/IG1hotapp.pdf)

### Inferences
- [INFERENCE] Order-of-magnitude table, computed by me with typical MSIS-like moderate-activity number densities. These are not sourced values; verify with NRLMSIS for the OSSE. Ambient T is about 1000 K. The chamber uses a ram enhancement of about 50x at Tw = 300 K (lower, about 25x, where He dominates).

| Altitude | n_ambient (m^-3, approx.) | p_ambient (Torr) | p_chamber (Torr, approx.) |
|---|---|---|---|
| 200 km | ~7e15 | ~7e-7 | ~1e-5 |
| 300 km | ~1e15 | ~1e-7 | ~2e-6 |
| 400 km | ~3e14 | ~3e-8 | ~5e-7 |
| 500 km | ~1e14 | ~1e-8 | ~1.5e-7 |
| 600 km | ~3e13 | ~3e-9 | ~5e-8 |
| 800 km | ~5e12 (He/O) | ~5e-10 | ~5e-9 to 1e-8 |

- [INFERENCE] Ambient pressure above about 500 km is below 1e-8 Torr, so an un-chambered (nude) gauge would be out of range for both gauge types. The accommodation chamber's ram compression is essential, not optional. Solar-maximum and storm conditions raise densities by 2-10x, which helps. Solar minimum at 700-800 km is the hard case. Spacecraft outgassing near the gauge can add a background comparable to these chamber pressures early in a mission, so wake-side or zero-ram reference readings are needed.

### Gaps
- No sourced altitude-vs-chamber-pressure table for MIGSI or Streak was found. The values above are my estimates.

---

## Q5. Ram pressure / drag balance sensors (Broglio balance, UNICubeSAT)

### Takeaway
The Broglio drag balance flew on five San Marco satellites (1963-1988). The CubeSat version (UNICubeSAT, about 1 kg, 20% expected accuracy, needing perigee at 350 km or lower) never flew with the balance. The UniCubeSat-GG that launched on Vega in February 2012 swapped it for gravity-gradient booms and was never heard from. No CubeSat drag-balance density data exist.

### Cited findings
- **UNICubeSAT design [CLAIM]:** About 1 kg CubeSat with a Broglio drag balance that measures drag via displacement of light plates exposed to the incoming flux. Expected density accuracy 20%; needed perigee about 350 km or lower; planned for Vega's maiden flight. — [IAC-09 UNICubeSAT](https://iafastro.directory/iac/archive/browse/IAC-09/D1/1/4859/); [IAC-08 Broglio balance](https://iafastro.directory/iac/archive/browse/IAC-08/B4/4.B/1209/)
- **San Marco heritage [FLIGHT]:** The Broglio balance flew on 5 San Marco satellites, 1963-1988, with NASA. — [IAC-09](https://iafastro.directory/iac/archive/browse/IAC-09/D1/1/4859/)
- **What flew [FLIGHT, failed]:** UniCubeSat-GG launched 13 Feb 2012 on Vega into a 311 x 1439 km, 69.5° orbit. The drag balance had been replaced by gravity-gradient booms, and no signals were received. — [Gunter's Space Page](https://space.skyrocket.de/doc_sdat/unicubesat-gg.htm); [nanosats.eu](https://nanosats.eu/sat/unicubesat-gg)
- **Attitude effects [ANALYSIS]:** Felicetti and Santoni (2014) found that CubeSat attitude motion produces no frequency components that would affect drag-balance performance, confirmed by Monte Carlo. — [CORE](https://core.ac.uk/display/54498461)
- **Drag-torque density from attitude sensors [ANALYSIS]:** An MIT thesis reports about 1e-13 kg/m³ RMS error in simulation. — [MIT DSpace](https://dspace.mit.edu/server/api/core/bitstreams/58772ae7-693b-48a9-9fae-acc035409b61/content)

### Inferences
- [INFERENCE] A drag balance measures momentum flux directly, so it is composition-independent except through the drag coefficient. That is an advantage over gauges for He-rich altitudes. However, it has no flight heritage on small satellites, and its sensitivity falls off quickly above about 400 km.

### Gaps
- No balance mass, power, resolution, or cost figures were found for the CubeSat version.

---

## Q6. MEMS / small accelerometers for drag; GPS POD density (Spire, Mutschler, Swarm)

### Takeaway
MEMS accelerometers have shown drag-derived density only on sounding rockets in the mesosphere and lower thermosphere (SpEED Demon 2022: agreement with an ion gauge and MSIS within 10% at 80-100 km). Orbital drag at 400 km is roughly 1e-7 to 1e-6 g on a CubeSat, far below COTS MEMS noise floors. ESA's CubeSat accelerometer concepts (CASPA-ADM/CAITDM) use cold-atom interferometers on 16U, not MEMS. The cheap orbital route is GNSS precise orbit determination (POD) or drag on many small satellites (Spire, SoleiTool), which yields along-orbit averaged density rather than in-situ high-rate data.

### Cited findings
- **SpEED Demon / ERAU [FLIGHT, rocket]:** Low-cost MEMS accelerometers flew in August 2022. Drag density agreed with the ionization gauge and MSIS within 10% between 80 and 100 km. On a separate payload, MEMS agreed with an ion gauge up to 80 km. MEMS is useful only up to about 100 km. — [ERAU portfolio](https://portfolio.erau.edu/en/publications/mesosphere-lower-thermosphere-neutral-density-measurements-from-l/); [ERAU Discovery Day](https://commons.erau.edu/cgi/viewcontent.cgi?article=1746&context=discovery-day)
- **ESA-supported CASPA-ADM [CLAIM]:** A cold-atom accelerometer on a 16U CubeSat for thermospheric density, described as free of bias and scale-factor error. Converting acceleration to density also needs composition, temperature, and wind data, to be supplied by a mass spectrometer and wind sensor. Launch was targeted for the mid-to-late 2020s. — [EGU21-6009](https://meetingorganizer.copernicus.org/EGU21/EGU21-6009.html); [CEOI/Teledyne CAGE-CASPA](https://ceoi.ac.uk/wp-content/uploads/2021/07/CAGE-CASPA_reduced.pdf); [SPIE 12093](https://neurophotonics.spiedigitallibrary.org/conference-proceedings-of-spie/12093/1209305/Embedded-cold-atom-accelerometer-for-atmospheric-drag-measurement/10.1117/12.2619027.full)
- **Electrostatic accelerometer drift [CLAIM]:** Current drag accelerometers are electrostatic and drift with temperature-dependent voltage references. CAITDM is pitched as drift-free. — [CEOI case study CAITDM (2026)](https://ceoi.ac.uk/wp-content/uploads/2026/08/CEOI-Case-Study-CAITDM.pdf)
- **Miniature accelerometer target [CLAIM]:** The USU SmallSat 2010 "Atmospheric Drag Environment Sensor" was designed to resolve about 10 nano-g in 10 x 10 x 10 cm. — [USU SmallSat 2010](https://digitalcommons.usu.edu/smallsat/2010/all2010/7)
- **GNSS POD density from CubeSats [FLIGHT data, analysis]:**
  - Mutschler's dissertation (2022), "Global Thermospheric Density Estimation using CubeSat GPS Data and a Physics-based Space Environment Model," introduces the SoleiTool approach. — [CU vivo pubid 307684](https://vivo-cub.colorado.edu/display/pubid_307684)
  - Sutton, Thayer, Pilinski, Mutschler et al., "Toward Accurate Physics-Based Specifications of Neutral Density Using GNSS-Enabled Small Satellites," converts CubeSat POD into density time series and assimilates them. — [ESS Open Archive](https://essopenarchive.org/doi/full/10.1002/essoar.10506143.2)
  - POD-accelerometry beat EDR and DTM2000 in mean absolute percentage error over 45 storms, using GRACE-FO/CHAMP truth. — [arXiv 2408.16805](https://arxiv.org/html/2408.16805v2)
  - Constant, Mutschler et al. (AMOS 2025) study how POD noise, drag level, fit span, and spacecraft count affect EDR densities. — [AMOS](https://amostech.com/TechnicalPapers/2023/Poster/Ray.pdf) (listing; the exact URL may point to a related poster)

### Inferences
- [INFERENCE] Orbital drag acceleration is ρ·V²·Cd·A/(2m). With ρ about 3e-12 kg/m³ at 400 km, V = 7.6 km/s, Cd = 2.2, and A/m about 0.01 m²/kg, a ≈ 1.9e-6 m/s², or about 0.2 µg. At 600 km it is about 10x smaller. Good COTS MEMS (navigation grade) have noise of tens of µg/√Hz and bias instability of µg to tens of µg. MEMS therefore cannot resolve orbital drag in situ, consistent with the lack of any flight results. Electrostatic or cold-atom sensors are needed, at science-grade cost.
- [INFERENCE] For a cheap hosted payload, GNSS POD on the host (if it has a dual-frequency receiver) gives an orbit-averaged density essentially for free. It complements a gauge, which gives an in-situ, about 1 Hz, along-track density.

### Gaps
- No quantitative Mutschler 2023 accuracy figures (for example percent error versus GRACE-FO) were retrieved. Swarm GPS-derived density accuracy was not retrieved. No CubeSat MEMS flight noise-floor data were found.

---

## Q7. Other cheap in-situ options flown (context) and unit costs

### Takeaway
FIPEX (TU Dresden), a solid-electrolyte amperometric O/O2 sensor, is a low-cost, flight-proven species sensor: ISS EuTEF for about 18 months, QB50 CubeSats, and rockets at 100 Hz. It measures atomic oxygen rather than total density. For costs, commercial cold-cathode heads run $430-2,300. No MIGSI cost was found.

### Cited findings
- **FIPEX [FLIGHT]:** Flew on QB50-era 2U CubeSats (SpaceCube, QBUS-4), distinguishing atomic and molecular oxygen. It operated about 18 months on ISS EuTEF. On the WADIS-1 rocket (2013) it sampled at 100 Hz with vertical resolution better than 9 m and measured O peaks of about 3e10 cm^-3 at 94-96 km, with lab calibration against an O source. No CubeSat FIPEX results were found published. — [AMT 8, 3701 (2015)](https://amt.copernicus.org/articles/8/3701/2015/); [Gunter's SpaceCube](https://space.skyrocket.de/doc_sdat/spacecube.htm); [QBUS-4](https://space.skyrocket.de/doc_sdat/qbus-4.htm)
- **QB50 INMS [FLIGHT, brief context]:** Only about 1 month of data from the one working QB50 CubeSat. — [ESA indico](https://indico.esa.int/event/340/contributions/5813/)
- **Commercial gauge head prices [retail]:** MKS 423 I-Mag $431-$569 (MKS list) or $685-$837 (Ideal Vacuum); Pfeiffer IKR 361 C about $2,070-$2,277. — [MKS](https://www.MKS.com/f/423-i-mag-cold-cathode-vacuum-sensors); [Ideal Vacuum](https://idealvac.com/en-bs/MKS-423-I-Mag-Cold-Cathode/pl/34-1932-472); [AJVS](https://www.ajvs.com/pfeiffer-vacuum-high-current-23134)

### Inferences
- [INFERENCE] Bill-of-materials estimate for a 100+ unit hosted gauge: a commercial cold-cathode head ($0.5-2k) or a miniature BA head (likely $0.3-1k, unverified), plus a machined Al/Ti spherical chamber ($0.2-1k), plus custom HV/electrometer or emission-control electronics ($1-3k at volume). That gives roughly $2-6k recurring hardware per unit, before qualification, calibration, and integration labor. Per-unit calibration in a vacuum chamber against a spinning-rotor gauge or reference BA gauge (N2, O2, He) is likely the dominant recurring cost. These are rough estimates, not sourced.

### Gaps
- No MIGSI, Streak, or LAICE unit cost was found. No FIPEX mass, power, or cost was found.
