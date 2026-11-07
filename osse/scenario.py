import math 
import numpy as np
import torch

from simt import Scenario, kf_update_scalar
from osse.atmosphere import build_tables
from osse.params import value

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
        self.dt = get("DT")
        self.a_common = math.exp(-self.dt / get("TRUTH_COMMON_TAU"))
        self.kick_common = get("TRUTH_COMMON_SD") * math.sqrt(1 - self.a_common ** 2)
        self.a_species = math.exp(-self.dt / get("TRUTH_SPECIES_TAU"))
        self.kick_species = get("TRUTH_SPECIES_SD") * math.sqrt(1 - self.a_species ** 2)
        self.truth_np, self.prior_np, self.nper = build_tables(self.alt_km, self.n_phases, cache_dir)
        self.n_steps = self.truth_np.shape[1]
        self._key = None

    def get(self, name):
        return self.overrides.get(name, value(name))

    def _build(self, device, dtype):
        key = (str(device), dtype)
        if self._key == key:
            return
        self._key = key
        get = self.get

        def f(a):
            return torch.as_tensor(np.asarray(a), device=device, dtype=dtype)

        cum = np.cumsum(self.prior_np, axis=1)
        shifted = np.zeros_like(cum)
        shifted[:, self.nper:] = cum[:, :-self.nper]
        self.truth = f(self.truth_np)
        self.prior = f(self.prior_np)
        self.prior_win = f((cum - shifted) / self.nper)
        self.mass = f(value("MASS"))
        self.r_true_t = f(get("R_TRUE"))
        self.r_filt_t = f(get("R_FILT"))
        group = value("GROUP")
        self.gidx = torch.as_tensor(group, device=device)
        self.G = f(np.eye(3)[list(group)])
        self.P0 = torch.diag(f(get("P0_SD")) ** 2)
        self.Qd = torch.diag(f(get("Q_SD")) ** 2)

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
            "x": zeros(n, 6),
            "P": self.P0.expand(n, 6, 6).clone(),
            "truth_ring": zeros(self.nper, n),
            "truth_sum": zeros(n),
            "est_ring": zeros(self.nper, n),
            "est_sum": zeros(n),
            "err_prior": zeros(n),
            "err_gauge": zeros(n),
            "err_fused": zeros(n),
            "n_storm": 0,
        }
    
    def _group_H(self, terms, col):
        tot = terms.sum(1)
        H = torch.zeros(terms.shape[0], 6, device=terms.device, dtype=terms.dtype)
        H[:, :3] = (terms / tot[:, None]) @ self.G
        H[:, col] = 1.0
        return H, tot

    def step(self, s, k, p, generator):
        x, P = s["x"], s["P"]
        n, dev, dt = x.shape[0], x.device, x.dtype
        get = self.get
        amu = value("AMU")
        use = value("USE_SENSORS")

        def randn(*shape):
            return torch.randn(*shape, generator=generator, device=dev, dtype=dt)

        if k > 0:
            s["common"] = self.a_common * s["common"] + self.kick_common * randn(n)
            s["species"] = self.a_species * s["species"] + self.kick_species * randn(n, len(self.species))

        tk = k * self.dt
        n_true = self.truth[p["phase"], k] * torch.exp(s["common"][:, None] + s["species"])
        n_prior = self.prior[p["phase"], k]
        rho_true = (n_true * self.mass).sum(1) * amu
        rho_prior = (n_prior * self.mass).sum(1) * amu

        slot = k % self.nper
        s["truth_sum"] = s["truth_sum"] + rho_true - s["truth_ring"][slot]
        s["truth_ring"][slot] = rho_true

        z_gauge = (torch.log((n_true * self.r_true_t).sum(1)) + p["gauge_gain"] + p["gauge_drift"] * tk
                   + get("GAUGE_NOISE") * randn(n))
        z_o = torch.log(n_true[:, self.o_idx]) + p["o_gain"] + p["o_drift"] * tk + get("O_NOISE") * randn(n)

        n_tot_prior = n_prior.sum(1)
        r_bar = (n_prior * self.r_filt_t).sum(1) / n_tot_prior
        rho_gauge = torch.exp(z_gauge) / r_bar * rho_prior / n_tot_prior

        P = P + self.Qd
        if "gauge" in use:
            e = torch.exp(x[:, self.gidx])
            H, tot = self._group_H(self.r_filt_t * n_prior * e, 3)
            x, P = kf_update_scalar(x, P, H, z_gauge, torch.log(tot) + x[:, 3], get("R_GAUGE") ** 2)
        if "o" in use:
            H = torch.zeros(n, 6, device=dev, dtype=dt)
            H[:, 0] = 1.0
            H[:, 4] = 1.0
            x, P = kf_update_scalar(x, P, H, z_o, torch.log(n_prior[:, self.o_idx]) + x[:, 0] + x[:, 4],
                                    get("R_O") ** 2)
        if "drag" in use and (k + 1) % self.nper == 0:
            z_drag = torch.log(s["truth_sum"] / self.nper) + p["cd_bias"] + get("DRAG_NOISE") * randn(n)
            e = torch.exp(x[:, self.gidx])
            H, _ = self._group_H(self.mass * self.prior_win[p["phase"], k] * e, 5)
            rho_now = (n_prior * e * self.mass).sum(1) * amu
            h = torch.log((s["est_sum"] - s["est_ring"][slot] + rho_now) / self.nper) + x[:, 5]
            x, P = kf_update_scalar(x, P, H, z_drag, h, get("R_DRAG") ** 2)

        rho_est = (n_prior * torch.exp(x[:, self.gidx]) * self.mass).sum(1) * amu
        s["est_sum"] = s["est_sum"] + rho_est - s["est_ring"][slot]
        s["est_ring"][slot] = rho_est
        s["x"], s["P"] = x, P

        h0, h1 = value("REF_STORM_HOURS")
        if h0 <= tk / 3600 < h1:
            s["err_prior"] += (rho_prior / rho_true - 1).abs()
            s["err_gauge"] += (rho_gauge / rho_true - 1).abs()
            s["err_fused"] += (rho_est / rho_true - 1).abs()
            s["n_storm"] += 1
        return s

    def score(self, s, params):
        n = max(s["n_storm"], 1)
        return {
            "storm_err_prior": s["err_prior"] / n,
            "storm_err_gauge": s["err_gauge"] / n,
            "storm_err_fused": s["err_fused"] / n,
        }