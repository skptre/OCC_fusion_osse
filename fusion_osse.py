"""
OCC proof-of-concept: can software turn cheap, imperfect sensors into accurate
density AND composition?  (A small observing-system simulation experiment, OSSE.)

Nature run ("truth"): NRLMSIS 2.1 driven by a synthetic G5-like storm profile
    (shaped like May 10-11, 2024; NOT the exact historical indices) plus
    unmodeled along-track structure (AR(1), ~5%, 10-min correlation).
Prior model (what an operator has): NRLMSIS 2.1 driven by degraded drivers
    (ap forecast lagged 6 h and capped at 100, F10.7 off by -20 sfu) - a proxy
    for the well-documented storm-time underestimate of empirical models.

Simulated cheap sensors on one host in a circular orbit:
  * Ionization gauge: N2-equivalent number density sum(R_i n_i); unknown gain
    (lab-calibrated to +/-10%) that also drifts; 1% noise per 30 s sample.
    The filter's atomic-O sensitivity R_O is deliberately 5% wrong (models
    uncertain O recombination in the chamber).
  * Solid-electrolyte O sensor (FIPEX-type): n_O with unknown gain (+/-15%)
    that degrades over time; 5% noise.
  * Host GPS drag: one orbit-averaged mass density per orbit, biased by an
    unknown drag-coefficient error (+/-10%); 3% noise.

Estimators compared:
  1. Prior model alone.
  2. Gauge alone, converted with the prior model's composition (naive).
  3. Drag alone (orbit-averaged, held for the next orbit).
  4. FUSED: extended Kalman filter estimating log-corrections to O, N2, He
     plus the gauge gain, O-sensor gain and C_D bias jointly, with uncertainty.

Outputs: figures + a JSON/CSV summary in ./out.
Run:  pip install pymsis numpy matplotlib ; python fusion_osse.py
"""
import json, os, math
import numpy as np
from pymsis import msis

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

AMU = 1.66053906660e-27
MU, RE, WE = 3.986004418e14, 6371008.8e0, 7.2921159e-5
# MSIS output columns: 0 rho,1 N2,2 O2,3 O,4 He,5 H,6 Ar,7 N,8 anomO,9 NO,10 T
MASS = {"N2": 28.0134, "O2": 31.9988, "O": 15.9994, "He": 4.002602, "H": 1.00794, "Ar": 39.948, "N": 14.0067}
# Gauge relative sensitivities vs N2 (BA gauge table / ionization cross-section ratios - assumptions)
R_TRUE = {"N2": 1.0, "O2": 0.90, "O": 0.58, "He": 0.16, "H": 0.42, "Ar": 1.45, "N": 0.55}
R_FILT = dict(R_TRUE, O=0.55)      # filter's model of the gauge is imperfect on purpose

DT = 30.0                                          # s, OCC in-situ resolution target
T0 = np.datetime64("2024-05-09T00:00")
NDAY = 4
t = np.arange(0, NDAY * 86400, DT)
dates = T0 + (t * 1e3).astype("timedelta64[ms]")

# ------------------------------------------------------------------ drivers
# Prior-model driver variants: (ap lag in 3-h steps, ap cap, F10.7). "lag6_cap100" is the default
# used for the headline numbers; the others exist so verify.py can show how much the baseline
# error depends on this setup choice.
PRIOR_VARIANTS = {
    "truth":       (0, None, 220.0),   # perfect drivers (only unmodeled structure remains)
    "lag3":        (1, None, 200.0),
    "lag6_cap200": (2, 200.0, 200.0),
    "lag6_cap100": (2, 100.0, 200.0),  # default
    "missed":      (0, 7.0, 200.0),    # storm missed entirely
}

def ap3_profile(kind):
    """3-hourly ap series (index 0 = 3 days before T0 so history exists)."""
    n = (NDAY + 3) * 8
    ap = np.full(n, 7.0)
    hrs = (np.arange(n) - 24) * 3.0               # hours since T0
    for i, h in enumerate(hrs):
        if 39 <= h < 42: ap[i] = 94
        elif 42 <= h < 45: ap[i] = 300
        elif 45 <= h < 57: ap[i] = 400            # Kp 9-
        elif 57 <= h < 66: ap[i] = 207
        elif 66 <= h < 78: ap[i] = 80
        elif 78 <= h < 90: ap[i] = 32
        elif h >= 90: ap[i] = 15
    if kind == "prior":                           # forecast: 6 h late, capped
        kind = "lag6_cap100"
    if kind in PRIOR_VARIANTS:
        lag, cap, _ = PRIOR_VARIANTS[kind]
        if lag: ap = np.concatenate([np.full(lag, 7.0), ap[:-lag]])
        if cap is not None: ap = np.minimum(ap, cap)
    return hrs, ap

def ap_array(kind):
    hrs, ap = ap3_profile(kind)
    th = t / 3600.0
    idx = np.searchsorted(hrs, th, side="right") - 1
    out = np.zeros((len(t), 7))
    for k, i in enumerate(idx):
        day0 = int((i // 8) * 8)
        out[k, 0] = ap[day0:day0 + 8].mean()
        out[k, 1:5] = ap[i], ap[i - 1], ap[i - 2], ap[i - 3]
        out[k, 5] = ap[i - 11:i - 3].mean()
        out[k, 6] = ap[i - 19:i - 11].mean()
    return out

# ------------------------------------------------------------------ orbit
def orbit(alt_km, inc_deg=51.6, raan0=0.0):
    r = RE + alt_km * 1e3
    n = math.sqrt(MU / r ** 3)
    u = n * t
    inc = math.radians(inc_deg)
    lat = np.degrees(np.arcsin(np.sin(inc) * np.sin(u)))
    lon_in = np.arctan2(np.cos(inc) * np.sin(u), np.cos(u)) + raan0
    lon = np.degrees((lon_in - WE * t + np.pi) % (2 * np.pi) - np.pi)
    return lat, lon, 2 * math.pi / n

def run_msis(lat, lon, alt, f107, f107a, aps):
    o = msis.calculate(dates, lon, lat, np.full(len(t), alt), np.full(len(t), f107),
                       np.full(len(t), f107a), aps, geomagnetic_activity=-1, version=2.1)
    o = np.nan_to_num(o, nan=0.0)
    return {"N2": o[:, 1], "O2": o[:, 2], "O": o[:, 3] + o[:, 8], "He": o[:, 4], "H": o[:, 5],
            "Ar": o[:, 6], "N": o[:, 7], "T": o[:, 10]}

def rho_of(n):
    return sum(n[s] * MASS[s] for s in MASS) * AMU

def ar1(rng, n, sigma, tau_s):
    a = math.exp(-DT / tau_s); x = np.zeros(n); e = rng.normal(0, sigma * math.sqrt(1 - a * a), n)
    for k in range(1, n): x[k] = a * x[k - 1] + e[k]
    return x

# groups: which species each log-correction state scales
GROUP = {"O": "O", "N": "O", "N2": "N2", "O2": "N2", "Ar": "N2", "He": "He", "H": "He"}
SPEC = list(MASS)

AP_T, AP_P = None, None
_AP_CACHE = {}

def prior_ap(kind):
    if kind not in _AP_CACHE: _AP_CACHE[kind] = ap_array(kind)
    return _AP_CACHE[kind]

def simulate(alt_km, seed, return_series=False, zero_cal=False, *, prior="lag6_cap100", cal_scale=1.0,
             noise_scale=1.0, filter_knows_cal=False, r_filt_exact=False, filt_conf=1.0, cal_sigma=None, cal_drift=None,
             configs=None):
    """One OSSE run. Keyword options (defaults reproduce the headline setup; verify.py uses them):
      prior            : which degraded-driver variant the prior model gets (see PRIOR_VARIANTS)
      cal_scale        : multiplies the TRUE sensor calibration errors (gains, drifts, C_D bias)
      noise_scale      : multiplies the TRUE sensor noise (filter still assumes the nominal noise)
      filter_knows_cal : filter is told the sensor gains/C_D exactly (tiny prior, no random walk)
      r_filt_exact     : filter uses the true gauge species sensitivities (removes the 5% R_O error)
      filt_conf        : filter claims its sensors are this many times better (R and gain priors / filt_conf)
      cal_sigma        : override the filter's prior 1-sigma on sensor ln-gains, e.g. {"gauge": 1e-3}
                         (keys "gauge", "O", "CD"; small = "this one was calibrated well on the ground")
      cal_drift        : override the filter's per-step random walk on sensor ln-gains, same keys
                         (0 = "this gain does not drift in flight")
      configs          : subset of fused configurations to run (default: all four)
    """
    rng = np.random.default_rng(seed)
    lat, lon, period = orbit(alt_km, raan0=rng.uniform(0, 2 * np.pi) if not return_series else 0.0)
    base_t = run_msis(lat, lon, alt_km, 220.0, 170.0, AP_T)
    base_p = run_msis(lat, lon, alt_km, PRIOR_VARIANTS[prior][2], 170.0, prior_ap(prior))
    RF = R_TRUE if r_filt_exact else R_FILT
    # nature run = MSIS truth x unmodeled structure (partly species-specific)
    common = ar1(rng, len(t), 0.05, 600.0)
    nt = {s: base_t[s] * np.exp(common + ar1(rng, len(t), 0.02, 900.0)) for s in SPEC}
    npri = {s: base_p[s] for s in SPEC}
    rho_t, rho_p = rho_of(nt), rho_of(npri)
    ntot_t = sum(nt[s] for s in SPEC)
    xO_t = nt["O"] / ntot_t
    mbar_t = rho_t / (ntot_t * AMU)

    # ---- sensor truths (random draws within the priors the filter assumes)
    gG0 = rng.normal(0, 0.08); gG_drift = rng.normal(0, 0.02) / 86400      # ln-gain, per s
    gO0 = rng.normal(0, 0.12); gO_drift = -abs(rng.normal(0.03, 0.01)) / 86400
    kCD = rng.normal(0, 0.07)
    gG0, gG_drift, gO0, gO_drift, kCD = (v * cal_scale for v in (gG0, gG_drift, gO0, gO_drift, kCD))
    if zero_cal:   # isolate common-mode (design/model) error: perfect gains and C_D
        gG0 = gG_drift = gO0 = gO_drift = kCD = 0.0
    lnG = gG0 + gG_drift * t
    lnGO = gO0 + gO_drift * t
    ns = noise_scale
    zG = np.log(sum(R_TRUE[s] * nt[s] for s in SPEC)) + lnG + rng.normal(0, 0.01 * ns, len(t))
    zO = np.log(nt["O"]) + lnGO + rng.normal(0, 0.05 * ns, len(t))
    nper = int(round(period / DT))
    drag_idx = np.arange(nper - 1, len(t), nper)
    zD = {int(k): math.log(rho_t[k - nper + 1:k + 1].mean()) + kCD + rng.normal(0, 0.03 * ns) for k in drag_idx}

    # ---- baseline 2: gauge-only with prior-model composition, gain assumed 1
    Rbar_p = sum(RF[s] * npri[s] for s in SPEC) / sum(npri[s] for s in SPEC)
    mbar_p = rho_p / (sum(npri[s] for s in SPEC) * AMU)
    rho_gauge = np.exp(zG) / Rbar_p * mbar_p * AMU
    # ---- baseline 3: drag-only, orbit-mean held until next estimate
    rho_drag = np.full(len(t), np.nan)
    last = None
    for k in range(len(t)):
        if last is not None: rho_drag[k] = last
        if k in zD: last = math.exp(zD[k])

    # ---- FUSED EKF. state x = [dO, dN2, dHe, lnG, lnGO, lnK]
    nx = 6
    gi = {"O": 0, "N2": 1, "He": 2}
    csum = {s: np.cumsum(npri[s]) for s in SPEC}
    def win_mean(s, k):
        a = k - nper + 1
        return (csum[s][k] - (csum[s][a - 1] if a > 0 else 0)) / nper
    def run_ekf(use):
        x = np.zeros(nx)
        cal_sd = np.array([0.10, 0.15, 0.10])               # prior 1-sigma: gauge gain, O gain, C_D
        cal_q = np.array([0.0005, 0.0008, 0.0002])          # random walk per step
        for i, key in enumerate(("gauge", "O", "CD")):
            if cal_sigma and key in cal_sigma: cal_sd[i] = cal_sigma[key]
            if cal_drift and key in cal_drift: cal_q[i] = cal_drift[key]
        if filter_knows_cal: cal_sd, cal_q = np.full(3, 1e-4), np.zeros(3)
        cal_sd = cal_sd / filt_conf
        P = np.diag(np.concatenate([[0.5 ** 2, 0.5 ** 2, 0.7 ** 2], cal_sd ** 2]))
        Qd = np.diag(np.concatenate([[0.02 ** 2, 0.02 ** 2, 0.01 ** 2], cal_q ** 2]))
        Rg, Ro, Rd = (v / filt_conf ** 2 for v in (0.012 ** 2, 0.05 ** 2, 0.035 ** 2))  # incl. representativeness
        n = len(t)
        out = {k_: np.zeros(n) for k_ in ("rho", "sig", "xO", "mbar")}
        nis = {"gauge": [], "O": [], "drag": []}            # normalized innovation squared, per sensor
        def update(z, h, H, Rv, key):
            nonlocal x, P
            S = H @ P @ H + Rv
            nu = z - h
            nis[key].append(nu * nu / S)
            K = P @ H / S
            x = x + K * nu
            P = (np.eye(nx) - np.outer(K, H)) @ P
        def rho_now(xv, k):
            return sum(npri[s][k] * math.exp(xv[gi[GROUP[s]]]) * MASS[s] for s in SPEC) * AMU
        for k in range(n):
            P = P + Qd
            if "g" in use:
                e = {s: math.exp(x[gi[GROUP[s]]]) for s in SPEC}
                terms = {s: RF[s] * npri[s][k] * e[s] for s in SPEC}
                tot = sum(terms.values())
                H = np.zeros(nx)
                for s in SPEC: H[gi[GROUP[s]]] += terms[s] / tot
                H[3] = 1.0
                update(zG[k], math.log(tot) + x[3], H, Rg, "gauge")
            if "o" in use:
                H = np.zeros(nx); H[0] = 1.0; H[4] = 1.0
                update(zO[k], math.log(npri["O"][k]) + x[0] + x[4], H, Ro, "O")
            if "d" in use and k in zD:
                e = {s: math.exp(x[gi[GROUP[s]]]) for s in SPEC}
                terms = {s: MASS[s] * win_mean(s, k) * e[s] for s in SPEC}
                tot = sum(terms.values())
                H = np.zeros(nx)
                for s in SPEC: H[gi[GROUP[s]]] += terms[s] / tot
                H[5] = 1.0
                # predicted orbit mean uses the filter's own along-track estimate history
                # (removes within-orbit representativeness error during fast storm changes)
                hist = out["rho"][k - nper + 1:k]
                h_orbit = math.log(np.mean(np.append(hist, math.exp(math.log(tot * AMU)) * 0 + rho_now(x, k)))) if len(hist) else math.log(tot * AMU)
                update(zD[k], h_orbit + x[5], H, Rd, "drag")
            e = {s: math.exp(x[gi[GROUP[s]]]) for s in SPEC}
            nm = {s: npri[s][k] * e[s] for s in SPEC}
            rho = sum(nm[s] * MASS[s] for s in SPEC) * AMU
            J = np.zeros(nx)
            for s in SPEC: J[gi[GROUP[s]]] += nm[s] * MASS[s] * AMU / rho
            out["rho"][k] = rho; out["sig"][k] = math.sqrt(J @ P @ J)
            ntot = sum(nm.values()); out["xO"][k] = nm["O"] / ntot; out["mbar"][k] = rho / (ntot * AMU)
        out["x_final"] = x.copy()
        out["nis"] = {k_: float(np.mean(v)) for k_, v in nis.items() if v}
        return out
    CONFIGS = {"fused_gauge_O_drag": "god", "fused_gauge_drag": "gd", "fused_gauge_O": "go", "fused_O_drag": "od"}
    if configs is not None: CONFIGS = {k_: CONFIGS[k_] for k_ in configs}
    ek = {name: run_ekf(u) for name, u in CONFIGS.items()}

    hrs = t / 3600
    storm = (hrs >= 39) & (hrs < 72)
    quiet = hrs < 36
    allm = np.ones(len(t), bool)
    def stats(est, mask, truth=rho_t):
        ok = mask & np.isfinite(est)
        err = est[ok] / truth[ok] - 1
        return {"MAPE": float(np.mean(np.abs(err))), "bias": float(np.mean(err)), "P95": float(np.percentile(np.abs(err), 95))}
    res = {"alt_km": alt_km, "seed": seed}
    ests = {"prior_model": rho_p, "gauge_only": rho_gauge, "drag_only": rho_drag}
    ests.update({n_: ek[n_]["rho"] for n_ in CONFIGS})
    for name, est in ests.items():
        res[name] = {"quiet": stats(est, quiet), "storm": stats(est, storm), "all": stats(est, allm)}
    xO_p = npri["O"] / sum(npri[s] for s in SPEC)
    res["composition"] = {"prior_model": {"xO_MAE_pp_storm": float(np.mean(np.abs(xO_p - xO_t)[storm]) * 100),
                                           "mbar_MAPE_storm": float(np.mean(np.abs(mbar_p / mbar_t - 1)[storm]))}}
    for n_ in CONFIGS:
        o = ek[n_]
        z = np.abs(np.log(o["rho"] / rho_t)) / o["sig"]
        res[n_]["cov2sig"] = float(np.mean(z < 2))
        res[n_]["NEES_rho"] = float(np.mean(z ** 2))       # ~1 = honest, <1 cautious, >1 overconfident
        res[n_]["NIS"] = o["nis"]                          # ~1 per sensor = noise assumptions right
        res["composition"][n_] = {"xO_MAE_pp_storm": float(np.mean(np.abs(o["xO"] - xO_t)[storm]) * 100),
                                  "mbar_MAPE_storm": float(np.mean(np.abs(o["mbar"] / mbar_t - 1)[storm]))}
    if "fused_gauge_O_drag" in ek:
        xf = ek["fused_gauge_O_drag"]["x_final"]
        res["gain_errors_final_ln"] = {"gauge": float(xf[3] - (gG0 + gG_drift * t[-1])),
                                       "O_sensor": float(xf[4] - (gO0 + gO_drift * t[-1])), "CD": float(xf[5] - kCD),
                                       "gauge_prior": float(gG0 + gG_drift * t[-1]), "O_prior": float(gO0 + gO_drift * t[-1]), "CD_prior": float(kCD)}
    res["storm_composition_shift"] = {"xO_truth_quiet_mean": float(xO_t[quiet].mean()), "xO_truth_storm_min": float(xO_t[storm].min()),
                                      "mbar_truth_quiet": float(mbar_t[quiet].mean()), "mbar_truth_storm_max": float(mbar_t[storm].max())}
    series = None
    if return_series:
        f = ek["fused_gauge_O_drag"]; g = ek["fused_gauge_drag"]
        series = dict(hrs=hrs, rho_t=rho_t, rho_p=rho_p, rho_gauge=rho_gauge, rho_drag=rho_drag, rho_f=f["rho"],
                      sig=f["sig"], rho_gd=g["rho"], xO_t=xO_t, xO_p=xO_p, xO_f=f["xO"], xO_gd=g["xO"],
                      mbar_t=mbar_t, mbar_p=mbar_p, mbar_f=f["mbar"], mbar_gd=g["mbar"],
                      ap=AP_T[:, 1], ap_p=AP_P[:, 1])
    return res, series

AP_T, AP_P = ap_array("truth"), prior_ap("lag6_cap100")

if __name__ == "__main__":
    all_res = {}
    for alt in (300, 450):
        res0, ser = simulate(alt, seed=1, return_series=True)
        np.savez_compressed(os.path.join(OUT, f"series_{alt}km.npz"), **ser)
        mc = []
        for sd in range(2, 42):          # 40 Monte Carlo runs: new noise, gains, C_D bias, orbit phase
            r, _ = simulate(alt, seed=sd)
            mc.append(r)
        cm = [simulate(alt, seed=sd, zero_cal=True)[0] for sd in range(100, 110)]
        all_res[alt] = {"reference_run": res0, "monte_carlo": mc, "common_mode_only": cm}
        print(alt, "done")
    with open(os.path.join(OUT, "results.json"), "w") as f:
        json.dump(all_res, f, indent=1)
