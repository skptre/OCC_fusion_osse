import math 
import numpy as np
import torch

from simt import Scenario, kf_update_scalar
from osse.atmosphere import build_tables
from osse.params import value
from osse.filter import IDX, N_STATES, density
from osse.sensors import drag_predict, drag_true, gauge_predict, gauge_true, o_predict, o_true
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
        self.dt = get("DT")
        self.a_common, self.kick_common = self._ar1(get("TRUTH_COMMON_SD"), get("TRUTH_COMMON_TAU"))
        self.a_species, self.kick_species = self._ar1(get("TRUTH_SPECIES_SD"), get("TRUTH_SPECIES_TAU"))
        self.truth_np, self.prior_np, self.nper = build_tables(self.alt_km, self.n_phases, cache_dir)
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
        self.mass = f(value("MASS"))
        self.r_true_t = f(get("R_TRUE"))
        self.r_filt_t = f(get("R_FILT"))
        group = value("GROUP")
        self.gidx = torch.as_tensor(group, device=device)
        self.G = f(np.eye(3)[list(group)])
        na = 3
        common_var = self.kick_common ** 2 / (1 - self.a_common ** 2)
        species_var = self.kick_species ** 2 / (1 - self.a_species ** 2)
        common_dq = 2 * self.kick_common ** 2 / (1 + self.a_common)
        species_dq = 2 * self.kick_species ** 2 / (1 + self.a_species)

        P0 = np.zeros((N_STATES, N_STATES))
        P0[:na, :na] = common_var + np.diag(np.array(get("P0_MSIS_SD")) ** 2 + species_var)
        P0[na:, na:] = np.diag(np.array([get("GAUGE_GAIN_SD"), get("O_GAIN_SD"), get("CD_SD")]) ** 2)

        day_frac = math.sqrt(self.dt / 86400)
        o_drift_rms = math.hypot(get("O_DRIFT_MEAN"), get("O_DRIFT_SD"))
        Q = np.zeros((N_STATES, N_STATES))
        Q[:na, :na] = common_dq + np.diag(np.array(get("Q_MSIS_SD")) ** 2 + species_dq)
        Q[na:, na:] = np.diag(np.array([get("GAUGE_DRIFT_SD"), o_drift_rms, get("CD_DRIFT_SD")]) ** 2) * day_frac ** 2

        self.P0 = f(P0)
        self.Qd = f(Q)

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

        z_gauge = gauge_true(n_true, self.r_true_t, p["gauge_gain"], p["gauge_drift"], tk, get("GAUGE_NOISE"), randn(n))
        z_o = o_true(n_true[:, self.o_idx], p["o_gain"], p["o_drift"], tk, get("O_NOISE"), randn(n))

        n_tot_prior = n_prior.sum(1)
        r_bar = (n_prior * self.r_filt_t).sum(1) / n_tot_prior
        rho_gauge = torch.exp(z_gauge) / r_bar * rho_prior / n_tot_prior

        P = P + self.Qd
        if "gauge" in use:
            e = torch.exp(x[:, self.gidx])
            h, H = gauge_predict(n_prior, e, self.r_filt_t, self.G, x)
            x, P, info = kf_update_scalar(x, P, H, z_gauge, h, get("GAUGE_NOISE") ** 2, return_info=True)
            s["score"].add_nis("gauge", info)
        if "o" in use:
            h, H = o_predict(n_prior[:, self.o_idx], x)
            x, P, info = kf_update_scalar(x, P, H, z_o, h, get("O_NOISE") ** 2, return_info=True)
            s["score"].add_nis("o", info)
        day_end = (k + 1) % self.drag_steps == 0
        if "drag" in use and day_end:
            m = self.drag_steps
            z_drag = drag_true(s["truth_day"] / m, p["cd_bias"], get("DRAG_NOISE"), randn(n))
            e = torch.exp(x[:, self.gidx])
            rho_now = density(n_prior, x, self.gidx, self.mass, amu)
            h, H = drag_predict(self.mass, self.prior_day[p["phase"], k // m], e, self.G,
                                s["est_day"] + rho_now, m, x)
            x, P, info = kf_update_scalar(x, P, H, z_drag, h, get("DRAG_NOISE") ** 2, return_info=True)
            s["score"].add_nis("drag", info)

        rho_est = density(n_prior, x, self.gidx, self.mass, amu)
        s["est_day"] = s["est_day"] + rho_est
        if day_end:
            s["truth_day"] = torch.zeros_like(rho_true)
            s["est_day"] = torch.zeros_like(rho_est)
        s["x"], s["P"] = x, P

        w = s["score"].window(tk / 3600)
        if w is not None:
            o, n2 = self.o_idx, self.n2_idx
            e = torch.exp(x[:, self.gidx])
            est = {"rho_prior": rho_prior, "rho_gauge": rho_gauge, "rho_fused": rho_est,
                   "O_prior": n_prior[:, o], "O_fused": n_prior[:, o] * e[:, o],
                   "N2_prior": n_prior[:, n2], "N2_fused": n_prior[:, n2] * e[:, n2]}
            truth = {"rho": rho_true, "O": n_true[:, o], "N2": n_true[:, n2]}
            s["score"].add_errors(w, est, truth)
            x_true = torch.stack([
                torch.log(n_true[:, o] / n_prior[:, o]),
                torch.log(n_true[:, n2] / n_prior[:, n2]),
                torch.log(n_true[:, self.he_idx] / n_prior[:, self.he_idx]),
                p["gauge_gain"] + p["gauge_drift"] * tk,
                p["o_gain"] + p["o_drift"] * tk,
                p["cd_bias"]], dim=1)
            s["score"].add_nees(x, x_true, P)
        return s

    def observe(self, s, k, p):
        o, n2 = self.o_idx, self.n2_idx
        x, P = s["x"], s["P"]
        n_prior = self.prior[p["phase"], k]
        e = torch.exp(x[:, self.gidx])
        tk = k * self.dt
        return {
            "N2_truth": s["n_true"][:, n2], "N2_prior": n_prior[:, n2], "N2_fused": n_prior[:, n2] * e[:, n2],
            "O_truth": s["n_true"][:, o], "O_prior": n_prior[:, o], "O_fused": n_prior[:, o] * e[:, o],
            "N2_sd": P[:, 1, 1].sqrt(),
            "gauge_gain_est": x[:, 3], "gauge_gain_true": p["gauge_gain"] + p["gauge_drift"] * tk,
            "o_gain_est": x[:, 4], "o_gain_true": p["o_gain"] + p["o_drift"] * tk,
        }

    def score(self, s, params):
        return s["score"].summary()