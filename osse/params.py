from dataclasses import dataclass

KINDS = {
    "sourced": "from a datasheet, paper or physical constant (cited)",
    "vendor": "INFICON or Stuttgart will provide it; swept until then",
    "research": "the literature has it",
    "sweep": "unknown; result is 'must be better than X'",
    "choice": "our decision; reasoning written down",
    "assumption": "assumed value; reasoning written down",
}

@dataclass(frozen=True)
class Param:
    value: object
    kind: str
    source: str
    becomes: str = ""
    note: str = ""

    def __post_init__(self):
        if self.kind not in KINDS:
            raise ValueError(f"unknown kind {self.kind!r}")

        if not self.source:
            raise ValueError(f"every number must say where they come from or why")
        
        if self.becomes and self.becomes not in KINDS:
            raise ValueError(f"unknown kind {self.becomes!r} in becomes")



REGISTRY = {}

def reg(name, value, kind, source, becomes="", note=""):
    if name in REGISTRY:
        raise ValueError(f"{name} registered twice")
    
    REGISTRY[name] = Param(value, kind, source, becomes, note)

def value(name):
    return REGISTRY[name].value

def report(kind=None):
    for name, p in REGISTRY.items():
        if kind is None or p.kind == kind:
            tail = f" -> {p.becomes}" if p.becomes else ""
            print(f"{p.kind:>10}{tail:<14} {name:<18} {p.value!r:<28} {p.source}")



# physical constants
reg("AMU", 1.66053906660e-27, "sourced",
    "CODATA 2018 atomic mass constant, Tiesinga et al. 2021 Rev Mod Phys 93:025010 (kg)")
reg("MU", 3.986004418e14, "sourced",
    "WGS84 GM incl. atmosphere, NGA.STND.0036 v1.0.0 (2014) Table 3.1 (m^3/s^2)")
reg("RE", 6371008.8, "sourced",
    "GRS80 mean radius R1=(2a+b)/3 = 6371008.7714 m, Moritz 2000 J Geod 74:128 (m)")
reg("WE", 7.2921159e-5, "sourced",
    "Earth rotation rate, precessing frame, 7.2921158553e-5, NGA.STND.0036 (2014) Table 3.4 (rad/s)")
reg("SPECIES", ("N2", "O2", "O", "He", "H", "Ar", "N"), "sourced",
    "NRLMSIS 2.1 outputs 2-8, Emmert et al. 2022 JGR Space Phys 127:e2022JA030896; pymsis",
    note="anomalous O (output 9) is added into O, as MSIS does for total density; NO excluded, as MSIS does")
reg("MASS", (28.0134, 31.9988, 15.9994, 4.002602, 1.00794, 39.948, 14.0067), "sourced",
    "IUPAC 2005, Wieser 2006 Pure Appl Chem 78:2051 Table 2 (g/mol); N2, O2 = 2x atom",
    note="MSIS uses He=4.0, H=1.0 internally: <0.07% density difference at 250-450 km")


# run setup
reg("DT", 30.0, "choice",
    "OCC in-situ density resolution '30 seconds or faster'; sim steps = 30 s averaged products (s)",
    note="sensor raw rates are separate (vendor); averaging converts them to 30 s; sweep DT for resolution vs precision")
reg("T0", "2024-05-09T00:00", "choice",
    "1.5 days before G5 first observed 22:54 UTC May 10 2024 (NOAA SWPC), so the filter settles first (UTC)")
reg("NDAY", 5, "choice",
    "covers the full storm incl. the second Kp>=5 burst 12 May 21:00-13 May 06:00 UTC (GFZ) and early recovery (days)")
reg("N_PHASES", 32, "choice",
    "convergence test: 16/32/64 phases give overlapping 95% CIs on the median of storm and quiet fused MAE "
    "and storm prior bias (1000 runs each, Nov 8)")
reg("PRODUCT_TIME", "midpoint", "choice",
    "each 30 s product is stamped at its window midpoint; the 30 s mean of MSIS density equals the "
    "midpoint value within 0.013% (our calc, NRLMSIS 2.1, 1 s along-track, May 2024 storm onset)",
    note="the truth wiggles (scales 40-260 s) DO need averaging: done when their researched values go in")


# orbit
reg("ALT_KM", 300, "choice", "middle of the claimed density + composition range 250-450 km (km)")
reg("INC_DEG", 51.6, "assumption", "ISS-like inclination, common for rideshare hosts (deg)",
    becomes="choice", note="fix once the reference host orbits are chosen; also run ~97 deg")
reg("MSIS_VERSION", 2.1, "sourced", "NRLMSIS 2.1, Emmert et al. 2022 JGR Space Phys, doi:10.1029/2022JA030896; via pymsis")


# storm drivers
reg("SW_FILE", "data/SW-All.csv", "sourced",
    "CelesTrak SW-All.csv, read by pymsis; May 2024 Kp/ap identical to GFZ definitive (Matzka et al. 2021, doi:10.5880/Kp.0001)",
    note="pinned copy so results never change; download date goes in docs/sources.md")
reg("F107_KIND", "observed", "sourced",
    "NRLMSIS 2.1 source: F10.7 at the Sun-Earth distance, not 1 AU; GFZ recommends F10.7obs for atmospheric studies")
reg("GEOMAG_MODE", -1, "sourced", "NRLMSIS storm-time mode uses the 3-hourly ap history; pymsis default 1 = daily Ap only")
reg("STORM_HOURS", (39.0, 78.0), "sourced",
    "Kp >= 5 (NOAA G1) continuously 10 May 15:00 to 12 May 06:00 UTC, GFZ definitive (hours after T0)")
reg("QUIET_HOURS", (12.0, 39.0), "assumption",
    "after 12 h of filter settling, up to storm onset; Kp <= 3.7 throughout (GFZ definitive) (hours after T0)",
    becomes="choice", note="settling time to be justified by NEES / convergence")
reg("RECOVERY_HOURS", (78.0, 120.0), "choice",
    "after the main Kp>=5 period to run end; includes the second Kp>=5 burst (93-102 h) and recovery; "
    "scored so post-storm behaviour is not hidden (hours after T0)")

# operator baseline: what forecasters actually had
reg("FORECAST_DIR", "data/swpc", "sourced",
    "NOAA SWPC 3-day forecasts, geomag forecasts and RSGA reports for May 2024, NCEI archive")
reg("FORECAST_RULE", "latest", "choice",
    "at each time, use the newest forecast issued before it (0-1 day lead): the most generous baseline, "
    "so our improvement is not overstated; lead-time binning as in Parker & Linares 2024")
reg("KP_TO_AP", (0, 2, 3, 4, 5, 6, 7, 9, 12, 15, 18, 22, 27, 32, 39, 48, 56, 67, 80, 94,
                 111, 132, 154, 179, 207, 236, 300, 400), "sourced",
    "standard Kp->ap table in thirds 0o..9o (Bartels; Matzka et al. 2021); 20 pairs checked against GFZ May 2024 data")
reg("PRIOR_PAST_AP", "measured", "assumption",
    "hours already past use the measured ap: generous to the baseline (operators had only estimated Kp)")
reg("PRIOR_F107A", 165.0, "assumption",
    "operators have no 81-day centered average; nearest published value is the RSGA 90-day mean, 164-165 (issued 9 May)",
    note="also run the baseline with the true 176.2 as its best case")
reg("PRIOR_F107", "measured", "choice",
    "MSIS uses the previous day's F10.7, which operators already have measured (DRAO); same as truth")


# truth atmosphere: small-scale structure MSIS doesn't have
PH = "placeholder from the reference code"
reg("TRUTH_COMMON_SD", 0.13, "sourced",
    "CHAMP density variability ~9% low / ~13% high geomagnetic activity, 370-450 km (Bruinsma & Forbes 2008); "
    "high-activity value used throughout (1-sigma ln units, before 30 s averaging)",
    note="sweep 0.09-0.13: rougher truth is harder for the filter but also makes the baseline look worse")
reg("TRUTH_COMMON_TAU", 100.0, "assumption",
    "775 km / 7.7 km/s; 775 km = geometric middle of observed 300-2000 km structure scales "
    "(Bruinsma et al. 2006; Garcia et al. 2016) (s)", becomes="sweep", note="sweep 40-260 s")
reg("TRUTH_SPECIES_SD", 0.02, "assumption",
    "per-species small-scale composition structure: no published value; kept small vs the common term",
    becomes="sweep", note="sweep 0-0.10")
reg("TRUTH_SPECIES_TAU", 100.0, "assumption", "same scale as the common structure (s)", becomes="sweep")
reg("TRUTH_MSIS_VERSION", 2.1, "choice",
    "atmosphere model for the TRUTH: 2.1 = identical twin, 0 = NRLMSISE-00 (fraternal sibling, Picone et al. 2002); "
    "the prior always uses MSIS_VERSION")


# CCG (gauge)
reg("R_TRUE", (1.0, 1.01, 0.56, 0.18, 0.22, 1.29, 0.58), "sourced",
    "N2 1 (reference), O2 1.01, He 0.18, Ar 1.29: MKS table (hot + cold cathode). O 0.56, N 0.58, H 0.22: "
    "electron-impact ionization cross section ratio to N2 at ~100 eV (NIST SRD 107: O 0.54-0.58, N 0.53-0.64, "
    "H 0.22-0.23), method per Summers 1969 NASA TN D-5285 (~10%)", becomes="vendor",
    note="O is S_O: bracket ~0.5 (full wall recombination, Explorer 17 practice) to 0.77 (Geoprobe 1969); A2 sweep")
reg("R_FILT", (1.0, 1.01, 0.56, 0.18, 0.22, 1.29, 0.58), "choice",
    "filter uses the same nominal factors; the mismatch cases are the sweeps (A2 for S_O)")
reg("CD_SD", 0.10, "assumption",
    "middle of 5-15% 1-sigma C_D uncertainty from gas-surface-interaction literature (Moe et al. 1998: 15%; "
    "March et al. 2021: +-10%; Mehta et al. 2014, 2023) (ln units)", becomes="sweep",
    note="sweep 0.05-0.15; tens of percent above 450 km at solar min (Mehta 2023)")
reg("GAUGE_GAIN_SD", 0.30, "sourced",
    "MAG084 datasheet accuracy 30% (N2, typical), taken as 1-sigma: the conservative reading (ln units)",
    becomes="vendor", note="INFICON: is 30% 1-sigma or a bound, and what does per-unit calibration achieve; also run 0.10")
reg("GAUGE_DRIFT_SD", 0.02, "assumption", PH + "; gain drift rate, 1-sigma (ln units per day)", becomes="vendor")
reg("GAUGE_NOISE", 0.01, "assumption", PH + "; noise per 30 s reading, 1-sigma (ln units)",
    becomes="vendor", note="needs INFICON noise + sampling rate, converted to 30 s averages")
reg("GAUGE_MODEL", "ram", "choice",
    "ram = gauge sees chamber density from the ram flux balance n_c,i = n_i V cos(theta) sqrt(2 pi m_i / (k T_c)) "
    "(free-molecular orifice, speed ratio s >> 1; thermal terms ~exp(-s^2), <1% even for H), so species weights become "
    "R_i * sqrt(m_i / m_N2); V, cos(theta), T_c common to all gases (known, folded into gain); static = R_i only (old)")


# FIPEX (atomic O)
reg("O_GAIN_SD", 0.30, "vendor",
    "Stuttgart IRS call Nov 9 2026: FIPEX absolute accuracy ~30%, depends on calibration instruments; "
    "taken as 1-sigma (conservative) (ln units)", note="confirm against the spec sheet; is it repeatability or accuracy?")
reg("O_DRIFT_MEAN", 0.03, "assumption", PH + "; mean sensitivity loss (ln units per day, always downward)",
    becomes="vendor")
reg("O_DRIFT_SD", 0.01, "assumption", PH + "; its spread, 1-sigma (ln units per day)", becomes="vendor")
reg("O_NOISE", 0.05, "assumption", PH + "; noise per 30 s reading, 1-sigma (ln units)", becomes="vendor")


# filter: state = [dO, dN2, dHe, gauge gain, O gain, C_D bias]
reg("GROUP", (1, 1, 0, 2, 2, 1, 0), "choice",
    "which correction state scales each species (SPECIES order): O,N->O; N2,O2,Ar->N2; He,H->He; "
    "lumps minor species with the major one they track")
reg("P0_MSIS_SD", (0.20, 0.20, 0.20), "sourced",
    "initial model-gap sd for dO, dN2, dHe from published model-vs-data error, not the identical twin: "
    "Bruinsma & Laurens 2024 JSWSC 14:28 storm std 14.5/21.6/27% (GOCE/CHAMP/GRACE); DE-2 NACS vs MSIS 2.1 storm days "
    "rho -26..+11%, N2 -42..+15% (our replay, Nov 10); 20% best of 10/20/30 on the fraternal test (ln units)")
reg("Q_MSIS_SD", (0.01001, 0.01848, 0.02933), "choice",
    "model-gap random-walk step sd for dO, dN2, dHe per 30 s: 4x the forecast-only value from the twin tables; "
    "x4 brings NEES 6.1 -> 3.3 on the fraternal truth; costs quiet N2 accuracy (ln units)",
    note="tuned against the NRLMSISE-00 truth: re-check on DTM2020 truth so it is not tuned to one model")
reg("FILTER_STRUCTURE", "gauss-markov", "choice",
    "per gas group: slow model gap (random walk) + common and own wiggles (AR(1), same tau/sigma as truth); "
    "lets the filter separate persistent sensor gains from atmosphere; prototype: run-to-run spread ~halved")
reg("CD_DRIFT_SD", 0.01, "assumption",
    "slow C_D change from attitude and surface state over days (ln units per day)", becomes="sweep")
reg("USE_SENSORS", ("gauge", "o", "drag"), "choice", "full suite; subsets run as comparisons")
reg("DRAG_WINDOW", 86400.0, "sourced",
    "GPS-only drag gives day-averaged beta (Lowe & D'Amico 2026); one estimate per UTC day (s)")
reg("DRAG_NOISE", 0.06, "sourced",
    "Lowe & D'Amico 2026: day-averaged beta error 6% for the May 2024 storm (16/9/5% low/mean/high solar activity); "
    "their RMS percent error used as 1-sigma (ln units)")
reg("FILTER_SENSOR_BELIEF", "matched", "choice",
    "filter's starting sensor-state sd = the true calibration spreads and its R = the true sensor noise "
    "(filter knows its sensors); mismatched cases are the sweeps")
reg("LEAK_NOISE", 0.05, "assumption",
    "in-flight calibrated argon leak: absolute gauge-gain reading error, 1-sigma (ln units); L9 budget 3-6%, "
    "leak supplier spec not yet confirmed", becomes="vendor")
reg("LEAK_WINDOW", 86400.0, "choice", "one leak calibration pulse per UTC day (s)")
reg("SO_SD", 0.16, "sourced",
    "1-sigma of ln S_O around the filter's 0.56: physical bracket 0.5-0.77 (NIST cross sections, Explorer 17, Geoprobe); "
    "0.77 sits at +2 sigma (ln(0.77/0.56) = 0.318) (ln units)")
reg("SO_MODE", "consider", "choice",
    "consider = S_O uncertainty carried but never estimated (Schmidt filter); estimate = in-flight S_O estimation; "
    "off = SO_SD ignored (old behaviour)")
reg("SO_TRUTH_SD", 0.16, "sweep",
    "spread of the TRUE ln S_O across runs (0 = truth uses R_TRUE exactly); set equal to SO_SD for the fair "
    "'filter fooled' test (ln units)")
reg("SO_TRUTH_OFFSET", 0.0, "choice",
    "fixed shift added to every run's true ln S_O; used only to measure sensitivities (consider analysis) (ln units)")