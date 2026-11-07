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
| INFICON call (pending) | Gas factors, 30% breakdown, drift, temperature coefficient, linearity, pumping speed, noise/rate, ignition | `vendor` entries | pending |
| Eberhart et al. (2015), "Measurement of atomic oxygen in the middle atmosphere using solid electrolyte sensors and catalytic probes", Atmos. Meas. Tech. 8:3701–3714. https://amt.copernicus.org/articles/8/3701/2015/ | FIPEX amperometric principle; ~500 °C operation; calibration by microwave O₂ plasma + mass spectrometer | FIPEX model background | verified (earlier research) |
| Eberhart et al. (2019), "Atomic oxygen number densities in the MLT region measured by solid electrolyte sensors on WADIS-2", Atmos. Meas. Tech. 12:2445–2461, doi:10.5194/amt-12-2445-2019. PDF: https://elib.dlr.de/127198/1/Eberhart-amt-12-2445-2019.pdf | Calibration via molecular-beam mass spectrometry; FIPEX measures flux, not density; aerodynamic correction by simulation; electrode orientation matters; unit-to-unit disagreement. Appendix A Table A1 = calibration uncertainty | FIPEX fallback numbers | abstract and reviews verified; Table A1 not yet pulled |
| Stuttgart IRS call, Nov 9 (pending) | Absolute O uncertainty, unit spread, drift, flux→density, angle, rate, channels | `vendor` entries | pending |

## Filter and drag literature

| Source | Values it gives us | Used for | Status |
|---|---|---|---|
| Lowe & D'Amico (2026), Acta Astronautica 245 | GPS-only UKF β error 16 / 9 / 5 / 6% (low / mean / high / May 2024 storm); Harris-Priester 58 / 39 / 13 / 29% with predicted flux; C_D fixed at 2.2; day-averaged; Appendix B Harris-Priester tables; Table 3 tuning | Drag error model, baseline, cross-check | verified (paper PDF read) |
| Filter textbooks (Kalman 1960; Bierman 1977; Bar-Shalom et al. 2001; Simon 2006; Tapley et al. 2004; Rauch et al. 1965; Julier & Uhlmann 2004; Mehra 1970; Friedland 1969; Groves 2013; Maybeck 1979); Storz et al. 2005 (HASDM); Hoffman & Atlas 2016 (OSSE) | Standard components (see status_and_plan, filter section) | Design-rationale table | to verify (research job R1) |
