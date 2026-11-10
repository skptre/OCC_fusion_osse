import math 
import numpy as np
import torch

from simt import Scenario, kf_predict
from osse.atmosphere import build_tables
from osse.params import value
from osse.filter import IDX, N_STATES, GAP, WC, WG, correction, density, CONSIDER, consider_update
from osse.sensors import drag_predict, drag_true, gauge_predict, gauge_true, o_predict, o_true, leak_true, leak_predict
from osse.metrics import Scorer

class OSSE(Scenario):

    def __init__(self, alt_km=None, n_phases=None, cache_dir="cache", **overrides):
        for name in overrides:
            value(name)
        self.overrides = overrides
        self.alt_km = value("ALT_KM") if alt_km is None else alt_km
        self.n_phases = value("N_PHASES") if n_phases is None else n_phases
        get = self.get
        self.species = value("SPECIES")
        self.o_idx = self.species.index("O")
        self.n2_idx = self.species.index("N2")
        self.he_idx = self.species.index("He")
        self.so_true = math.log(get("R_TRUE")[self.o_idx] / get("R_FILT")[self.o_idx])
        mode = get("SO_MODE")
        self.consider = CONSIDER if mode == "consider" else ()
        self.so_sd = 1e-6 if mode == "off" else get("SO_SD")
        self.dt = get("DT")
        self.a_common, self.kick_common = self._ar1(get("TRUTH_COMMON_SD"), get("TRUTH_COMMON_TAU"))
        self.a_species, self.kick_species = self._ar1(get("TRUTH_SPECIES_SD"), get("TRUTH_SPECIES_TAU"))
        self.truth_np, self.prior_np, self.nper = build_tables(self.alt_km, self.n_phases, cache_dir, get("TRUTH_MSIS_VERSION"))
        self.n_steps = self.truth_np.shape[1]
        self._key = None

    def get(self, name):
        return self.overrides.get(name, value(name))
    
    def _ar1(self, sd, tau):
        x = self.dt / tau
        sd_mean = sd * math.sqrt(2 * (x - 1 + math.exp(-x)) / x ** 2)
        a = math.exp(-x)
        return a, sd_mean * math.sqrt(1 - a ** 2)

    def _build(self, device, dtype):
        key = (str(device), dtype)
        if self._key == key:
            return
        self._key = key
        get = self.get

        def f(a):
            return torch.as_tensor(np.asarray(a), device=device, dtype=dtype)

        self.drag_steps = int(get("DRAG_WINDOW") / self.dt)
        n_win = self.prior_np.shape[1] // self.drag_steps
        day_means = self.prior_np[:, :n_win * self.drag_steps].reshape(self.n_phases, n_win, self.drag_steps, -1).mean(2)
        self.truth = f(self.truth_np)
        self.prior = f(self.prior_np)
        self.prior_day = f(day_means)
        self.o_ref = f(self.truth_np[:, :, self.o_idx].mean(1))
        self.mass = f(value("MASS"))
        w = np.sqrt(np.array(value("MASS")) / value("MASS")[self.n2_idx]) if get("GAUGE_MODEL") == "ram" else 1.0
        self.r_true_t = f(np.array(get("R_TRUE")) * w)
        self.r_filt_t = f(np.array(get("R_FILT")) * w)
        group = value("GROUP")
        self.gidx = torch.as_tensor(group, device=device)
        self.G = f(np.eye(3)[list(group)])
        common_var = self.kick_common ** 2 / (1 - self.a_common ** 2)
        species_var = self.kick_species ** 2 / (1 - self.a_species ** 2)
        day_frac2 = self.dt / 86400
        o_drift_rms = math.hypot(get("O_DRIFT_MEAN"), get("O_DRIFT_SD"))
        gg, og, cd = IDX["gauge_gain"], IDX["o_gain"], IDX["cd_bias"]

        P0 = np.zeros((N_STATES, N_STATES))
        P0[GAP, GAP] = np.diag(np.array(get("P0_MSIS_SD")) ** 2)
        P0[WC, WC] = common_var
        P0[WG, WG] = np.eye(3) * species_var
        P0[gg, gg], P0[og, og], P0[cd, cd] = get("GAUGE_GAIN_SD") ** 2, get("O_GAIN_SD") ** 2, get("CD_SD") ** 2
        P0[IDX["ln_so"], IDX["ln_so"]] = self.so_sd ** 2

        Q = np.zeros((N_STATES, N_STATES))
        Q[GAP, GAP] = np.diag(np.array(get("Q_MSIS_SD")) ** 2)
        Q[WC, WC] = self.kick_common ** 2
        Q[WG, WG] = np.eye(3) * self.kick_species ** 2
        Q[gg, gg] = get("GAUGE_DRIFT_SD") ** 2 * day_frac2
        Q[og, og] = o_drift_rms ** 2 * day_frac2
        Q[cd, cd] = get("CD_DRIFT_SD") ** 2 * day_frac2

        F = np.eye(N_STATES)
        F[WC, WC] = self.a_common
        F[WG, WG] = np.eye(3) * self.a_species

        self.P0, self.Qd, self.F = f(P0), f(Q), f(F)

    def sample(self, n_runs, generator, device, dtype):
        self._build(device, dtype)
        get = self.get

        def normal(mean, sd):
            return mean + sd * torch.randn(n_runs, generator=generator, device=device, dtype=dtype)

        return {
            "phase": torch.randint(0, self.n_phases, (n_runs,), generator=generator, device=device),
            "gauge_gain": normal(0.0, get("GAUGE_GAIN_SD")),
            "gauge_drift": normal(0.0, get("GAUGE_DRIFT_SD")) / 86400,
            "o_gain": normal(0.0, get("O_GAIN_SD")),
            "o_drift": -normal(get("O_DRIFT_MEAN"), get("O_DRIFT_SD")).abs() / 86400,
            "cd_bias": normal(0.0, get("CD_SD")),
            "ln_so": normal(0.0, get("SO_TRUTH_SD")) + get("SO_TRUTH_OFFSET"),
        }

    def init_state(self, params, generator):
        ref = params["gauge_gain"]
        n = ref.shape[0]

        def zeros(*shape):
            return torch.zeros(*shape, device=ref.device, dtype=ref.dtype)

        return {
            "common": zeros(n),
            "species": zeros(n, len(self.species)),
            "x": zeros(n, N_STATES),
            "P": self.P0.expand(n, N_STATES, N_STATES).clone(),
            "truth_ring": zeros(self.nper, n),
            "truth_sum": zeros(n),
            "truth_day": zeros(n),
            "est_day": zeros(n),
            "score": Scorer(n, ref.device, ref.dtype),
            "up_g": torch.ones(n, dtype=torch.bool, device=ref.device),
            "up_o": torch.ones(n, dtype=torch.bool, device=ref.device),
            "cd_walk": zeros(n),
            "cd_sum": zeros(n),
        }

    def step(self, s, k, p, generator):
        x, P = s["x"], s["P"]
        n, dev, dt = x.shape[0], x.device, x.dtype
        get = self.get
        amu = value("AMU")
        use = get("USE_SENSORS")

        def randn(*shape):
            return torch.randn(*shape, generator=generator, device=dev, dtype=dt)

        if k > 0:
            s["common"] = self.a_common * s["common"] + self.kick_common * randn(n)
            s["species"] = self.a_species * s["species"] + self.kick_species * randn(n, len(self.species))

        tk = k * self.dt
        n_true = self.truth[p["phase"], k] * torch.exp(s["common"][:, None] + s["species"])
        s["n_true"] = n_true
        n_prior = self.prior[p["phase"], k]
        rho_true = (n_true * self.mass).sum(1) * amu
        rho_prior = (n_prior * self.mass).sum(1) * amu

        s["truth_day"] = s["truth_day"] + rho_true

        physics_cd = get("CD_TRUTH_MODEL") == "physics"
        if physics_cd:
            if k > 0:
                s["cd_walk"] = s["cd_walk"] + get("CD_DRIFT_SD") * math.sqrt(self.dt / 86400) * randn(n)
            s["cd_sum"] = s["cd_sum"] + get("CD_O_COEF") * torch.log(n_true[:, self.o_idx] / self.o_ref[p["phase"]])

        n_g = n_true.clone()
        n_g[:, self.o_idx] = n_g[:, self.o_idx] * torch.exp(p["ln_so"])
        z_gauge = gauge_true(n_g, self.r_true_t, p["gauge_gain"], p["gauge_drift"], tk, get("GAUGE_NOISE"), randn(n))
        z_o = o_true(n_true[:, self.o_idx], p["o_gain"], p["o_drift"], tk, get("O_NOISE"), randn(n))

        if get("GAPS"):
            s["up_g"] = self._flip(s["up_g"], get("GAUGE_GAP_EVERY"), get("GAUGE_GAP_LEN"), generator)
            s["up_o"] = self._flip(s["up_o"], get("O_GAP_EVERY"), get("O_GAP_LEN"), generator)
        if get("OUTLIER_RATE") > 0:
            hit = torch.rand(n, generator=generator, device=dev, dtype=dt) < get("OUTLIER_RATE")
            z_gauge = z_gauge + hit.to(dt) * get("OUTLIER_SIZE") * torch.sign(randn(n))
        gate = get("NIS_GATE") or None

        n_tot_prior = n_prior.sum(1)
        r_bar = (n_prior * self.r_filt_t).sum(1) / n_tot_prior
        rho_gauge = torch.exp(z_gauge) / r_bar * rho_prior / n_tot_prior

        x, P = kf_predict(x, P, self.F, self.Qd)
        if "gauge" in use:
            e = torch.exp(correction(x)[:, self.gidx])
            h, H = gauge_predict(n_prior, e, self.r_filt_t, self.G, x, self.o_idx)
            x, P, info = consider_update(x, P, H, z_gauge, h, get("GAUGE_NOISE") ** 2, self.consider, mask=s["up_g"], gate=gate)
            s["score"].add_nis("gauge", info, offered=s["up_g"])
            s["score"].add_nis("gauge", info)
        if "o" in use:
            h, H = o_predict(n_prior[:, self.o_idx], x)
            x, P, info = consider_update(x, P, H, z_o, h, get("O_NOISE") ** 2, self.consider, mask=s["up_o"], gate=gate)
            s["score"].add_nis("o", info, offered=s["up_o"])
            s["score"].add_nis("o", info)
        day_end = (k + 1) % self.drag_steps == 0
        if "drag" in use and day_end:
            m = self.drag_steps
            cd_true = p["cd_bias"] + (s["cd_walk"] + s["cd_sum"] / m if physics_cd else 0.0)
            z_drag = drag_true(s["truth_day"] / m, cd_true, get("DRAG_NOISE"), randn(n))
            e = torch.exp(correction(x)[:, self.gidx])
            rho_now = density(n_prior, x, self.gidx, self.mass, amu)
            h, H = drag_predict(self.mass, self.prior_day[p["phase"], k // m], e, self.G,
                                s["est_day"] + rho_now, m, x)
            x, P, info = consider_update(x, P, H, z_drag, h, get("DRAG_NOISE") ** 2, self.consider)
            s["score"].add_nis("drag", info)
        
        leak_end = (k + 1) % int(get("LEAK_WINDOW") / self.dt) == 0
        if "leak" in use and (k == 0 or leak_end):
            z_leak = leak_true(p["gauge_gain"], p["gauge_drift"], tk, get("LEAK_NOISE"), randn(n))
            h, H = leak_predict(x)
            x, P, info = consider_update(x, P, H, z_leak, h, get("LEAK_NOISE") ** 2, self.consider)
            s["score"].add_nis("leak", info)

        rho_est = density(n_prior, x, self.gidx, self.mass, amu)
        s["est_day"] = s["est_day"] + rho_est
        if day_end:
            s["truth_day"] = torch.zeros_like(rho_true)
            s["est_day"] = torch.zeros_like(rho_est)
            s["cd_sum"] = torch.zeros_like(s["cd_sum"])
        s["x"], s["P"] = x, P

        w = s["score"].window(tk / 3600)
        if w is not None:
            o, n2 = self.o_idx, self.n2_idx
            e = torch.exp(correction(x)[:, self.gidx])
            est = {"rho_prior": rho_prior, "rho_gauge": rho_gauge, "rho_fused": rho_est,
                   "O_prior": n_prior[:, o], "O_fused": n_prior[:, o] * e[:, o],
                   "N2_prior": n_prior[:, n2], "N2_fused": n_prior[:, n2] * e[:, n2]}
            truth = {"rho": rho_true, "O": n_true[:, o], "N2": n_true[:, n2]}
            s["score"].add_errors(w, est, truth)
            msis = self.truth[p["phase"], k]
            he = self.he_idx
            x_true = torch.stack([
                torch.log(msis[:, o] / n_prior[:, o]),
                torch.log(msis[:, n2] / n_prior[:, n2]),
                torch.log(msis[:, he] / n_prior[:, he]),
                s["common"],
                s["species"][:, o], s["species"][:, n2], s["species"][:, he],
                p["gauge_gain"] + p["gauge_drift"] * tk,
                p["o_gain"] + p["o_drift"] * tk,
                p["cd_bias"] + ((s["cd_walk"] + get("CD_O_COEF") * torch.log(n_true[:, self.o_idx] / self.o_ref[p["phase"]])) if physics_cd else 0.0), 
                torch.full_like(p["cd_bias"], self.so_true) + p["ln_so"]], dim=1)
            s["score"].add_nees(x, x_true, P)
        return s

    def observe(self, s, k, p):
        o, n2 = self.o_idx, self.n2_idx
        x, P = s["x"], s["P"]
        n_prior = self.prior[p["phase"], k]
        e = torch.exp(correction(x)[:, self.gidx])
        tk = k * self.dt
        a = torch.zeros(N_STATES, device=x.device, dtype=x.dtype)
        a[[IDX["gap_N2"], WC, IDX["w_N2"]]] = 1.0
        return {
            "N2_truth": s["n_true"][:, n2], "N2_prior": n_prior[:, n2], "N2_fused": n_prior[:, n2] * e[:, n2],
            "O_truth": s["n_true"][:, o], "O_prior": n_prior[:, o], "O_fused": n_prior[:, o] * e[:, o],
            "N2_sd": (a @ P @ a).sqrt(),
            "gauge_gain_est": x[:, IDX["gauge_gain"]], "gauge_gain_true": p["gauge_gain"] + p["gauge_drift"] * tk,
            "o_gain_est": x[:, IDX["o_gain"]], "o_gain_true": p["o_gain"] + p["o_drift"] * tk,
            "P": P,
            "x": x,
            "rho_truth": (s["n_true"] * self.mass).sum(1) * value("AMU"),
        }

    def score(self, s, params):
        return s["score"].summary()
    
    def _flip(self, up, every, length, generator):
        u = torch.rand(up.shape[0], generator=generator, device=up.device, dtype=torch.float64)
        return torch.where(up, u >= self.dt / every, u < self.dt / length)