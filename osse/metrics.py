import torch 

from simt import RunningStats

from osse.params import value
from osse.filter import STATES

WINDOWS = ("quiet", "storm", "recovery")
ESTIMATES = ("rho_prior", "rho_gauge", "rho_fused", "O_prior", "O_fused", "N2_prior", "N2_fused")
SENSORS = ("gauge", "o", "drag", "leak")

class Scorer:

    def __init__(self, n, device, dtype):
        self.errors = {(w,q): RunningStats(n, device, dtype) for w in WINDOWS for q in ESTIMATES}
        self.nis = {s: RunningStats(n, device, dtype) for s in SENSORS}
        self.nees = RunningStats(n, device, dtype)
        self.nees_state = {s: RunningStats(n, device, dtype) for s in STATES}
        self.z_state = {s: RunningStats(n, device, dtype) for s in STATES}
    
    def window(self, hours):
        for w in WINDOWS:
            h0, h1 = value(f"{w.upper()}_HOURS")
            if h0 <= hours < h1:
                return w 

        return None
    
    def add_errors(self, w, est, truth):
        for q in ESTIMATES:
            self.errors[(w, q)].add(est[q] / truth[q.split("_")[0]] - 1)

    def add_nis(self, sensor, info):
        self.nis[sensor].add(info["nis"], mask=info["accepted"])

    def add_nees(self, x, x_true, P):
        d = (x - x_true).unsqueeze(-1)
        nees = (d.mT @ torch.linalg.solve(P, d)).squeeze(-1).squeeze(-1) / x.shape[1]
        self.nees.add(nees)
        err = x - x_true
        sd = torch.diagonal(P, dim1=1, dim2=2).sqrt()
        for i, s in enumerate(STATES):
            z = err[:, i] / sd[:, i]
            self.z_state[s].add(z)
            self.nees_state[s].add(z * z)

    def summary(self):
        out = {}
        for (w, q), stats in self.errors.items():
            out.update(stats.summary(f"{w}_{q}"))
        for s, stats in self.nis.items():
            out[f"nis_{s}"] = stats.summary("x")["x_bias"]
        out["nees"] = self.nees.summary("x")["x_bias"]
        for s in STATES:
            out[f"nees_{s}"] = self.nees_state[s].summary("x")["x_bias"]
            out[f"z_{s}"] = self.z_state[s].summary("x")["x_bias"]
        return out