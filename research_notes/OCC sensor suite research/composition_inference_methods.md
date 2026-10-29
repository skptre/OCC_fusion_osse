# Inferring Thermospheric Composition and Density from Cheap Measurements: Methods, Accuracy, Observability Limits

Scope note: research was done on 2026-10-11 using web search. Several key full texts (Mehta et al. 2019 Space Weather; Jin et al. 2025 Remote Sensing; Bernstein et al. 2022 Space Weather; arXiv 1912.01069 and 1503.03207) returned HTTP 403 or could not be text-extracted, so many numbers below come from abstracts, index pages, or search summaries. Anything not traced to a source is placed under Inferences (physics reasoning) or Gaps. Treat numbers marked "abstract-level" as needing a check against the full paper before they go into a proposal.

---

## Q1. Published methods that infer composition or species densities from mass density, number density, drag, or partial-species sensors

### Takeaway
Composition has been inferred from cheap data in three main ways: (a) reduced-order or modal fitting of species fields to accelerometer mass density plus a composition proxy (Mehta, Linares & Sutton 2019, CHAMP/GRACE + TIMED/GUVI), (b) using two satellites at different altitudes in near-coplanar orbits to separate He from O through scale-height differences (Thayer et al. 2012; Liu et al. 2014), and (c) Kalman filters on a physical model that estimate composition from simulated observations (Minter et al. 2004; Codrescu et al. 2004). Direct gauge-vs-drag combinations exist (QQ-Satellite, SpEED Demon), but I found no published paper that inverts gauge number density together with drag mass density for mean molecular mass.

### Cited Findings
**Mehta, Linares & Sutton (2019), data-driven composition inference**
- Citation: "Data-Driven Inference of Thermosphere Composition During Solar Minimum Conditions," Space Weather 17(9), 1364-1379, doi 10.1029/2019SW002264. The motivating point is that mass density can depart from the variation expected from temperature alone because composition changes. — [GFZ GRACE reference index](https://www-app2.gfz.de/grace-references/b2hd-2019SpWea..17.1364M.html)
- Method (from the group's slide document): build MSIS snapshots over a range of solar and geomagnetic drivers, extract POD/SVD basis vectors for O, O2, N2 and He separately, then fit time-varying modal coefficients to observations. Validation was inferring the O-to-He transition while jointly assimilating TIMED/GUVI (column O/N2) and CHAMP/GRACE (accelerometer mass density). — [Mehta, WVU slide PDF (via search summary; direct fetch returned 403)](https://piyushmehta.faculty.wvu.edu/files/d/b483383a-fc7b-451e-8caf-0ad31f898da4/data-driven-inference-and-investigation-of-thermosphere-dynamics-and-variations.pdf)
- N and H were not tuned, because CHAMP/GRACE carry no signal for these minor species and H's partial pressure was taken as negligible. The first r = 3 modes per species captured more than 98% of variance. — [same WVU slide PDF](https://piyushmehta.faculty.wvu.edu/files/d/b483383a-fc7b-451e-8caf-0ad31f898da4/data-driven-inference-and-investigation-of-thermosphere-dynamics-and-variations.pdf)

**Thayer et al. (2012) and Liu et al. (2014), He from CHAMP/GRACE**
- Thayer, Liu, Lei, Pilinski & Burns (2012), "The impact of helium on thermosphere mass density response to geomagnetic activity during the recent solar minimum," JGR 117, A07315, doi 10.1029/2012JA017832. — [GFZ GRACE reference index](https://www-app2.gfz.de/grace-references/b2hd-2012JGRA..117.7315T.html)
- Used near-coplanar CHAMP and GRACE orbits for 1-10 December 2008. He number densities were extracted near 500 km and showed a winter-hemisphere He bulge. Wintertime He exceeded NRLMSISE-00 by 30-70% in quiet conditions, even after F10.7 adjustment. — [UCAR dataset record, "Altitude variations in the thermosphere mass density response..."](https://data.ucar.edu/dataset/ce95c53b-3334-46d6-a5cb-2ae0b3c4c8aa); [EGU2014-14742 abstract](https://meetingorganizer.copernicus.org/EGU2014/EGU2014-14742.pdf)
- A 2015 assimilation paper also attributes the 30-70% He excess to Liu et al. (2014) and links it to very low winter He/O transition altitudes. — [arXiv 1503.03207](https://arxiv.org/pdf/1503.03207)
- Fetched text did not confirm the exact inversion. As far as could be seen, it relies on two altitudes plus diffusive-equilibrium scale-height separation (see Gaps).

**Minter, Fuller-Rowell & Codrescu (2004); Codrescu, Fuller-Rowell & Minter (2004), Kalman filters for composition**
- Minter et al. (2004), "Estimating the state of the thermospheric composition using Kalman filtering," Space Weather 2, doi 10.1029/2003SW000006. This was an OSSE: a physical-model "truth" thermosphere was sampled through simulated instruments and orbits. The Kalman filter usually cut estimation error below 6%, even with observation errors as large as 15%. The best results came from pairing the filter with an accurate physical model. — [EarthRef / search summary](https://earthref.org/ERR/84356); [CU Vivo](https://vivo.colorado.edu/display/pubid_119861)
- Codrescu et al. (2004), "An ensemble-type Kalman filter for neutral thermospheric composition during geomagnetic storms," Space Weather 2, doi 10.1029/2004SW000088. Composition is an externally forced system, unlike weather or ocean models. A 10-member ensemble was enough to characterize state covariance and keep the filter stable. The filter followed the general trend of the forcing but departed from it at times. — [EarthRef](https://earthref.org/ERR/81578)
- A companion paper: Fuller-Rowell, Minter & Codrescu (2004), "Data assimilation for neutral thermospheric species during geomagnetic storms," Radio Science, doi 10.1029/2002RS002835. Follow-on: Codrescu, Codrescu & Fedrizzi (2018), "An Ensemble Kalman Filter for the Thermosphere-Ionosphere," Space Weather 16. — [CU Vivo, EnKF T-I](https://vivo.colorado.edu/display/pubid_235610)

**Gauge or number-density sensors combined with drag**
- QQ-Satellite: a 73.8 kg, 800 mm sphere at about 520 km in a dawn-dusk orbit (97.46°), launched 14 Oct 2021. It carries a dual-frequency GPS/BeiDou receiver for POD and an ionization-gauge "Orbital Neutral Atmospheric Detector" (OAD). — [Sun et al. 2022, Remote Sensing 14, 3873](https://doi.org/10.3390/rs14163873)
- Jin et al. (2025), Remote Sensing 17(1), 98, doi 10.3390/rs17010098, compare POD-derived and gauge-derived mass densities on that satellite for 31 Oct-7 Nov 2021. The full text returned 403, so their quantitative POD-vs-gauge difference is unverified here. — [DOI link](https://doi.org/10.3390/rs17010098)
- The "~19%" figure in the brief most likely corresponds to an "approximately 18.77% difference" reported for QQ-Satellite POD-derived density in Sun et al. (2022). The same paper reports a 1-sigma difference of 52.99% during a storm. The text available here did not say what the 18.77% is measured against (MSIS or gauge). Do not cite it as "gauge vs GPS" until checked. — [Sun et al. 2022](https://doi.org/10.3390/rs14163873); [ResearchGate](https://www.researchgate.net/publication/362593934_Analysis_of_Orbital_Atmospheric_Density_from_QQ-Satellite_Precision_Orbits_Based_on_GNSS_Observations)
- SpEED Demon sounding rocket (ERAU, 80-100 km): densities from cheap COTS accelerometers (drag) agreed with an onboard ionization gauge and MSIS within 10%. — [Graves et al., CEDAR 2023 poster](https://daytonabeach.erau.edu/-/media/files/daytona-beach/college-of-arts-and-sciences/research/sail/graves-cedar-2023.pdf); [ERAU portfolio](https://portfolio.erau.edu/en/publications/mesosphere-lower-thermosphere-neutral-density-measurements-from-l/)
- LLITED (two 1.5U CubeSats): MIGSI is a pressure gauge converted to density and neutral wind, with a range of 1e-3 to 1e-8 torr. One secondary source gives 0.1% precision and 20% accuracy. Differential drag between the two spacecraft was a planned, not demonstrated, density technique. A solar-cell anomaly cut the duty cycle and the orbit differed from plan. I found no published MIGSI-vs-drag comparison. — [LLITED presentation (NASA SPDF)](https://spdf.gsfc.nasa.gov/pub/data/aaa_smallsats_cubesats/llited/documents/LLITED-presentation-2026-00325.pdf); [eoPortal LLITED](https://www.eoportal.org/satellite-missions/llited); [NASA SmallSat lessons learned](https://www.nasa.gov/smallsat-institute/community-of-practice/lessons-learned-from-the-llited-mission/)
- Mars analog: MAVEN NGIMS (mass spectrometer; species sum to mass density) vs ACCEL (drag). The ratio is near 1 but rises with density, reaching about 30% at periapsis. The cause is unexplained. This shows that two independent "mass density" paths can disagree systematically by tens of percent. — [BAAS 2023 abstract](https://baas.aas.org/pub/2023n8i307p02)
- Composition from ionograms (indirect, ground-based): ionogram profiles calibrated against TIMED/GUVI to infer O/N2. — [Reading eprint](https://reading-clone.eprints-hosting.org/96158); [Ann. Geophys. 39, 309 (2021)](https://angeo.copernicus.org/articles/39/309/2021/)

### Inferences
- Mean molecular mass follows from the definition m̄ = ρ/n (ρ = mass density, n = total number density). A co-located density channel (drag or accelerometer) and a number-density channel (gauge) therefore give m̄ directly. Errors add in quadrature in log space: σ(m̄)/m̄ ≈ sqrt[(σρ/ρ)² + (σn/n)²]. With today's demonstrated agreements of about 10-20% per channel, m̄ comes out at about 15-30%. That is too coarse to resolve O vs N2 (m = 16 vs 28) unless one channel is much better calibrated.
- The two most mature composition-from-cheap-data methods (Mehta 2019; Thayer 2012) each needed a second, independent constraint besides one mass-density stream: GUVI O/N2, or a second altitude. That points to the third-measurement requirement discussed in Q2.

### Gaps
- Full text and quantitative accuracy of Mehta, Linares & Sutton (2019), e.g. error in the inferred He or O-He transition height vs truth. The PDF was 403.
- The exact Thayer/Liu He-extraction algorithm and its stated uncertainty.
- Jin et al. (2025) QQ-Satellite gauge vs POD numbers.
- No published LLITED MIGSI-vs-drag result found as of Oct 2026.

---

## Q2. Observability: sensitivity weights of each measurement to O, N2 and He; degeneracies; the third measurement; when He matters

### Takeaway
Each sensor class weights species differently. Drag and accelerometers weight by mass (He:O:N2 = 4:16:28). An N2-calibrated ionization gauge weights by ionization cross-section (He ≈ 0.16-0.19 relative to N2 = 1; O not well tabulated). An O-only sensor weights O alone. Because O dominates both mass and gauge signal at 300-500 km, gauge and drag respond to roughly the same linear combination, which makes them nearly degenerate. A species-selective channel is needed to break the O/N2 and O/He degeneracies: an O-specific sensor, a column-O/N2 proxy like GUVI, or a second altitude. He matters near and above the O-He transition, which is much lower in solar minimum and in winter.

### Cited Findings
- Ionization gauges are calibrated to N2. Uncorrected readings are "nitrogen-equivalent." — [MKS/Granville-Phillips 274 datasheet](https://www.mks.com/medias/sys_master/resources/he3/hc9/10080780189726/GP-160827-274Gauges-DS/GP-160827-274Gauges-DS.pdf)
- Bayard-Alpert relative sensitivities (N2 = 1): He 0.16, H2 0.42, Ne 0.30, O2 about 0.90 (composite table). — [Physics Today table PDF](https://aip.brightspotcdn.com/PTO.v25.i8.40_1.online.pdf)
- Another measurement gives He 0.19 and H2 0.45 relative to N2. — [EPFL ICPP 1998 paper](https://lac913.epfl.ch/epsppd3/1998/WEB/98ICPP_W/F061PR.PDF)
- Nominally identical gauges can vary by up to 20% in absolute sensitivity. — [Physics Today table PDF](https://aip.brightspotcdn.com/PTO.v25.i8.40_1.online.pdf)
- No tabulated laboratory relative sensitivity for atomic O was found. — (searches above)
- CHAMP/GRACE (accelerometers) carry no information on minor species such as N or H, so these were left untuned in modal inference. — [Mehta WVU slide PDF](https://piyushmehta.faculty.wvu.edu/files/d/b483383a-fc7b-451e-8caf-0ad31f898da4/data-driven-inference-and-investigation-of-thermosphere-dynamics-and-variations.pdf)
- He/O transition effects in the 2008 solar minimum: the storm-time mass-density perturbation was 60% at CHAMP altitudes but only 25% at GRACE altitudes in the winter hemisphere. The largest storm-time perturbation occurred near the He/O transition, with a weaker maximum near the O/N2 transition. The altitude of maximum perturbation is where the change in weighted pressure scale height equals and opposes the change in mean-molecular-weight scale height. — [UCAR dataset record](https://data.ucar.edu/dataset/ce95c53b-3334-46d6-a5cb-2ae0b3c4c8aa); [EGU2014-14742](https://meetingorganizer.copernicus.org/EGU2014/EGU2014-14742.pdf)
- Winter He bulge densities extracted near 500 km. 1960s Explorer drag data (390-880 km) attributed the winter bulge to a high-latitude winter He bulge, with He and O as primary constituents at about 550-750 km. — [EGU2014-14742](https://meetingorganizer.copernicus.org/EGU2014/EGU2014-14742.pdf); [NASA NTRS 1969 report](https://ntrs.nasa.gov/api/citations/19690016177/downloads/19690016177.pdf)
- Winter He/O transition altitudes were "extremely low" in 2008, explaining the 30-70% model He deficit. — [arXiv 1503.03207](https://arxiv.org/pdf/1503.03207)
- GSI knowledge is weakest above the O/He transition, where most LEO satellites operate. — [BAAS 2023 abstract](https://baas.aas.org/pub/2023n3i323/download/pdf)

### Inferences
These are physics reasoning, not sourced results. Verify them in the team's OSSE.
- Linearized measurement rows. Let n_i be the species number densities.
  - Drag or accelerometer mass density: ρ = Σ m_i n_i, so ∂ρ/∂n_i ∝ (4, 16, 28, 32) amu for (He, O, N2, O2), scaled further by C_D, which itself depends on composition (Q3).
  - Gauge (N2-equivalent number density): n_g = Σ S_i n_i, with S ≈ (0.16-0.19, S_O, 1, 0.9). S_O is unmeasured. If O scales like half of O2, S_O ≈ 0.4-0.5. In practice a ram-facing gauge also sees AO recombine to O2 on surfaces, which changes the effective weight. This is a key calibration unknown.
  - O-only sensors (e.g., AO actinometer or resonance fluorescence): ∂/∂n_i = (0, 1, 0, 0).
- Gauge + drag near-degeneracy. At 400-500 km in moderate activity, O makes up roughly 80-95% of n. Both rows are then dominated by the O column of the Jacobian, so the angle between the two row vectors is small. In the 2D subspace (O, N2) the normalized rows are (16, 28)/|·| and (S_O, 1)/|·|. With S_O ≈ 0.5 the angle is only about 3-4°, because 16/28 ≈ 0.57 is close to S_O/1 ≈ 0.5. Whether they are degenerate therefore hinges on the unmeasured S_O. In (O, He) the rows are (16, 4) and (S_O, 0.17), which gives more contrast. Gauge + drag thus constrain He/O better than N2/O. This is my estimate. The team should compute the condition number with MSIS profiles.
- Breaking O/N2. Add a channel with a very different O:N2 ratio. Options: an O-specific sensor (row (0, 1, 0)), a column O/N2 remote proxy (GUVI-like; the Mehta 2019 approach), or a second altitude, since O and N2 have different scale heights (H_N2 ≈ 0.57·H_O).
- Breaking He/O. Use a second altitude (the Thayer approach: H_He ≈ 4·H_O), or rely on the gauge's low He sensitivity relative to its mass weight. An O-only sensor combined with drag also isolates He + N2 by subtraction.
- Under diffusive equilibrium, species profiles depend on exospheric temperature, so a temperature-capable channel adds a strong constraint. That could be orbit-to-orbit density scale height from altitude variation over an eccentric orbit, or a gauge in ram plus a wake gauge.
- He matters mostly for altitudes at or above about 450-500 km near solar minimum, especially winter high latitudes. The cited 2008 results place He-significant behaviour near 500 km. Specific transition heights by F10.7 were not found in a citable source (see Gaps).

### Gaps
- No primary source found for the O-He transition altitude as a function of F10.7 (the commonly quoted "~450 km at solar minimum, ~700+ km at solar maximum" was not confirmed). Compute it from NRLMSIS 2.0 directly in the OSSE.
- No lab or flight-calibrated ionization-gauge relative sensitivity for atomic O was found. Also missing: how ram-gauge surface recombination (O → O2) changes it.
- No published Fisher-information or condition-number analysis of gauge + drag + O-sensor was found. This looks like an open niche the OSSE could fill.

---

## Q3. Drag coefficient (C_D) and gas-surface interaction (GSI): composition and AO adsorption dependence, uncertainty, and how composition reduces C_D error

### Takeaway
C_D is the dominant error in drag-derived density. Diffuse-reflection assumptions can bias density by about 25% near the O-He transition, where low AO coverage of surfaces and light He change the accommodation. Composition enters C_D twice: through the mean molecular mass in the speed ratio, and through AO adsorption, which sets the accommodation. An in-situ O channel therefore directly reduces C_D error for the density channel.

### Cited Findings
- Moe & Bowman (AAS 05-258, 2005): adsorbed AO on satellite surfaces masks material differences near 200 km. At higher altitudes, where adsorbed AO decreases, material characteristics "slowly emerge." C_D was interpreted with a combination of Sentman and Schamberg models and flight-measured GSI parameters. — [AAS 05-258 PDF (spacewx.com)](https://spacewx.com/wp-content/uploads/2024/02/AAS_2005_258_Surface_Effects_on_CD_of_Spheres.pdf)
- Pilinski (CU dissertation, 2011): energy accommodation can be predicted with Langmuir-adsorption GSI models. Accommodation is explained by AO binding to the surface at about 5.7 eV. Diffuse reflection suits CHAMP near 400 km. Pre-2008 accommodation was 0.86-0.89. — [CU Scholar dissertation](https://scholar.colorado.edu/asen_gradetds/37/)
- Historical paddlewheel-satellite measurements: nearly diffuse re-emission, accommodation 0.65-0.9. — [DTIC AD0673946](https://apps.dtic.mil/sti/pdfs/AD0673946.pdf)
- Bernstein, Pilinski & Knipp (2020), "Evidence for Drag Coefficient Modeling Errors near and Above the Oxygen-to-Helium Transition," J. Spacecraft & Rockets 57(6), 1246-1263. — [CU experts record](https://experts.colorado.edu/display/pubid_301345)
- Follow-up (Space Weather 2022, "Drag Coefficient Constraints for Space Weather Observations in the Upper Thermosphere"): C_D errors are altitude- and solar-cycle-dependent, larger near 500 km at the O-He transition. Inter-satellite comparisons favour incomplete accommodation over diffuse. Diffuse modelling could produce density errors of about 25% near solar maximum. — [ESSOAr preprint 10.1002/essoar.10508667.1](https://essopenarchive.org/doi/full/10.1002/essoar.10508667.1)
- Mehta et al. (2022) review of drag-coefficient modelling for accelerometer densities (CEAS Space Journal): scale differences between thermospheric data sets mostly come from aerodynamic modelling, namely surface geometry and GSI. The review calls for robust UQ and for GSI models that include altitude and solar-cycle dependence. — [Springer, CEAS Space J., doi 10.1007/s12567-022-00434-3](https://link.springer.com/article/10.1007/s12567-022-00434-3)
- C_D is most sensitive to GSI (Mehta et al. 2014b; March et al. 2021), and GSI physics is still an open question. — [search summary of the review literature](https://link.springer.com/article/10.1007/s12567-022-00434-3)
- In VLEO material experiments, C_D-determination uncertainty grows as accommodation falls, because aerodynamic attitude perturbations increase. This is worse near 200 km. — [TU Delft repository](https://repository.tudelft.nl/file/File_07e6d2b4-e1c6-4d87-ad2c-3ccf52978e31)
- Generalized energy-accommodation treatment (arXiv 2411.11597). — [ar5iv](https://ar5iv.labs.arxiv.org/html/2411.11597)

### Inferences
- Composition-to-C_D coupling:
  - The molecular speed ratio s = V/sqrt(2kT/m̄) shrinks as m̄ falls when He rises, which raises C_D for flat plates and spheres.
  - The Langmuir AO surface coverage θ = K·P_O/(1 + K·P_O) depends on the O partial pressure, which sets the accommodation coefficient α. An O-partial-pressure channel therefore gives θ, then α, then C_D, reducing the single largest systematic error in the density channel. That realizes the "composition channels that also improve density" concept.
- Practical C_D uncertainty to plan for: about 5-10% below 400 km where diffuse is valid, rising to 15-25% near 500 km and the O-He transition (from the 25% figure above). This is a planning estimate, not a single published number.
- A sphere (QQ-Satellite style) minimizes attitude-dependent C_D error. That is a design option for the density channel.

### Gaps
- The 0.98 accommodation value often quoted for low altitude was not confirmed in the sources found.
- No paper was found that quantifies the C_D error reduction from flying an in-situ O sensor. This is a candidate OSSE result.

---

## Q4. How in-situ measurements improve density beyond the sensor itself: data assimilation, reduced-order models, fleet calibration, ML models

### Takeaway
Assimilating sparse density observations into a model reduces global density error to roughly 5-10%. Examples: HASDM's design goal of under 5%; WAM-IDEA with Starlink at 6.6% RMS (6.4% independently vs GRACE-FO); HASDM-ML at under 10% MAE. Reduced-order Kalman filters (Gondelach & Linares) estimate global density from TLEs and outperform NRLMSISE-00 and JB2008 in orbit determination. Composition-specific DA was demonstrated only in OSSEs (Minter 2004: under 6% from 15% observations).

### Cited Findings
- HASDM: data-assimilative, based on JB2008, using calibration-satellite tracking. Design goal of under 5% density uncertainty at most epochs (older description). It is the operational US Space Force model for catalogue maintenance and conjunction assessment. — [ESA SDC8 paper 25](https://conference.sdo.esoc.esa.int/proceedings/sdc8/paper/25/SDC8-paper25.pdf)
- HASDM-ML (Licata & Mehta): Monte-Carlo-dropout UQ with NLPD loss, mean absolute error under 10% with well-calibrated uncertainties. The largest calibration discrepancy at GRACE altitudes is just over 1%. HASDM storm densities are mostly within the bounds. — [arXiv 2109.07651](https://arxiv.org/pdf/2109.07651)
- MSIS-UQ (calibrated NRLMSIS 2.0): reported reductions vs NRLMSIS 2.0. A search summary mentions about 11% MAE reduction and errors under 1.5% in some comparison, but attribution within the paper is unclear. — [arXiv 2208.11619](https://arxiv.org/pdf/2208.11619)
- Gondelach & Linares (2020, Space Weather, doi 10.1029/2019SW002356): reduced-order model with an unscented Kalman filter that jointly estimates density modes plus orbits and ballistic coefficients of about 15 objects from TLEs. Validated vs CHAMP/GRACE. — [MIT DSpace](https://dspace.mit.edu/handle/1721.1/135442); [GFZ index](https://www-app2.gfz-potsdam.de/grace-references/b2hd-2020SpWea..1802356G.html)
- Swarm A orbit determination (January 2020) with ROM TLE-estimated densities was more precise than NRLMSISE-00 or JB2008, especially along-track. — [arXiv 2207.08993 (ML orbit estimation survey)](https://arxiv.org/pdf/2207.08993)
- Reduced-order density UQ for conjunction assessment reports orbit-averaged density error statistics vs CHAMP/GRACE for NRLMSISE-00, JB2008 and ROM (Table 3). The numbers could not be extracted. — [arXiv 1912.01069](https://arxiv.org/pdf/1912.01069)
- Starlink + WAM via IDEA (Cheng & Sutton, 2026 Space Weather Workshop poster): Jan-Apr 2023 including a G4 storm on 23 April. RMS 6.6% vs Starlink orbit-effective density, 6.4% vs independent GRACE-FO accelerometer density. WAM had a positive bias before assimilation. This is a poster, not peer-reviewed, and the pre-assimilation baseline was not given. — [CPAESS SWW 2026 abstract](https://cpaess.ucar.edu/abstract-2026-sww/multi-month-thermospheric-neutral-density-nowcast-and-forecast-using-multiple-low)
- IDEA precursor: CHAMP + GUVI assimilation into WAM captured density through the Nov 2003 storm. — [NSF PAR 10370357](https://par.nsf.gov/biblio/10370357)
- Reduced-order thermospheric DA bridging to operations (Narayanan, WVU, SWW 2026): ROM + Kalman filter evaluated with CHAMP, GRACE/-FO, GOCE, Swarm, HASDM and TLE data. Significant improvement over open loop, especially during storms. No numbers were given in the excerpt. — [CPAESS SWW 2026 abstract](https://cpaess.ucar.edu/abstract-2026-sww/bridging-high-fidelity-modeling-and-operations-reduced-order-thermospheric-data)
- Mehta et al. transformative DA/calibration framework for physical I-T models. — [arXiv 1804.04088](https://arxiv.org/pdf/1804.04088)
- Ensemble Kalman filter mass-density specification. — [UCAR impacts record](https://impacts.ucar.edu/en/publications/thermospheric-mass-density-specification-using-an-ensemble-kalman/)
- Karman/ESA: no specific error numbers retrieved for the "Karman" ML density framework.

### Inferences
- For a fleet of cheap gauges, the DA filter can carry per-sensor gain and offset as augmented states, a self-calibration approach analogous to low-cost air-quality sensor networks. These states become observable when sensors cross each other or pass near a reference density source (POD/accelerometer satellite, HASDM, Starlink-derived densities). No space-specific publication on this was found. It is a design inference.
- A good DA system already reaches about 5-7% density error. A new density channel must therefore beat that, or add something DA lacks, to matter. The most defensible added value is composition (He/O, O/N2) and C_D or m̄ correction, not raw density.

### Gaps
- An authoritative peer-reviewed number for current operational HASDM error (the "2-10%" range was not confirmed).
- Peer-reviewed publication of the Starlink/WAM 6.6% result.
- Karman / HASDM-ML per-altitude error tables.
- Published fleet cross-calibration of space-borne cheap neutral sensors.

---

## Q5. Achievable composition accuracy from fusion (OSSEs and real data) and failure modes

### Takeaway
The only quantitative composition-estimation accuracy found is the Minter et al. (2004) OSSE: under 6% estimation error from 15%-error observations with a Kalman filter and an accurate physical model. Real-data He inferences show the models themselves can be wrong by 30-70% in winter at solar minimum. Storms drive upwelling of N2 and O depletion (O/N2 depletion, with strong hemispheric asymmetry), which is the main failure mode for estimators with climatological composition priors.

### Cited Findings
- OSSE accuracy: Kalman filter composition estimation error usually under 6% even with 15% observation errors. — [Minter et al. 2004, EarthRef](https://earthref.org/ERR/84356)
- A 10-member ensemble suffices for a stable composition EnKF during storms, but the estimate departs from the forcing trend at times. — [Codrescu et al. 2004, EarthRef](https://earthref.org/ERR/81578)
- Real-data model error for He: 30-70% NRLMSISE-00 underestimate in winter at solar minimum. — [EGU2014-14742](https://meetingorganizer.copernicus.org/EGU2014/EGU2014-14742.pdf)
- Storm composition mechanism: horizontal and vertical advection dominate storm perturbations in the middle thermosphere (about 160 km), partly offset by molecular diffusion (Nov 2003 superstorm). O/N2 decreases came mostly from O depletion in the low-middle thermosphere. Increases came mainly from N2 depletion. Hemispheric asymmetry was strong, especially during recovery. — [GUVI bibliography: "Response of Middle Thermosphere (~160 km) Composition to the November 20-21, 2003 Superstorm"](https://guvitimed.jhuapl.edu/bibcite/reference/10239)
- Each storm of 1-4 Oct 2002 caused significant O/N2 depletion reaching 10°N and -5°S, an asymmetry attributed to season and to heating- and convection-driven winds. — [GUVI bibliography, IMAGE SI-13 and GUVI O/N2](https://guvitimed.jhuapl.edu/bibcite/reference/8156)
- GUVI shows that O/N2 can be depleted or enhanced depending on latitude, and that N, N2 and NO increase in the depleted regions. Storm-time O2 enhancement (120-170 km) also matters. — [Geophys. Res. Lett. Oct 2023 (DOAJ)](https://doaj.org/article/af48a1837e1d4331a4c0c1991df40c32)
- The GUVI O/N2 data product definition (column O/N2 referenced to a fixed N2 column depth). — [GUVI L3 O/N2 documentation, 2004JA010441](https://cdaweb.gsfc.nasa.gov/pub/data/timed/documentation/guvi/documentation_v10/science/documents/L3_ON2_2004JA010441.pdf)
- Storm-time density is hard even for POD: the QQ-Satellite POD density 1-sigma difference was about 53% during a storm. — [Sun et al. 2022](https://doi.org/10.3390/rs14163873)
- November 2025 storm example of hemispherically asymmetric ionospheric response tied to composition. — [arXiv 2603.14454](https://arxiv.org/pdf/2603.14454)

### Inferences
- Failure modes for a gauge + drag + O-channel estimator:
  1. Storm upwelling raises N2 at fixed altitude. Drag sees m̄ rise while the gauge sees a large N2-weighted increase. A filter with an MSIS-like prior on O/N2 and too-small process noise will misattribute the change to temperature.
  2. The O-He transition moves seasonally and with solar activity. With low He sensitivity (gauge He weight about 0.17), He errors leak into C_D through m̄ and the speed ratio, and into density.
  3. Ram-gauge AO surface recombination and outgassing bias the gauge.
  4. Attitude-dependent C_D.
  Process noise on the composition modes should be inflated with Kp/Ap or Joule-heating proxies (adaptive Q).
- The "~50% O/N2 drop" in the brief is plausible for major storms but was not confirmed numerically in the sources retrieved (see Gaps).

### Gaps
- A cited numerical O/N2 storm drop (e.g., 50%). The GUVI papers above give a mechanism and spatial extent, but the excerpts carried no percentages.
- No real-data (non-OSSE) published composition-estimation accuracy from fused cheap sensors was found.
- Quantitative accuracy of Mehta et al. (2019) inferred composition vs independent truth (inaccessible here).
