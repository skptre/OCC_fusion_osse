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
reg("N_PHASES", 32, "assumption", "orbit start points precomputed for speed; convergence untested",
    becomes="choice", note="show results stop changing above some number of phases")


# orbit
reg("ALT_KM", 300, "choice", "middle of the claimed density + composition range 250-450 km (km)")
reg("INC_DEG", 51.6, "assumption", "ISS-like inclination, common for rideshare hosts (deg)",
    becomes="choice", note="fix once the reference host orbits are chosen; also run ~97 deg")
reg("MSIS_VERSION", 2.1, "sourced", "NRLMSIS 2.1, Emmert et al. 2022 JGR Space Phys, doi:10.1029/2022JA030896; via pymsis")


# storm drivers, reference version (bit-identical check only)
REF = "reference code (examples/occ.py); kept only for the bit-identical check"
reg("REF_AP_QUIET", 7.0, "assumption", REF, becomes="sourced")
reg("REF_AP_STEPS", ((39, 94.0), (42, 300.0), (45, 400.0), (57, 207.0), (66, 80.0), (78, 32.0), (90, 15.0)),
    "assumption", REF + "; (hours after T0, ap from then on), hand-typed shape of May 2024", becomes="sourced")
reg("REF_F107_TRUTH", 220.0, "assumption", REF, becomes="sourced")
reg("REF_F107_PRIOR", 200.0, "assumption", REF, becomes="sourced")
reg("REF_F107A", 170.0, "assumption", REF, becomes="sourced")
reg("REF_PRIOR_LAG", 2, "assumption", REF + "; forecast = truth delayed 2 x 3 h", becomes="sourced")
reg("REF_PRIOR_CAP", 100.0, "assumption", REF + "; forecast = truth capped at ap 100", becomes="sourced")


# storm drivers, real version (switched on after the bit-identical check)
reg("SW_FILE", "data/SW-All.csv", "sourced",
    "CelesTrak SW-All.csv, read by pymsis; May 2024 Kp/ap identical to GFZ definitive (Matzka et al. 2021, doi:10.5880/Kp.0001)",
    note="pinned copy so results never change; download date goes in docs/sources.md")
reg("F107_KIND", "observed", "sourced",
    "NRLMSIS 2.1 source: F10.7 at the Sun-Earth distance, not 1 AU; GFZ recommends F10.7obs for atmospheric studies")
reg("GEOMAG_MODE", -1, "sourced", "NRLMSIS storm-time mode uses the 3-hourly ap history; pymsis default 1 = daily Ap only")
reg("STORM_HOURS", (39.0, 78.0), "sourced",
    "Kp >= 5 (NOAA G1) continuously 10 May 15:00 to 12 May 06:00 UTC, GFZ definitive (hours after T0)")

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


# truth atmosphere: small-scale structure MSIS doesn't have
PH = "placeholder from the reference code"
reg("TRUTH_COMMON_SD", 0.05, "assumption", PH + "; all-species AR(1) wiggle, 1-sigma (ln units)",
    becomes="research", note="replace with measured small-scale density variability (CHAMP/GRACE)")
reg("TRUTH_COMMON_TAU", 600.0, "assumption", PH + "; its correlation time (s)", becomes="research")
reg("TRUTH_SPECIES_SD", 0.02, "assumption", PH + "; per-species AR(1) wiggle, 1-sigma (ln units)", becomes="research")
reg("TRUTH_SPECIES_TAU", 900.0, "assumption", PH + "; its correlation time (s)", becomes="research")


# CCG (gauge)
reg("R_TRUE", (1.0, 0.90, 0.58, 0.16, 0.42, 1.45, 0.55), "assumption",
    PH + "; true gas sensitivities vs N2, SPECIES order (hot-cathode table, not this gauge)",
    becomes="vendor", note="INFICON Q1 (O2, He); atomic O is the S_O sweep")
reg("R_FILT", (1.0, 0.90, 0.55, 0.16, 0.42, 1.45, 0.55), "assumption",
    PH + "; filter's belief; O deliberately wrong by 0.03", becomes="sweep")
reg("GAUGE_GAIN_SD", 0.08, "assumption", PH + "; unit-to-unit gain error, 1-sigma (ln units)",
    becomes="sourced", note="datasheet 30%, run as 1-sigma and as bound; per-unit cal level is vendor")
reg("GAUGE_DRIFT_SD", 0.02, "assumption", PH + "; gain drift rate, 1-sigma (ln units per day)", becomes="vendor")
reg("GAUGE_NOISE", 0.01, "assumption", PH + "; noise per 30 s reading, 1-sigma (ln units)",
    becomes="vendor", note="needs INFICON noise + sampling rate, converted to 30 s averages")


# FIPEX (atomic O)
reg("O_GAIN_SD", 0.12, "assumption", PH + "; calibration error, 1-sigma (ln units)",
    becomes="vendor", note="Stuttgart Nov 9; fallback WADIS-2 Table A1")
reg("O_DRIFT_MEAN", 0.03, "assumption", PH + "; mean sensitivity loss (ln units per day, always downward)",
    becomes="vendor")
reg("O_DRIFT_SD", 0.01, "assumption", PH + "; its spread, 1-sigma (ln units per day)", becomes="vendor")
reg("O_NOISE", 0.05, "assumption", PH + "; noise per 30 s reading, 1-sigma (ln units)", becomes="vendor")


# host drag
reg("CD_SD", 0.07, "assumption", PH + "; drag-coefficient bias, 1-sigma (ln units)",
    becomes="research", note="needs a cited C_D uncertainty (15-25% is unsourced)")
reg("DRAG_NOISE", 0.03, "assumption", PH + "; noise per drag estimate, 1-sigma (ln units)",
    becomes="sourced", note="Lowe & D'Amico 2026: 5/9/16% day-averaged")
reg("REF_DRAG_WINDOW", "orbit", "assumption", REF + "; one drag value per orbit, averaged over that orbit",
    becomes="sourced", note="becomes day-averaged (Lowe & D'Amico 2026)")


# filter: state = [dO, dN2, dHe, gauge gain, O gain, C_D bias]
reg("GROUP", (1, 1, 0, 2, 2, 1, 0), "choice",
    "which correction state scales each species (SPECIES order): O,N->O; N2,O2,Ar->N2; He,H->He; "
    "lumps minor species with the major one they track")
reg("P0_SD", (0.5, 0.5, 0.7, 0.10, 0.15, 0.10), "assumption", PH + "; starting uncertainty per state (ln units)",
    becomes="choice", note="justify from prior-vs-truth error statistics + NEES")
reg("Q_SD", (0.02, 0.02, 0.01, 0.0005, 0.0008, 0.0002), "assumption",
    PH + "; random-walk step per 30 s per state (ln units)", becomes="choice", note="tune by NIS/NEES")
reg("R_GAUGE", 0.012, "assumption", PH + "; filter's gauge noise incl. representativeness (ln units)",
    becomes="choice", note="must follow GAUGE_NOISE; tune by NIS")
reg("R_O", 0.05, "assumption", PH + "; filter's FIPEX noise (ln units)", becomes="choice")
reg("R_DRAG", 0.035, "assumption", PH + "; filter's drag noise (ln units)", becomes="choice")
reg("USE_SENSORS", ("gauge", "o", "drag"), "choice", "full suite; subsets run as comparisons")