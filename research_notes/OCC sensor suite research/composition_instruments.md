# Low-cost small-satellite thermospheric neutral COMPOSITION instruments (flown)

Evidence labels: **[FLIGHT]** = data returned in orbit/suborbital flight; **[FLOWN-NO-DATA]** = launched, no published data found; **[GROUND]** = lab only; **[CLAIM]** = developer/pre-launch statement. Research budget was limited (~20 tool calls); several key primary papers (Eberhart 2015 full text, 2023 Progress in Aerospace Sciences review, Masutti IAC-17 full text, SWARM-EX NSF paper PDF) could not be read in full. Items from background knowledge that could not be re-verified are confined to Gaps and marked UNVERIFIED.

## Q1. FIPEX solid-electrolyte atomic/molecular oxygen sensor (TU Dresden / Uni Stuttgart IRS)

### Takeaway
FIPEX is the only true low-cost, small, flight-proven *species-selective* O / O2 sensor for small sats: flown on the ISS (EuTEF on Columbus, 572 days), a sounding rocket (WADIS-1, 100 Hz, <9 m vertical resolution), and several QB50 CubeSats, and it is manifested on CU Boulder's SWARM-EX together with a Langmuir probe. It measures only oxygen (O and O+O2). It does not measure N2 or He. Published QB50 FIPEX results and a confirmed SWARM-EX launch could not be found.

### Cited Findings
- **Principle [FLIGHT]:** solid-oxide-electrolyte (zirconia-type) amperometric microsensor. A gold cathode (non-dissociative reaction) detects atomic O, and a platinum anode (dissociative adsorption) detects O + O2, so a pair of heads separates O from O2. The sensor head has about 180° field of view. — [AMT/QB50 sources via search, spaceflight101 QB50P2](https://spaceflight101.com/spacecraft/?p=1986); [ESA "FIPEX on ISS"](https://www.esa.int/ESA_Multimedia/Images/2008/07/FIPEX_on_ISS)
- **Lineage:** ESA describes the FIPEX sensors as solid-oxide-electrolyte microsensors developed by TU Dresden. A separate ESA caption calls the sensor a spin-off of a ceramic gas sensor developed by ESA and the University of Stuttgart, originally meant to measure atomic oxygen around re-entry vehicles. ESA also pictured a commercial derivative, the "VacuSen" vacuum/plasma sensor from German company ESCUBE (a possible procurement route). — [ESA FIPEX on ISS](https://www.esa.int/ESA_Multimedia/Images/2008/07/FIPEX_on_ISS); [ESA VacuSen/ESCUBE](https://www.esa.int/ESA_Multimedia/Images/2011/04/VacuSen_sensor)
- **ISS flight [FLIGHT]:** launched February 2008 on STS-122 Atlantis and installed on the EuTEF external platform on Columbus. It measured O concentration along the ISS orbit for **572 days** (about 19 months). PI was Stefanos Fasoulas (TU Dresden). Tino Schmiel (TU Dresden) called these the first location- and time-resolved AO measurements in LEO. — [ESA DE "Gefahr im Orbit"](https://www.esa.int/Space_in_Member_States/Germany/Gefahr_im_Orbit_Hochreaktive_Sauerstoffatome); [TU Dresden news 2008](https://tu-dresden.de/tu-dresden/newsportal/news/spaceshuttle); [EuTEF Wikipedia](https://en.wikipedia.com/wiki/EuTEF)
- **Eberhart et al. 2015, AMT 8, 3701–3714 (WADIS-1 rocket, Andøya, June 2013) [FLIGHT]:** first use of solid-electrolyte sensors to measure AO selectively on a sounding rocket. Sensors were lab-calibrated with a microwave-plasma AO source against a mass spectrometer, which was itself calibrated for O by a methane-based method. Sampling was **100 Hz** with vertical resolution **better than 9 m**. Peak [O] was about **3×10^10 cm^-3** at 93.6 km (upleg) and 96 km (downleg). Results were compared with VUV resonance absorption and MSIS. Aerodynamic (ram/shock) effects were assessed with flow simulations. — [AMT 2015](https://amt.copernicus.org/articles/8/3701/2015/)
- **QB50 [FLOWN; outcome unclear]:** QB50P2 (2U) was identical to QB50P1 except that it carried FIPEX instead of INMS. QB50 assigned one of three MSSL-coordinated science units to each CubeSat: INMS, FIPEX, or the multi-Needle Langmuir Probe (mNLP). eoPortal lists Atlantis, Columbia and others as FIPEX carriers. — [spaceflight101 QB50P2](https://spaceflight101.com/spacecraft/?p=1986); [IAC-17 Masutti abstract](https://iafastro.directory/iac/archive/browse/IAC-17/B4/2/40579/); [eoPortal nSight-1](https://directory.eoportal.org/satellite-missions/nsight-1)
- **QB50 constellation health:** 36 CubeSats flew (down from >50 planned). 28 deployed from the ISS on 18 Apr 2017 and 8 launched on PSLV on 23 Jun 2017. 9 of 36 were dead on arrival, about one third were inactive after one year, and 3 had already de-orbited. — [QB50 IPPW 2018 slides (search snippet; PDF later 404)](https://colorado.edu/event/ippw2018/sites/default/files/attached-files/21_-_qb50_ippw_2018_v1.pdf)
- **SWARM-EX [CLAIM/manifested]:** three 3U CubeSats from CU Boulder and Olin College, testing formation flying, crosslinks, propulsion and autonomy. The payload is **a Langmuir probe plus a FIPEX**. The mission was selected by NASA CSLI (ELaNa) in 2021. nanosats.eu (updated May 2024) listed it as not launched, targeting ELaNa 59 around 31 Dec 2024. Gunter's Space Page still lists the launch as "202x" with no vehicle. — [CU Boulder project](https://www.colorado.edu/aerospace/academics/graduates/graduate-projects/2022-2023-projects/space-weather-atmospheric-reconfigurable); [Gunter's Space Page](https://space.skyrocket.de/doc_sdat/swarm-ex.htm); [nanosats.eu](https://nanosats.eu/sat/swarm-ex); [NSF PAR paper](https://par.nsf.gov/servlets/purl/10582655)

### Inferences
- FIPEX is a heated ceramic amperometric cell, functionally similar to automotive wide-band lambda sensors. At 100+ units the sensor elements should be cheap; the cost drivers are heater power, the precision current electronics, and calibration against an AO beam.
- Because it responds to O2 as well as O and has a wide (~180°) field of view, absolute accuracy depends on modeling ram flux, surface recombination and spacecraft attitude. Expect a "relative density, cross-calibrated to a model" product rather than an absolute standard.
- For an OCC hosted payload, FIPEX is the strongest candidate for cheap in-situ O/O2. It gives no N2 or He, so O/N2 needs another sensor or a model.

### Gaps
- Heater temperature and power were not verified in a source. From background knowledge (UNVERIFIED), the electrolyte operates around 600–700 °C and a sensor head draws on the order of 1 W.
- No published QB50 FIPEX science results were found, nor how many FIPEX CubeSats returned data.
- SWARM-EX launch status as of Oct 2026 is unconfirmed. Search found no launch record, and its 2024 ELaNa target is stale.
- No accuracy figure (e.g. ±%) or lifetime/degradation rate was found. Licensing terms (TU Dresden, IRS Stuttgart, ESCUBE) and unit cost were not found.
- Attitude dependence was not quantified in the sources reached.

## Q2. Atomic-oxygen actinometers / material-degradation sensors (silver, carbon, osmium films; ORMADD)

### Takeaway
These are the cheapest AO sensors (resistance or optical change of an erodible film), and some have flown on small sats (TAUSAT-1 ORMADD, TianTuo-1, STRV-1a). They are consumable, measure only AO fluence/flux (no O2, N2 or He), and respond slowly. That makes them sensors of integrated AO dose, not high-cadence density instruments, so they have little value for OSSE-grade composition.

### Cited Findings
- **Principle:** a thin conducting film (silver, carbon, osmium) oxidises or erodes in AO flow, and its resistance rise tracks cumulative fluence. Calibration is needed for atmospheric use. — [DTIC AD0779492](https://apps.dtic.mil/sti/html/tr/AD0779492/index.html); [Southampton eprints](https://eprints.soton.ac.uk/21740/)
- **Silver limits:** STRV-1a results suggest silver resistance sensors suit low-flux environments. Silver forms an oxide layer, and a Beijing institute paper concludes it is unsuitable for long-duration flight. NASA notes that silver's reactivity can exhaust the film even at the lower AO densities of higher orbits. — [Southampton eprints](https://eprints.soton.ac.uk/21740/); [NASA NTRS 19950021213](https://ntrs.nasa.gov/api/citations/19950021213/downloads/19950021213.pdf)
- **Small-sat silver design [CLAIM/GROUND]:** a 1.1 μm silver film sampled at 1 Hz was designed for IDEASSat Lite (NCU, Taiwan). — [NCU repository](https://ir.lib.ncu.edu.tw/handle/987654321/88132)
- **Carbon films:** the Southampton work on carbon-based AO sensors includes the STORM detector on the EuTEF/MEDET platform alongside FIPEX. — [CORE carbon AO sensors](https://core.ac.uk/works/325912); [Southampton eprints 155253](https://eprints.soton.ac.uk/155253)
- **TianTuo-1 [FLIGHT, data unverified]:** 9.3 kg NUDT nanosat launched 10 May 2012 into a 468 × 471 km, 97.2° orbit, with on-orbit AO detection among its objectives. It decayed on 3 Nov 2014. — [Gunter's TT-1](https://space.skyrocket.de/doc_sdat/tt-1.htm); [N2YO](https://www.n2yo.com/satellite/?s=38258)
- **ORMADD on TAUSAT-1 [FLIGHT]:** the On-orbit MAterial Degradation Detector (Soreq NRC / Bar-Ilan / Tel Aviv University, Israel) is a low-cost detector made of PV cells under semi-transparent AO-erodible coatings. Two units flew on the 3U TAUSAT-1, deployed from the ISS in March 2021. One had an amorphous-carbon coating and the other a thick pyrolytic Kapton film. The derived average AO flux was comparable to SPENVIS model predictions (Acta Astronautica 2023). Gouzman et al. (MRS 2023) call it one of two cost-effective AO monitoring methods from their lab. — [BIU CRIS](https://cris.biu.ac.il/en/publications/measurements-of-material-erosion-in-space-by-atomic-oxygen-using-/); [MRS 2023](https://mrs.org/meetings-events/presentation/2023_mrs_spring_meeting/2023_mrs_spring_meeting-3835154)
- **2023 review:** "A review of satellite-based atomic oxygen sensing methods," Progress in Aerospace Sciences, Feb 2023. Only citation metadata was reachable. — [Altmetric listing](https://nature.altmetric.com/details/13283649/citations)

### Inferences
- These are cheap (PV cells or films plus an ADC, roughly milliwatts to 0.2 W), but the film is consumed, so lifetime trades against sensitivity. Temperature affects both resistance and reaction rate. Output is effectively an orbit-averaged flux, so they are poor for storm-time density dynamics.
- ORMADD matched SPENVIS only "comparably," which suggests accuracy at the factor-level, not the percent level.

### Gaps
- The TianTuo-1 sensor details were not verified: the 476 km altitude and 0.16 W power in the brief are unsourced (the listed orbit is 468–471 km), and no TianTuo-1 AO data were found. Chinese-language papers are needed.
- Contents of the 2023 Progress in Aerospace Sciences review (accuracy and time-resolution tables) were not read.
- Osmium-film flight results were not found.

## Q3. Miniature neutral mass spectrometers (INMS, WINCS) and commercial RGA/TOF

### Takeaway
These are the only small-sat instruments that resolve O, N2, O2 and He together, but the flight record is poor. Of 9 QB50 INMS (MSSL/UCL) launched, only 1 CubeSat returned data. GSFC ExoCube INMS flew in 2015 and on Dellingr, with few published numbers. NRL/GSFC WINCS (0.75–0.85 kg, 1.3 W) flew on the ISS, STPSat-3, SENSE, CADRE and others, but published composition results were not found. Mass resolution of about 10 is enough for O, N2 and He. At 100+ units, cost and reliability (filament, high voltage, contamination) are the main risks.

### Cited Findings
- **QB50 INMS (MSSL/UCL, Kataria) [FLIGHT, 1 of 9]:** a miniaturised ram-facing analyser for low-mass ions and neutrals (O, O2, N2, NO). A 50 eV electron beam ionises neutrals, which then pass through an electrostatic analyser for mass separation. **9 INMS launched on educational CubeSats. Data came from one working CubeSat for "a one-month period"** per the ESA 2020 abstract. An MSSL CIRCE poster instead says six months and names the satellite as QB50 Phoenix (Taiwan), set to O+ mode. These sources conflict on duration. UCLSat (GB03) was deployed but apparently never worked. The two remaining flight units were assigned to CIRCE (launch planned mid-2021). An enhanced gated-TOF version adding velocity measurement flew on DISCOVERER SOAR, launched to the ISS on SpaceX CRS-22 (June 2021). — [ESA indico abstract](https://indico.esa.int/event/340/contributions/5813/); [CIRCE poster](https://register-as.oma.be/esww16/contributions/public/S12-P1/S12-P1-19-KatariaDhiren/INMS_CIRCE_Posterpublic.pdf); [Gunter's UCLSat](https://space.skyrocket.de/doc_sdat/uclsat.htm); [UCL MSSL news 2021](https://www.ucl.ac.uk/mssl/news/2021/jun/mssl-instrument-launched-international-space-station); [DISCOVERER Kataria slides](https://discoverer.space/wp-content/uploads/2019/12/Session-3_Mass-spectrometry-for-VLEO-and-DISCOVERER_Dhiren-Kataria.pdf)
- **QB50 INMS carriers:** QB50P1 (2U) hosted the MSSL INMS. Challenger (CU Boulder) also carried one. — [spaceflight101](https://spaceflight101.com/spacecraft/?p=1986); [eoPortal nSight-1/QB50 list](https://directory.eoportal.org/satellite-missions/nsight-1)
- **ExoCube INMS (NASA GSFC, with Cal Poly, U. Wisconsin, ERAU) [FLIGHT]:** intended to measure neutral and ionised H, He and O. Gated time-of-flight covering H, He, N, O, N2, O2 with **M/dM ≈ 10**, using a thermionic-emitter electron-impact source. Flight unit is **1.3U and 570 g**. Launched 31 Jan 2015, and the 2015 AGU abstract states it produced flight data. The INMS later flew on Dellingr. Spacecraft outgassing contaminates neutral H for years, so a dedicated neutral-H mode was added. — [NTRS 20160010304](https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20160010304.pdf); [AGU FM15 84629](https://agu.confex.com/agu/fm15/webprogram/Paper84629.html); [AGU FM15 84572](https://agu.confex.com/agu/fm15/webprogram/Paper84572.html); [ERAU](https://portfolio.erau.edu/en/publications/exocube-inms-with-neutral-hydrogen-mode/); [eoPortal ExoCube](https://eoportal.org/satellite-missions/exocube); [GSFC 2019 Paschalidis slides](https://science.gsfc.nasa.gov/attic/cubesats.gsfc.nasa.gov/symposiums/2019/presentations/Day1/PASCHALIDIS.pdf)
- **WINCS / SWATS (NRL + NASA GSFC) [FLIGHT, results unpublished in sources found]:** four electrostatic analysers (2 ion, 2 neutral) plus 2 mass spectrometers (WTS, IDS, NMS, IMS). Measures neutral winds, temperature, density and composition (O, N2) plus ion equivalents. **7.6 × 7.6 × 7.1 cm, about 1.3 W.** Mass is given as **0.75 kg** (NRL abstracts) but **~0.85 kg including interface electronics** (eoPortal CADRE). Target mass resolution is 1/50, requiring 900 eV final energy. Operating on the ISS (Sep 2013) and STPSat-3 (Nov 2013). Also flown on SENSE-2 (Boeing Colony-2 3U, Nov 2013), CADRE (UMich, deployed from the ISS 16 May 2016, end of life ~1 Mar 2017), GPIM and Politech.1, per a NOAA SBIR for the successor "WIND" instrument. — [AGU FM14 Nicholas et al.](https://agu.confex.com/agu/fm14/webprogram/Paper7513.html); [AMS 2012](https://ams.confex.com/ams/92Annual/webprogram/Paper199144.html); [eoPortal CADRE](https://eoportal.org/satellite-missions/cadre); [eoPortal SENSE](https://www.eoportal.org/satellite-missions/sense); [HigherGov NOAA grant](https://www.highergov.com/grant/NA24OARX021G0036/)

### Inferences
- The QB50 lesson is that failures were dominated by student buses (9 of 36 dead on arrival, about a third dead within a year), not necessarily the INMS itself. A hosted payload on a professional bus removes much of that risk. INMS still needs ram pointing, high voltage and a filament.
- WINCS is the most mature integrated wind/temperature/composition unit, but no per-unit price was found. NRL/GSFC instruments are typically government-built and not catalog items.

### Gaps
- No published QB50 INMS, ExoCube or WINCS composition profiles or accuracy numbers were reached. The relevant sources are Paschalidis 2019 slides, the AGU FM14 full text, and the CADRE papers.
- No unit costs were found for INMS, ExoCube INMS or WINCS.
- No flown commercial miniature RGA/quadrupole (e.g. Inficon/SRS-type) on a CubeSat for thermospheric composition was found. Daedalus-concept instruments are not flight items.
- The CIRCE launch and INMS outcome were not verified.

## Q4. Ram wind/temperature/composition spectrometers (SWATS/WATS, RPA, energy/angle analyzers)

### Takeaway
SWATS is the same NRL/GSFC instrument family as WINCS (see Q3). It derives neutral winds and temperature from the angle/energy distribution of ram particles, with composition from the mass-spectrometer channels.

### Cited Findings
- NRL describes the instrument as "WINCS, also known as SWATS (Small Wind and Temperature Spectrometer)," operating on the ISS and STPSat-3 from 2013. — [AGU FM14](https://agu.confex.com/agu/fm14/webprogram/Paper7513.html)
- Wind measurement specs: 30° × 2° FOV, 15 angular pixels, 20 energy steps. — [eoPortal CADRE](https://eoportal.org/satellite-missions/cadre)
- The successor "WIND" instrument was proposed to NOAA, building on WINCS heritage. — [HigherGov](https://www.highergov.com/grant/NA24OARX021G0036/)

### Gaps
- No small-sat retarding-potential-analyser neutral composition results were found. RPAs mostly measure ions.

## Q5. Remote-sensing composition from small sats (brief)

### Takeaway
No cheap flown CubeSat UV O/N2 photometer was confirmed in this search. GOLD and GUVI-class O/N2 remain large-mission products.

### Gaps
- NRL Tri-TIP (Triple Tiny Ionospheric Photometer, 135.6 nm, flown on COSMIC-2) and solar-occultation O/N2 were not researched in the available budget. From background knowledge (UNVERIFIED), Tri-TIP measures ionospheric 135.6 nm emission (O+ recombination), not neutral O/N2, so treat it as an ionospheric sensor.

## Q6. Co-manifested combinations

### Cited Findings
- **SWARM-EX:** FIPEX + Langmuir probe in the same payload section (not yet confirmed flown). — [CU Boulder](https://www.colorado.edu/aerospace/academics/graduates/graduate-projects/2022-2023-projects/space-weather-atmospheric-reconfigurable); [Gunter's](https://space.skyrocket.de/doc_sdat/swarm-ex.htm)
- **EuTEF on ISS Columbus:** FIPEX flew with the STORM carbon-film AO detector (Southampton) on MEDET, on the same platform at the same time, giving a natural cross-check. — [Southampton eprints 155253](https://eprints.soton.ac.uk/155253); [EuTEF](https://en.wikipedia.com/wiki/EuTEF)
- **QB50:** INMS, FIPEX and mNLP each flew on separate CubeSats (one science unit per spacecraft), so they were not co-manifested. — [IAC-17 abstract](https://iafastro.directory/iac/archive/browse/IAC-17/B4/2/40579/)
- **WINCS:** combines wind, temperature, ion drift and composition in one 0.75–0.85 kg box. — [eoPortal CADRE](https://eoportal.org/satellite-missions/cadre)

### Inferences
- For a 100+ unit hosted payload, the cheapest credible composition package is **FIPEX (O, O2) + a Langmuir probe (ne/Te) + optionally an accelerometer or drag-derived density**. Total density minus O gives an N2+He proxy that needs a model. Resolving N2 and He directly needs an INMS-class TOF instrument (≈0.6–0.85 kg, ≈1.3 W, with a weaker reliability record).

### Gaps
- No published joint FIPEX + Langmuir probe results exist yet. SWARM-EX status is unconfirmed.
- Unit cost is not documented for any of these instruments. All cost estimates would be inference.
