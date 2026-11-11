# Claims-register audit: docs/proposal_claims.md (Nov 11 2026)

Verdict: BAD as it stands. The citations mostly hold up, but the register cannot go into the proposal yet. It mixes leak and no-leak numbers. The baseline (no-leak) headline it says to quote has not been run. Three citations are mis-attributed or stretched.

No repo file was edited and nothing was committed.

## A. Ranked problems

| # | Sev | Claim (line) | Problem | Evidence | Proposed fix |
|---|---|---|---|---|---|
| 1 | CRITICAL | "Headline numbers = the base_* cases" (L81) vs HEADLINE RESULTS density 3.2/3.6/4.7 etc. (L99-117) and "Baseline (A1, 2000 runs): 3.2/3.6/4.7" (L206) | The quotable headline numbers are the WITH-leak frozen default (L68-69 "daily argon leak"). The baseline is no-leak, and no base_* output exists: out/headline has harsh*, twin, msise00, driver_error, but no base_harsh.csv. There is also no out/phase_a_noleak. The no-leak numbers disagree with each other: 6.5/7.4/7.7 (L90, 100-run PRELIM), 5.2/5.8/6.8 (L205), 6.1/8.6/10.8 (L108, uncalibrated). | `ls out/headline`; scripts/headline.py L35-45 defines base_* | Run base_* (2000 runs) and the phase_a --noleak sweep before quoting anything. Until then, label every headline number "with Phase 2 calibrated leak". Rename L206 "Baseline" to "Leak configuration". |
| 2 | CRITICAL | Cal/val plan (L197, L200), drift tracking (L273-283), S_O same-beam argument (L195-196 "with the leak-anchored gauge gain") | These still describe the leak as baseline: "daily argon-leak gauge calibration", "re-anchored daily by a calibrated leak", "Long-term validity rests on the leak". The Nov 11 decision says the leak is Phase 2 only. | L79-85 vs L195-283 | Rewrite these for the no-leak baseline: the gauge gain is anchored by ground calibration + drag + S_O. Move the leak sentences to "Phase 2 enhancement". Redo the same-beam argument without the leak anchor. |
| 3 | HIGH | "Composition ... initialising thermosphere composition gives most of the storm-forecast benefit (Chartier, Jackson & Mitchell 2013)" (L23-24) | Mis-attribution of scope. Chartier et al. 2013 is a TIEGCM OSSE of the 2003 Halloween storm about storm-time PLASMA (electron) density forecasts. It says nothing about neutral density or drag forecasts. Bibliographic data correct: JGR 118(11):7329-7337, doi:10.1002/2013JA019034. | Crossref; abstract via Bath research portal / Zendy | "In a TIEGCM simulation of the 2003 Halloween storm, initialising thermospheric composition captured nearly all of the benefit of initialising the full thermospheric state for ionospheric forecasts (>=10% better for ~18 h vs <4 h for ionosphere-only; Chartier et al. 2013)." Do not use it as a neutral-density forecast claim. |
| 4 | HIGH | "Datasets themselves disagree by up to 30% (Bruinsma et al. 2023 ASR 72:5476)" (L22) | Wrong paper conflated. ASR 72(12):5476-5489 is Bruinsma, Siemes, Emmert & Mlynczak 2023, "Description and comparison of 21st century thermosphere data", doi:10.1016/j.asr.2022.09.038. It is NOT the OCC review doi:10.1016/j.asr.2023.05.011. Two "Bruinsma et al. 2023" papers are cited without a/b. The "up to 30%" was not checked in the 5476 paper (UNVERIFIED). The review itself says something different: the drag force "can vary by more than 30% depending on the [drag-coefficient] model". | Crossref both DOIs; review text p.2 and p.11 | Cite as Bruinsma, Siemes et al. 2023b with the correct DOI, and read it for the 30% before quoting. Alternative (verified): "drag force can vary by more than 30% depending on the gas-surface model (Bruinsma et al. 2023a)". |
| 5 | HIGH | "Our suite does all of these from a hosted payload" (L18-19), after 3.2.2 (O, N2, O2, He), 3.2.3 and 3.1.3/3.1.4 | Overclaim on three counts. (i) 3.2.2 asks for O2, N2, O, He "by means of mass spectrometers (e.g. DE2) or the Terahertz microwave technique". We give O and N2 only, with no mass spectrometer, which contradicts L25-27. (ii) 3.1.4 is about "indirect observations (e.g. electron densities)" and the covariances they need, not in-situ data in general. (iii) One hosted orbit is not "uninterrupted storm monitoring" in the 3.2.3 sense, which means a sustained database. | Review text §3.1 items 3-4, §3.2 items 2-3 (full text read) | "Our suite answers the review's call for simultaneous density and composition (3.2.2) for the two dominant species, O and N2, from a hosted payload. It provides continuous storm coverage along its orbit (3.2.3). It delivers data-assimilation-ready products with calibrated covariances (3.1.3, in the spirit of 3.1.4)." Keep O2/He as Phase 2. |
| 6 | HIGH | "In situ composition measurements have not been taken since DE-2" framing (L8-15) | The quote is verbatim and correct (review p.6, cites Carignan et al. 1981). More counterexamples exist beyond the ones already listed. (a) A Chinese experimental satellite (2012, ~499 km) flew a miniature magnetic-sector mass spectrometer that detected O, He, N2, O2, H2O (Eur. J. Mass Spectrom. 2017; found by search, not read). (b) San Marco D/L (1988) carried WATS: the register says it carried a neutral mass spectrometer, but its species output was NOT confirmed by search (UNVERIFIED). (c) QB50 INMS / FIPEX, ExoCube, Dellingr: not re-verified in this pass. (d) The review itself names NASA GDC (in-situ composition at 300-400 km) as planned; GDC's later status not checked. Most important: the register's own "safe wording" says "since DE-2 (Bruinsma et al. 2023)" when the quote really carries the paper's own scope. | Review text; web search (Chinese MS) | Keep the register's safe wording, but attribute it: "As the OCC reference review notes, no in-situ composition record has followed DE-2 (Bruinsma et al. 2023); demonstrations since then (e.g. QB50 FIPEX/INMS 2017, ExoCube, a 2012 Chinese mini mass spectrometer) were short or experimental." Never write "first", "only" or "none". |
| 7 | HIGH | Error-bar honesty: "Density and O error bars honest (z~1) with S_O consider" (L177) and "N2 ~2x overconfident" | Contradicted by L74 (calibration factors density x2.0, O x2.8, N2 x3.4) and by real data (NEES p50 18 GRACE-FO, 23-79 DE-2, L135). | L74, L135-136, L177 | Delete L177-178. State "OSSE calibration factors 2.0/2.8/3.4. On real data the filter remains overconfident (NEES 18-79). Real-data error-bar calibration is a Phase 1 task." |
| 8 | HIGH | DE-2 "held out and run once" (L50-51) | Sep 1982 exposed bug (1), and the three fixes came after the first held-out run (L137-143). So the held-out set was run more than once. | L137-143 | "Held-out days were run once. That run exposed a simulation bookkeeping bug on sparse-coverage windows; after three generic fixes (circular-orbit OSSE unchanged to 4 decimals) all held-out days were rerun once." |
| 9 | HIGH | Stage 6 numbers (L153-172) | PRELIM: only 3 recorded runs, and with leak (L151). The baseline is no-leak, and headline.py now records 20 base_harsh runs, which have not been run. The proposal wording at L170-172 quotes "2-3.5x". | L151-152; headline.py L45 | Rerun on base_harsh (20 recorded) before quoting. Otherwise say "simulation, 3 runs, leak configuration". Keep caveats (1)-(3) next to the claim. |
| 10 | MEDIUM | Ratio arithmetic: "4-6x better" density (L103); O "1.4-2.5x" (L104); N2 "~2x better at median" (L105); PRELIM "N2 ~2x better in every window" (L36) | Computed from the register's own numbers: density 15.3/3.2=4.8, 22.9/3.6=6.4, 15.1/4.7=3.2, so 3-6x. O 2.5/1.8/1.3, so 1.3-2.5x. N2 2.0/1.9/1.35. L36 N2 1.8/1.9/1.26. | Arithmetic | "3-6x" (density), "1.3-2.5x" (O), "~2x quiet/storm, 1.35x recovery" (N2). Then recompute everything on the base_* numbers. |
| 11 | MEDIUM | Wall temperature "+-20 K wall swing -> ~+-1.7% gain" (L247-248) vs "1.7%/10 K" (L269) and "+-1.7%/orbit" (L254) | sqrt(T) at 300 K gives 1.65% per 10 K, so +-20 K is +-3.3%. One of the two statements is wrong. | sqrt(320/300)=1.033 | Use "+-10 K -> +-1.7%; +-20 K -> +-3.3%". Check that 3.3% is still inside the swept gauge-drift/noise range (gauge noise was swept to 5%, so probably yes). |
| 12 | MEDIUM | "15-state Gauss-Markov EKF" (L184) | osse/filter.py defines 18 states (3 gaps, 4 wiggles, 2 gains, C_D bias, 4 N2 harmonics, 3 altitude slopes, ln_so). With harmonics off that leaves 14 estimated, ln_so being a consider state. | osse/filter.py L7-11 | "18-state structure (14 active in the frozen configuration; S_O as a consider/estimated state)". Recount once, state the exact number. |
| 13 | MEDIUM | NACS "25% absolute calibration error (PI statement; Carignan et al. 1981)" (L51, L126) | The 25% figure is in the NSSDC NACS data description (PI G. Carignan), not, as far as found, in the Carignan et al. 1981 instrument paper (Space Sci. Instrum. 5:429). The 25% itself is verified; the attribution is not. | NSSDC doc cdaweb.gsfc.nasa.gov/pub/documents/old/miscellaneous_documents_from_nssdc/b46557.txt (via search) | "25% absolute calibration uncertainty (NSSDC DE-2 NACS data documentation, PI G. Carignan; instrument: Carignan et al. 1981)". |
| 14 | MEDIUM | Weimer et al. 2016 cited for "an independent O error" (L46) and "temperature-type model error" (L60) | Weimer, Sutton, Mlynczak & Hunt 2016, JGR 121:5975-5990, doi:10.1002/2016JA022691 is "Intercalibration of neutral density measurements for mapping the thermosphere". It maps exospheric temperature from CHAMP/GRACE density via NRLMSISE-00. The abstract fragments seen mention no separate atomic-O error term, so the O-term attribution is UNVERIFIED. The temperature-type reading (N2 error growing with altitude means a T-infinity error) is fair. | Crossref; abstract fragments | Use Weimer 2016 only for "model error is well described as an exospheric-temperature error". Label the independent O error as our ASSUMPTION, or find the paper that actually adds a δO term (possibly Weimer et al. 2020 SW). |
| 15 | MEDIUM | Emmert et al. 2021 "MSIS 2.x tuned its thermosphere to 1986-2005 data" (L53) and "O ~10%, N2 ~20% lower than NRLMSISE-00" (sources.md) | The abstract confirms that thermospheric N2 and O are lower in 2.0 and that the NRLMSISE-00 thermosphere is "largely retained". The 1986-2005 window and the percentages were not found in the abstract (UNVERIFIED; the agent cited §3.1/§4.7). Note that "largely retained" weakens the circularity defence: NRLMSISE-00 also carries MSIS-86 heritage, which used DE-2. | Abstract via DOAJ/KNMI | Read §3.1/§4.7 before quoting. Safer: "MSIS 2.0 revised thermospheric O and N2 using newer data (Emmert et al. 2021); any residual DE-2 influence favours the prior, not our product." |
| 16 | MEDIUM | "O + N2 ~90%+ of mass at 250-450 km" (L26) | No stored test supports it. The register's own gauge-budget calc (sources.md) gives He number fraction up to 51% at 450 km at solar minimum. Mass fraction is smaller but could be ~10-20%. | sources.md "MSIS gauge-signal budget" | Compute it with MSIS and log it. State it for the declared range: "~90%+ of mass at 250-400 km at moderate/high activity; He matters at 450 km at solar minimum". |
| 17 | MEDIUM | "Meets the 20% benchmark without any external calibration" GRACE-FO (L125). "Error almost all bias ... removable by commissioning cross-calibration" (L122-124) | The reference has an accuracy limit of its own: Siemes et al. 2023 recalibrated these data, and datasets differ by tens of %. So the +13-16% bias may be partly the reference's. Removability is an assumption. Altitude 473-507 km is above the declared composition range. Note the replay results have no saved output file in out/: only scripts/de2_replay.py and data/de2/gracefo_2024-05.npz exist. | ls out/; scripts/gracefo_prep.py | Add: "the remaining bias is comparable to the spread between accelerometer density products". Save the replay CSV to out/replay/ as the evidence pointer. |
| 18 | MEDIUM | GRACE-FO TOLEOS v0003 citation | No formal citation in the register. Product per gracefo_prep.py: ESA Swarm DISC/TOLEOS GF_OPER_DNS1ACC_2_ v0003. Processing reference: Siemes et al. 2023, "New thermosphere neutral mass density and crosswind datasets from CHAMP, GRACE, and GRACE-FO", JSWSC 13:16, doi:10.1051/swsc/2023014 (verified via search; GFZ ref 2023JSWSC..13...16S). Whether v0003 is exactly the Siemes 2023 processing is UNVERIFIED. | Search results | Cite: "GRACE-FO accelerometer-derived density, ESA Swarm DISC TOLEOS product GF_OPER_DNS1ACC_2_ v0003 (processing: Siemes et al. 2023, JSWSC 13:16)". Add a data-access date. |
| 19 | MEDIUM | "Host needs only single-frequency GPS" / "C_D insensitive" (L222-224, L257, L109) | L207-209 already says these do NOT transfer to no-leak. L109 and L257 still state them unqualified. | L207-209 | Mark all of them "(leak configuration)" until out/phase_a_noleak exists. |
| 20 | MEDIUM | "Ground product = smoothed" / RTS improves 20-30% (L40-41) | Contradicts the freeze (L71-72: smoother NOT in the architecture, degrades estimate mode). | L71-72 | Delete L40-41 or mark it "superseded". |
| 21 | LOW-MED | Licata et al. 2022 MSIS-UQ used to justify the truth calibration (L45) | Bibliographic data correct (Space Weather 20(11), e2022SW003267). sources.md says "not yet read". | sources.md L146 | Read it or drop it from L45; Sutton 2018 + Bruinsma & Laurens 2024 suffice. |
| 22 | LOW-MED | Bruinsma & Laurens 2024 numbers 14.5/21.6/27.0% (L20) | Bibliographic data verified (JSWSC 14:28, doi:10.1051/swsc/2024027, 152 storms ap>=80; "model precision decreases with altitude"). The exact numbers could not be re-checked today: journal returns 403, and the arXiv ID 2404.14330 given by bohrium is a different paper. sources.md says full text was read earlier. | Crossref; search snippets | Keep, with the qualifier "std of ln(obs/model) after debiasing, upper bound (includes data noise)". Note these are NRLMSISE-00 values, not MSIS 2.1, and are compared with our MAE (different metric) at L48. |
| 23 | LOW | MAVEN NGIMS / LADEE NMS as calibration-gas heritage (L83, L200) | Partly supported: NGIMS has a "Calibration Reservoir" and a sealed noble-gas mixture for calibration peaks (NGIMS SIS rev 1.3 §3.4.5; 2014 NGIMS paper). That is sealed-gas tuning, not a valved calibrated leak. LADEE NMS UNVERIFIED. | Search results | "calibration-gas heritage (MAVEN NGIMS carries a noble-gas calibration reservoir; Mahaffy et al. 2015)". Drop LADEE unless checked. |
| 24 | LOW | "S_O never measured" (L267) | Absolute. True for MAG084 per INFICON; historic gauges were bracketed (Newton & Horowitz). | L214-215 | "S_O has not been measured for the MAG084 (INFICON, Nov 11)". |
| 25 | LOW | "Gate false-alarm rate matched chi-square exactly" (L175) | No output pointer. "Exactly" invites challenge. | -- | "matched to within sampling error (1.0e-4 observed vs 1e-4 expected, N=...)" plus the file. |
| 26 | LOW | FIPEX "unit gain known to <=12%" requirement (L217) | No sweep in the register gives 12%. | L216-217 | Point to the A3 row that yields 12% or drop it. |
| 27 | LOW | C9 "best estimate" (L107): FIPEX drift 1%/day, gauge 0.5%/day | Labelled "best estimate", but neither number has a source (FIPEX: no drift data; INFICON: "no major drift", non-statistical). | L238-239, L219 | Label it "optimistic ASSUMPTION case". |
| 28 | LOW | One-year simulation "planned (Phase 2)" (L279) vs "planned Stage 7" (L292) | Inconsistent. | -- | Pick one. |
| 29 | LOW | Model error numbers 15.7/23.9 (L33) vs 15.3/22.9/15.1 (L102-103); DE-2 N2 -51...+15% (450 km) vs -42...+15% (<350 km, sources.md) | Old vs new runs, different cutoffs. | -- | Use the final numbers only; state the altitude cutoff with each DE-2 range. |
| 30 | LOW | Altitude range (L29-30) "pending C6 grid" | Pending. OSSE only at 300 km circular (L291). The density claim "higher" rests on Stage 6 (simulation) + GRACE-FO 490 km. | -- | Declare it only after C6. Tie each altitude claim to its test. |

## B. Citation verification

Verified (metadata via Crossref; content as noted):
- Bruinsma, Dudok de Wit, Fuller-Rowell, Garcia-Sage, Mehta, Schiemenz, Shprits, Vasile, Yue, Elvidge (2023), "Thermosphere and satellite drag", Adv. Space Res., doi:10.1016/j.asr.2023.05.011. Crossref gives no volume or pages; cite by DOI. Full text read (NSF PAR copy) and checked:
  - The DE-2 quote is verbatim, including "(Carignan et al. 1981)".
  - "sparsity of data for high solar activity, in particular below 400 km": verbatim. It refers to CHAMP/GRACE/GOCE accelerometer density.
  - 3.2.2: the quote is fair. The paper's order is "(O2, N2, O, He)", followed by "by means of mass spectrometers (e.g. DE2) or the Terahertz microwave technique".
  - 3.2.3: "Uninterrupted high-resolution monitoring of geomagnetic storms".
  - 3.1.3: data assimilation is "the most promising way forward".
  - 3.1.4: "accurate covariance matrices", in the context of indirect observations (see problem 5).
- Bruinsma, Siemes, Emmert, Mlynczak (2023), ASR 72(12):5476-5489, doi:10.1016/j.asr.2022.09.038. Metadata OK; the 30% figure is UNVERIFIED.
- Bruinsma & Laurens (2024), JSWSC 14:28, doi:10.1051/swsc/2024027. Metadata and scope OK; exact numbers not re-checked today.
- Emmert, Jones, Siskind, Drob et al. (2022), "NRLMSIS 2.1...", JGR 127(10), e2022JA030896. OK.
- Emmert et al. (2021), NRLMSIS 2.0, Earth Space Sci. 8(3), doi:10.1029/2020EA001321. Metadata OK; the "lower N2 and O" claim OK; 1986-2005 and the percentages UNVERIFIED.
- Chartier, Jackson & Mitchell (2013), JGR 118(11):7329-7337. Metadata OK; scope misused (problem 3).
- Mehta, Walker, Sutton, Godinez (2017), Space Weather 15(4):558-576, doi:10.1002/2016SW001562. Metadata OK; 5-32% rescaling UNVERIFIED.
- March, Doornbos & Visser (2019), ASR 63:213-238, doi:10.1016/j.asr.2018.07.009. Metadata OK; numbers UNVERIFIED.
- Weimer, Sutton, Mlynczak, Hunt (2016), JGR 121(6):5975-5990, doi:10.1002/2016JA022691. Metadata OK; O-term attribution UNVERIFIED.
- Licata et al. (2022), Space Weather 20(11), e2022SW003267. Metadata OK; content unread.
- Moe, Moe & Wallace (1998), J. Spacecraft Rockets 35(3):266-272, doi:10.2514/2.3350. Metadata OK.
- March, van den IJssel, Siemes, Visser (2021), JSWSC 11:54, doi:10.1051/swsc/2021035. Metadata OK.
- Sutton (2018), Space Weather 16(6):736-753, doi:10.1002/2017SW001785. OK.
- Hoffman & Atlas (2016), BAMS 97(9):1601-1616. OK.
- Laher & Gilmore (1990), J. Phys. Chem. Ref. Data 19:277-305, doi:10.1063/1.555872. Metadata OK; the 0.51 at 70 eV ratio not re-checked.
- Mahaffy et al. (2015), Space Sci. Rev. 195:49-73, doi:10.1007/s11214-014-0091-1. OK (online 2014).
- Cross, Koontz & Hunton (1995), J. Spacecraft Rockets 32(3):496-501. OK. The title is about mass-spectrometer calibration in an atomic-O beam, which supports the AO-beam calibration plan.
- Eberhart et al. (2019), AMT 12(4):2445-2461. OK.
- Bierman (1977), Factorization Methods for Discrete Sequential Estimation, Academic Press. Exists (Crossref book record).
- Siemes et al. (2023), JSWSC 13:16, doi:10.1051/swsc/2023014. OK (GRACE-FO density processing).

UNVERIFIED in this pass (not found or not checked; do not change, but do not claim checked):
- Carignan et al. 1981 content (the 25% is in the NSSDC doc instead).
- Newton & Horowitz 1969 NASA TN D-5447 (sources.md says full text read).
- Schmidt 1966, Adv. Control Syst. 3:293 (standard; pages from memory).
- MKS gas correction factors page (sources.md says verified Nov 8).
- NIST SRD 107.
- Grabe et al. 2010 (DLR, ram formula).
- Bird 1994 section.
- Ray et al. 2023 (AMOS) and Constant et al. 2024 (arXiv:2408.16805): not cited in proposal_claims.md itself. Crossref only showed a Constant et al. AMOS 2025 paper.
- Lowe & D'Amico 2026 (sources.md says PDF read).
- QB50 FIPEX/INMS, ExoCube, Dellingr, San Marco D/L WATS species.
- Chinese 2012 mini mass spectrometer: details from a search snippet only.

## C. Classification of claim groups

- TEST (our runs): Performance/HEADLINE (out/headline/*.csv). Phase A (out/phase_a3/A1-A6.csv). Stage 6 (out/stage6/*.csv). DE-2 dev/held-out and GRACE-FO replay (scripts/de2_replay.py; NO saved output file). Error-bar factors, NEES, gate false-alarm rate, the FIPEX-gain run 0 check, and resource numbers (no file pointers). L33-41 are superseded PRELIM.
- CITATION: Bruinsma 2023a/b, B&L 2024, Chartier 2013, Emmert 2021/2022, Weimer 2016, Licata 2022, Sutton 2018, Hoffman & Atlas 2016, Carignan 1981/NSSDC, Mahaffy 2015, Cross 1995, March 2021, Bird 1994, Grabe 2010, Laher & Gilmore 1990, Newton & Horowitz 1969, Eberhart 2019, Schmidt 1966, Bierman 1977.
- VENDOR: INFICON email Nov 11: 30% max envelope, 5% repeatability, no major drift, linearity, ignition transient, pumping speed, stray field, gas factors He C=5.9 / Ar 0.8 / O2 = air, price. FIPEX data sheet: power, mass, data rate, interface. IRS call (30% accuracy, ~80k USD): user notes.
- ASSUMPTION (see D).

## D. Assumptions a reviewer could attack

| Assumption | Where | Labelled? |
|---|---|---|
| FIPEX drift 3%/day (baseline), 1%/day (C9 "best estimate") | L107, L216, L239, L273 | 3%/day yes (L238-239); 1%/day NO |
| O_GAIN_SD 30% from an IRS phone call (Eberhart 2019 gives +35/-28%) | L238 | yes |
| S_O ground calibration achievable to 5% (no AO data for MAG084) | L68, L211-215 | requirement stated; feasibility not evidenced, so it needs an AO-beam facility citation |
| INFICON 30% "max envelope" treated as 3σ, hence "conservative by ~3x" | L229-230 | NO: inference |
| Gauge drift 2%/day "conservative" from non-statistical lab statement | L219 | partially |
| Gauge noise 1%/30 s "conservative" | L220-221 | partially (vendor) |
| GRACE-FO bias removable by commissioning cross-calibration | L122-124 | NO |
| Truth = NRLMSISE-00 + calibrated driver errors realistic (storm scatter 0.20 at 300 km) | L44-48 | method stated; the "by construction" match compares MAE with std |
| Independent O error in the truth (Weimer 2016 attribution weak) | L46 | NO |
| O + N2 >= 90% of mass 250-450 km | L26 | NO (and false at 450 km solar min) |
| Outgassing negligible at 300 km after ~1 day | L263 | analysis; not labelled |
| Contamination design (bake, no polymers) adequate | L262 | design intent, not tested |
| Leak hardware 50-150 g, ~3.6 mg/yr Ar | L86-89 | yes ("rough estimates") |
| Root cause of overconfidence = within-orbit structure | L179 | yes (HYPOTHESIS) |
| Median-of-30 outlier preprocessing | L293 | yes (caveat) |
| C7 wall-T / pointing inside swept ranges (analysis, not simulated) | L254-256 | yes, but the arithmetic needs fixing (problem 11) |
| EKF 22 µs on STM32H7 | L261 | NO: estimate, needs basis |
| Stage 6 damping time 12 h = driver-error correlation time; random-walk pull 0.1/0.7 | L148, L157 | yes ("choice") |
| One storm, 300 km, 51.6°, 5 days, high solar activity generalises | L291 | yes (caveat) |
| Single-frequency GPS sufficient | L222-224, L257 | NO for no-leak (problem 19) |
| MAG084 magnet compatible with host | L251, L264 | flagged as risk |
