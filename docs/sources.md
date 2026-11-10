# Sources register

Every source the OSSE or the proposal relies on: what it is, the exact values it gives us, and where we use them (names match `osse/params.py`).

**Status column:** **verified** means the value was checked against the primary document (who checked, and when). **To verify** means it's cited but not yet checked.

Add a row whenever a new source is used. Never put a number in `params.py` whose source isn't here.

---

## Challenge

| Source | Values it gives us | Used for | Status |
|---|---|---|---|
| NASA TechLeap OCC, Technical guidelines. https://occ.nasatechleap.org/technical-guidelines/ | In-situ mass density: accuracy "20% or better", precision "10% or better", resolution "30 seconds or faster". Pressure: 20% / 5% / 30 s. Drag acceleration: 5% / 1% / 10 s. Benchmarks are "target floors, not fixed requirements." No distinction between sampling rate and reporting resolution. Composition = "individual number density of major neutral species", "valued but not required." | `DT`; all scoring targets; relevance claims | verified (page fetched Nov 6, 2026) |
| OCC sample submission form. https://occ.nasatechleap.org/wp-content/uploads/2026/08/TechLeap-OCC-sample-form.pdf | Technology performance prompt (350 words): accuracy, precision, resolution, calibration/validation, quantitative figures of merit with uncertainty | Proposal structure | verified (earlier research notes) |

## Physical constants

| Source | Values it gives us | Used for | Status |
|---|---|---|---|
| CODATA 2018, NIST table https://physics.nist.gov/cuu/Constants/ArchiveASCII/allascii_2018.txt ; paper: Tiesinga, Mohr, Newell, Taylor (2021), Rev. Mod. Phys. 93, 025010, doi:10.1103/RevModPhys.93.025010 | Atomic mass constant 1.66053906660(50)e-27 kg. (CODATA 2022: 1.66053906892e-27, +1.4e-9 relative, negligible.) | `AMU` | value verified against NIST table (agent, Nov 6); paper details from memory, glance once |
| NGA (2014), "DoD World Geodetic System 1984", NGA.STND.0036_1.0.0_WGS84, v1.0.0. Archived: https://web.archive.org/web/20160308080435/http://earth-info.nga.mil/GandG/publications/NGA_STND_0036_1_0_0_WGS84/NGA.STND.0036_1.0.0_WGS84.pdf | Table 3.1: GM = 3.986004418e14 m³/s², including the atmosphere's mass. Table 3.4: Earth's angular velocity in a precessing frame ω* = 7.2921158553e-5 rad/s (2π/ω* = 86164.09053 s). The defining nominal ω = 7.292115e-5. | `MU`, `WE` | verified (agent, Nov 6) |
| Moritz, H. (2000), "Geodetic Reference System 1980", J. Geodesy 74(1):128–133, doi:10.1007/s001900050278 | GRS80 mean radius R1 = (2a+b)/3 = 6371008.7714 m (rounds to 6371008.8) | `RE` | verified (agent, Nov 6) |
| Wieser, M. E. (2006), "Atomic weights of the elements 2005 (IUPAC Technical Report)", Pure Appl. Chem. 78(11):2051–2066, doi:10.1351/pac200678112051 | Table 2: H 1.00794, He 4.002602, N 14.0067, O 15.9994, Ar 39.948 (g/mol) | `MASS` | verified (agent, Nov 6) |
| CIAAW, Standard Atomic Weights 2024. https://www.ciaaw.org/atomic-weights.htm | Current intervals; our 2005 values all fall inside (differences ≤0.006%) | Defending `MASS` | verified (agent, Nov 6) |

## Atmosphere model

| Source | Values it gives us | Used for | Status |
|---|---|---|---|
| Emmert et al. (2022), "NRLMSIS 2.1: An Empirical Model of Nitric Oxide Incorporated Into MSIS", J. Geophys. Res. Space Physics 127(10), e2022JA030896, doi:10.1029/2022JA030896. Code: https://map.nrl.navy.mil/map/pub/nrl/NRLMSIS/NRLMSIS2.1/ ; pymsis https://github.com/SWxTREC/pymsis | Output order: total mass density, N2, O2, O, He, H, Ar, N, anomalous O, NO, temperature. Internal masses (msis_constants.F90): He 4.0, H 1.0, others match ours. Total density includes anomalous O and excludes NO. | `SPECIES`, `MSIS_VERSION`; truth and prior atmosphere | order verified from the official Fortran and pymsis (agent, Nov 6); paper full text not opened |
| Emmert et al. (2021), NRLMSIS 2.0, Earth and Space Science 8(3), e2020EA001321, doi:10.1029/2020EA001321 | The 2.0 base model (2.1 adds NO) | Background citation | to verify |

## Space weather

| Source | Values it gives us | Used for | Status |
|---|---|---|---|
| NOAA SWPC, "G5 Conditions Observed", May 10, 2024. https://www.spaceweather.gov/news/g5-conditions-observed | G5 first observed 6:54 pm EDT May 10, 2024 (= 22:54 UTC, our conversion). First G5 since Oct 2003. | `T0`, storm choice | verified (page fetched Nov 6) |
| NOAA Space Weather Scales. https://www.spaceweather.gov/noaa-scales-explanation | G1 = Kp 5, G2 = 6, G3 = 7, G4 = 8 (incl. 9-), G5 = 9 | Future `STORM_HOURS` definition (storm = Kp ≥ 5) | verified (page fetched Nov 6) |
| GFZ Potsdam definitive Kp/ap/Ap. File https://kp.gfz.de/app/files/Kp_ap_Ap_SN_F107_since_1932.txt (format: https://kp.gfz.de/app/files/Kp_ap_Ap_SN_F107_format.txt); JSON API https://kp.gfz.de/app/json/. Cite: Matzka et al. (2021) Space Weather, doi:10.1029/2020SW002641 and dataset doi:10.5880/Kp.0001. License CC BY 4.0. | May 8–13, 2024 all definitive (flag D=2). Daily Ap: 5, 5, 105, 271, 53, 27. Kp ≥ 5 (G1+) continuously 10 May 15:00 to 12 May 06:00 UTC (39 h), again 12 May 21:00 to 13 May 06:00. Kp 9o on 11 May 00–03 and 09–12 UTC. 3-hourly table in the agent report (Nov 7). | Truth ap; `STORM_HOURS` (= 39–78 h after T0) | verified (agent downloaded the file, Nov 7) |
| Kp → ap conversion table (Bartels; as used by GFZ, Matzka et al. 2021) | 0o→0, 0+→2, 1-→3, 1o→4, 1+→5, 2-→6, 2o→7, 2+→9, 3-→12, 3o→15, 3+→18, 4-→22, 4o→27, 4+→32, 5-→39, 5o→48, 5+→56, 6-→67, 6o→80, 6+→94, 7-→111, 7o→132, 7+→154, 8-→179, 8o→207, 8+→236, 9-→300, 9o→400 | Converting forecast Kp to ap for the baseline | 20 of 28 pairs checked against the GFZ May 2024 Kp/ap columns (Nov 7); cite the paper's table |
| CelesTrak space weather file SW-All.csv. https://celestrak.org/SpaceData/SW-All.csv | The file pymsis reads (daily AP1..AP8, AP_AVG, F10.7_OBS, F10.7_OBS_CENTER81). May 2024 Kp/ap match GFZ exactly. | Truth drivers via pymsis; pin a saved copy with `PYMSIS_SPACE_WEATHER_FILE` | values cross-checked against GFZ (agent, Nov 7); CelesTrak's own docs not read |
| NRCan DRAO Penticton F10.7. https://www.spaceweather.gc.ca/solar_flux_data/daily_flux_values/fluxtable.txt ; explanation https://www.spaceweather.gc.ca/forecast-prevision/solar-solaire/solarflux/sx-3-en.php . Cite: Tapping (2013) Space Weather 11:394, doi:10.1002/swe.20064 | Daily 20 UT observed F10.7: May 7–13 = 203.6, 227.1, 233.2, 223.4, 213.7, 221.8, 215.4. 81-day centered (observed) on May 10 = 176.2. Observed is "the quantity to use when terrestrial phenomena are being studied." | Truth F10.7 | verified (agent; 81-day mean recomputed from the GFZ file, Nov 7) |
| NRLMSIS 2.1 Fortran source (msis_calc.F90, msis_gtd8d.F90, msis_constants.F90, msis_init.F90). https://map.nrl.navy.mil/map/pub/nrl/NRLMSIS/NRLMSIS2.1/nrlmsis2.1.tar.gz | Inputs: "Daily F10.7 for previous day"; "81 day average, centered on input time"; F10.7 "at the Sun-Earth distance, not the radio flux at 1 AU" (so observed, not adjusted). | `F107_KIND`; how the truth drivers are fed | verified (agent read the source, Nov 7) |
| pymsis source (pymsis/msis.py, pymsis/utils.py). https://github.com/SWxTREC/pymsis | Downloads SW-All.csv when inputs are missing; uses F10.7_OBS (previous day) and F10.7_OBS_CENTER81; builds the 7-element ap array; default `geomagnetic_activity = 1` (daily Ap), so storm-time mode needs `-1`. | `GEOMAG_MODE`; truth pipeline | verified (agent read the source, Nov 7) |
| NOAA SWPC 3-day forecast (issued 0030 and 1230 UTC), NCEI archive: https://www.ngdc.noaa.gov/stp/space-weather/swpc-products/daily_reports/3day_forecast/2024/05/ (files `YYYYMMDDhhmmthree_day_forecast.txt`). Index: https://www.ncei.noaa.gov/node/2571 | Kp forecasts by 3-hour block. Issued 9 May 0030: max Kp 5.33 on May 10. Issued 10 May 0030: max 8.33 (G4) on May 11 06–09 UTC. Observed peak was 9o. | Operator baseline Kp | verified (agent downloaded; URL checked Nov 7) |
| NOAA SWPC 3-day geomagnetic forecast, NCEI: `.../daily_reports/geomag_forecast/2024/05/YYYYMMDDgeomag_forecast.txt` | Issued 9 May 2210 UTC: predicted Ap 25 / 90 / 30 for May 10–12 (observed 105 / 271 / 53) | Baseline Ap; how badly the storm was under-forecast | verified (agent; URL checked Nov 7) |
| NOAA SWPC RSGA (issued 2200 UTC), NCEI: `.../daily_reports/reports_solar_geophysical_activity/2024/05/YYYYMMDDRSGA.txt` | Predicted F10.7 and Ap for the next 3 days; e.g. issued 9 May: F10.7 230/225/220, Ap 025/090/030 for May 10–12. "90 Day Mean" F10.7 = 164–165. | Baseline F10.7; baseline f107a assumption | verified (agent; URL checked Nov 7) |
| NOAA SWPC Weekly PRF 2540 (27-day outlook issued 6 May 2024). https://www.ngdc.noaa.gov/stp/space-weather/swpc-products/weekly_reports/PRFs_of_SGD/2024/05/prf2540.pdf | Predicted a quiet May 10–11 (Ap 5, max Kp 2) | Context: long-range forecasts missed the storm entirely | verified (agent downloaded, Nov 7) |
| USAF 45-day forecast, Wayback captures only (NCEI archives this product only from 03/2026). https://web.archive.org/web/20240510182954id_/https://services.swpc.noaa.gov/text/45-day-ap-forecast.txt | Issued 10 May 1032 UTC: Ap 25/90/30/20 and F10.7 240/225/220/220 for May 10–13. No pre-storm capture found. | Optional cross-check | verified capture (agent, Nov 7) |
| Parker, W. E. & Linares, R. (2024), "Satellite Drag Analysis During the May 2024 Gannon Geomagnetic Storm", J. Spacecraft and Rockets 61(5):1412–1416, doi:10.2514/1.A36164 (arXiv:2406.08617) | Used SWPC 3-day ap forecasts at 0–1, 1–2, 2–3 day leads; storm magnitude and duration "poorly predicted, even one day in advance". Density model NRLMSISE-00. | Precedent for the forecast baseline and lead-time choice | found by agent (Nov 7); read the paper before citing |
| Evans et al. (2024), GOLD thermospheric response to the May 2024 storm, GRL, doi:10.1029/2024GL110506 | Observed composition response (O/N₂) during the storm | Context; possible composition comparison | to verify |

## Instruments

| Source | Values it gives us | Used for | Status |
|---|---|---|---|
| INFICON MAG084 datasheet (tiba71e1-a) | Range 1e-8 to 5e-3 mbar; accuracy 30% (N₂, typical); repeatability 5%; operating +5 to +80 °C; "indoors only"; NdFeB magnet; ≤3.3 kV; ≤600 µA; controller VGC094. No gas factors. | CCG gain prior, range/floor, altitude ceiling | verified (read Oct 2026). Unknown: whether 30% / 5% are 1σ or bounds |
| MKS Instruments, "Gas Correction Factors for Ionization Vacuum Gauges". https://www.mks.com/n/gas-correction-factors-for-ionization-vacuum-gauges | Stated to apply "for both hot cathode and cold cathode ionization vacuum gauges"; corrected pressure = reading ÷ factor (so factor = sensitivity relative to N₂). N₂ 1.00, O₂ 1.01, He 0.18, H₂ 0.46, Ar 1.29, Ne 0.30, CO 1.05, CO₂ 1.42, NO 1.30. **No atomic O, N or H.** No accuracy or original source stated. | `R_TRUE` / `R_FILT` for O₂, He, Ar (baseline until INFICON gives MAG084 values) | verified (page read in browser, Nov 8) |
| MSIS gauge-signal budget (our calculation, NRLMSIS 2.1, Jan 15 2024 12 UT, lon 0, F10.7 70/200, Ap 4/15, MKS factors, S_O = 0.55) | Share of the gauge signal: O 55–90%, N₂ 2–42%, O₂ ≤2% (quiet), He ≤2% below 400 km but up to 12% at 400 km and 26% at 450 km (solar-min winter, 60°), atomic N 1–3%, atomic H ≤1% below 450 km (up to 6% at 500 km). He number fraction: ≤6% at 300 km, up to 30% at 400 km and 51% at 450 km (solar min, 60°). | Which gas factors matter; the helium argument | computed Nov 8 (scratch script; rerun in the OSSE for the record) |
| INFICON call (pending) | Gas factors, 30% breakdown, drift, temperature coefficient, linearity, pumping speed, noise/rate, ignition | `vendor` entries | pending |
| Eberhart et al. (2015), "Measurement of atomic oxygen in the middle atmosphere using solid electrolyte sensors and catalytic probes", Atmos. Meas. Tech. 8:3701–3714. https://amt.copernicus.org/articles/8/3701/2015/ | FIPEX amperometric principle; ~500 °C operation; calibration by microwave O₂ plasma + mass spectrometer | FIPEX model background | verified (earlier research) |
| Eberhart et al. (2019), "Atomic oxygen number densities in the MLT region measured by solid electrolyte sensors on WADIS-2", Atmos. Meas. Tech. 12:2445–2461, doi:10.5194/amt-12-2445-2019. PDF: https://elib.dlr.de/127198/1/Eberhart-amt-12-2445-2019.pdf | Calibration via molecular-beam mass spectrometry; FIPEX measures flux, not density; aerodynamic correction by simulation; electrode orientation matters; unit-to-unit disagreement. Appendix A Table A1 = calibration uncertainty | FIPEX fallback numbers | abstract and reviews verified; Table A1 not yet pulled |
| Stuttgart IRS call (Löhle/Fasoulas group), Nov 9 2026; recorded by the user; spec sheet to follow | Absolute accuracy **~30%**, "depends on the calibration instruments". **No drift number**: never flown on this kind of mission. **~80k USD per sensor**; gold (O) and platinum (O+O₂) are separate sensors. Pt − Au for O₂ is **"near impossible"** because of platinum nonlinearity. Output is electrical current, **2 bytes per sample** minimum; converted to particle flux, then number density. Closest flown precedent named: **SWARM-EX (CU Boulder)**. Many TechLeap teams have already contacted them. | `O_GAIN_SD` (0.30), FIPEX drift (stays a sweep), cost, O₂ approach (gold only), data rate | user's meeting notes; confirm against the recording and spec sheet |

## Phase A inputs (research agent, Nov 8; "[OA]" = abstract via OpenAlex index, wording may differ slightly; "unconfirmed" = not seen in a primary text)

| Source | Values it gives us | Used for | Status |
|---|---|---|---|
| Bruinsma & Forbes (2008), "Medium- to large-scale density variability as observed by CHAMP", Space Weather 6, S08002, doi:10.1029/2008SW000411 | High-pass density variability at 370–450 km: ~9% (low activity), ~13% (high). Filter cutoff not given in the abstract. | `TRUTH_COMMON_SD` | abstract [OA]; read full text for the cutoff scale |
| Bruinsma et al. (2006), CHAMP/GRACE response to the 20–21 Nov 2003 storm, JGR 111, A06303, doi:10.1029/2005JA011284 | Storm anomalies ~1000–2000 km; "substantial variability… at smaller scales (~300–500 km)"; GRACE amplitude variations 10–20% | Truth structure scales (storm) | abstract [OA] |
| Bruinsma & Forbes (2009), TADs from CHAMP, Adv Space Res 43:369, doi:10.1016/j.asr.2008.10.031 | TADs >1000 km, speed 646 ± 122 m/s; amplitude not found | Context | snippet only; amplitude unconfirmed |
| García et al. (2016), GOCE gravity waves, JGR Space Phys 121:8089, doi:10.1002/2016JA022797 | ~250–270 km: dominant wavelengths 200–500 km at high solar flux; max ~1000 km | Truth structure scales (VLEO) | abstract [OA] |
| Bruinsma & Laurens (2024), "Thermosphere model assessment for geomagnetic storms from 2001 to 2023", JSWSC 14:28, doi:10.1051/swsc/2024027 | Accelerometer products resolve ~600 km (Swarm ~1000 km). **Storm model error** (std of ln obs/model, 152 storms, debiased): NRLMSISE-00 14.5% (GOCE ~250 km), 21.6% (CHAMP ~300–450 km), 27.0% (GRACE ~450–500 km); DTM2020-Res 10.9 / 16.8 / 20.3%. Bias 2–8% (MSIS00). "Model precision decreases with altitude." Values include instrument/geophysical noise, so they are an upper bound. | `P0_SD` / `Q_SD` derivation; baseline realism check | full text read |
| Bruinsma & Boniface (2021), DTM2020, JSWSC 11:47, doi:10.1051/swsc/2021032 | Quiet/overall CHAMP daily std: NRLMSISE-00 18.4%, JB2008 11.6%, DTM2020 ~12% | Quiet model error | table values unconfirmed (snippet) |
| Evans et al. (2024), GOLD and the May 2024 storm, GRL 51, e2024GL110506. Open copy: https://repository.library.noaa.gov/view/noaa/68704 | ΣO/N₂ "up to 50% lower" at high latitudes; ~50% higher at the equator; the depletion reached the equator for ≥12 h. Column ratio from ~160 km, not in-situ. | Storm composition change realism | full text read |
| Moe, Moe & Wallace (1998), J Spacecraft Rockets 35:266, doi:10.2514/2.3350 | Drag density "better than the present 15% uncertainty" with measured accommodation | `CD_SD` | abstract [OA] |
| March et al. (2021), GSI modelling and density, JSWSC 11:54, doi:10.1051/swsc/2021035 | Accommodation-driven density differences within ±10% (up to 15% at the poles); α = 0.85 most consistent; residual 4–5% | `CD_SD` | abstract [OA] |
| Mehta et al. (2023), Satellite drag coefficient modeling, Adv Space Res 72:5443, doi:10.1016/j.asr.2022.05.064 | Density differences "can reach tens of percent" above 450 km at solar min; scale differences mostly from geometry + GSI | `CD_SD` (high-altitude caveat) | abstract [OA] |
| Mehta et al. (2014), J Spacecraft Rockets 51:873, doi:10.2514/1.A32566 | GRACE: diffuse vs CLL ~15% (solar min), 2–3% (solar max) | `CD_SD` | unconfirmed (snippet) |
| **Synthesis (ours, labeled):** C_D 1σ ≈ 5–15% for a host with known shape and attitude; higher for unknown geometry; tens of percent above 450 km at solar min | | `CD_SD` sweep range | assumption derived from the rows above |
| Song et al. (2023), N₂ electron cross sections, JPCRD 52:023104, doi:10.1063/5.0150618 | N₂ total ionization 2.51 Å² at 100 eV (recommended, 5% uncertainty) | Cross-section ratios | full text read |
| NIST SRD 107 Electron-Impact Ionization database (BEB: Kim & Desclaux 2002 PRA 66:012708 for O, N; Kim & Rudd 1994 PRA 50:3954 for H, He) + experimental compilations | Ratio to N₂ at ~100 eV: **O 0.54–0.58** (Brook 1978, BEB, Thompson 1995); **N 0.53–0.64** (BEB ground state to Brook 1978); **H 0.22–0.23**; **He 0.14**; O₂ 1.00 | Physical bounds on S_O and the N/H factors | NIST tables read |
| Summers (1969), NASA TN D-5285 (NTRS 19690019953); Holanda (1972), NASA TN D-6815 | Total ionization cross section predicts relative gauge sensitivity, "probable error about 10 percent"; "invariant with gage type" (hot cathode). Cold cathode use is an assumption. | Method for S_O / N / H bounds | abstracts read (NTRS) |
| Newton & Horowitz, Explorer 17 density gauges error analysis, NASA TN D-5447 (NTRS 19690031535) | Cold-cathode orbital gauges: densities normalized "to the averaged effect between no and total recombination of oxygen inside the gauge"; nonlinearity and composition sensitivity of cold-cathode gauges discussed | **Flight precedent for bracketing S_O between no and full recombination** | full text read |
| Cooley & Reber (1969), Geoprobe mass spectrometer, GSFC X-621-69-260 (NTRS 19690021372) | Atomic O sensitivity taken as "77% that of molecular oxygen" at 75 eV (Fite & Brackmann ratios); chambers silver-oxide coated to enhance recombination | Older, higher S_O estimate (widens the bracket) | full text read |
| Pelz & Newton (1967), GSFC X-621-67-609 (NTRS 19680014398) | Explorer 17/32 magnetron gauges "oxygen-processed"; did not pump significant O; rocket Bayard-Alpert gauges pumped or adsorbed most O | Gauge O-pumping precedent | full text read |
| Paul et al. (2023), "A review of recombination coefficients of neutral oxygen atoms for various materials", Materials 16:1774, doi:10.3390/ma16051774 | Stainless steel γ 0.002–0.5 (avg 0.10); gold 0.003–0.2; nickel 0.001–0.28; rises with O exposure. Plasma conditions, not ram flux. | Chamber recombination range (γ ≈ 0.01–0.3) | full text read |
| Hoffman & Atlas (2016), "Future observing system simulation experiments", BAMS 97:1601, doi:10.1175/BAMS-D-15-00200.1 | OSSE methodology | Justifying the OSSE | citation verified (Crossref) |
| Our calculation (Nov 8): NRLMSIS 2.1 at 1 s along a 51.6° orbit, real May 2024 drivers | 30 s mean density vs the value at the **window start**: median 0.29–0.35%, max 1.0–1.6% (250/300/450 km, 5 days). vs the value at the **window midpoint**: median 0.003%, max 0.013% (250/450 km, storm onset 36–48 h). | `PRODUCT_TIME` = midpoint; the smooth MSIS part needs no 30 s averaging | computed (scratch script); rerun in the OSSE for the record |
| AR(1) variance of the mean: Var(x̄) ≈ (σ²/N)(1+ρ)/(1−ρ) | Effective sample size N(1−ρ)/(1+ρ) | Converting vendor noise to 30 s | derivation standard; textbook citation (Wilks 2011 / von Storch & Zwiers 1999) unconfirmed |

## Filter and drag literature

| Source | Topic | Status |
|---|---|---|
| Kalman (1960), J Basic Eng 82:35, doi:10.1115/1.3662552 | Kalman filter | verified (Crossref) |
| Rauch, Tung & Striebel (1965), AIAA J 3:1445, doi:10.2514/3.3166 | RTS smoother | verified |
| Julier & Uhlmann (2004), Proc IEEE 92:401, doi:10.1109/JPROC.2003.823141 | UKF | verified |
| Mehra (1970), IEEE TAC 15:175, doi:10.1109/TAC.1970.1099422 | Adaptive Q/R from innovations | verified |
| Friedland (1969), IEEE TAC 14:359, doi:10.1109/TAC.1969.1099223 | Bias estimation in recursive filtering | verified |
| Storz et al. (2005), HASDM, Adv Space Res 36:2497, doi:10.1016/j.asr.2004.02.020 | Model calibration from tracking | verified |
| Bierman (1977), Factorization Methods for Discrete Sequential Estimation, Academic Press (Dover 2006, ISBN 9780486449814) | UD factorization, sequential updates | book verified; chapter unconfirmed |
| Bar-Shalom, Li & Kirubarajan (2001), Estimation with Applications to Tracking and Navigation, Wiley, ISBN 0471416555 | NIS/NEES consistency, χ² gating (believed §5.4) | book verified; section unconfirmed |
| Simon (2006), Optimal State Estimation, Wiley, ISBN 0471708585 | Joseph form, Schmidt-Kalman | book verified |
| Tapley, Schutz & Born (2004), Statistical Orbit Determination, Elsevier, ISBN 0126836302 | Consider covariance (believed Ch. 6) | book verified; chapter unconfirmed |
| Groves (2013), Principles of GNSS, Inertial, and Multisensor Integrated Navigation, 2nd ed., Artech House | Sensor-bias states in integrated navigation | book verified |
| Maybeck (1979), Stochastic Models, Estimation, and Control Vol. 1, Academic Press | Observability, error budgets | book verified |

## Older filter and drag rows

| Source | Values it gives us | Used for | Status |
|---|---|---|---|
| Lowe & D'Amico (2026), Acta Astronautica 245 | GPS-only UKF β error 16 / 9 / 5 / 6% (low / mean / high / May 2024 storm); Harris-Priester 58 / 39 / 13 / 29% with predicted flux; C_D fixed at 2.2; day-averaged; Appendix B Harris-Priester tables; Table 3 tuning | Drag error model, baseline, cross-check | verified (paper PDF read) |
| Filter textbooks (Kalman 1960; Bierman 1977; Bar-Shalom et al. 2001; Simon 2006; Tapley et al. 2004; Rauch et al. 1965; Julier & Uhlmann 2004; Mehra 1970; Friedland 1969; Groves 2013; Maybeck 1979); Storz et al. 2005 (HASDM); Hoffman & Atlas 2016 (OSSE) | Standard components (see status_and_plan, filter section) | Design-rationale table | to verify (research job R1) |
