from pathlib import Path

import numpy as np

from osse.scenario import OSSE

REPO = Path(__file__).resolve().parents[1]


def _fill(a):
    """Fill uncovered (NaN) bins from the last covered bin; they never enter sensor updates or scoring."""
    a = np.array(a, dtype=float, copy=True)
    if a.ndim == 1:
        a = a[:, None]
    ok = ~np.isnan(a).any(1)
    idx = np.where(ok, np.arange(len(a)), 0)
    np.maximum.accumulate(idx, out=idx)
    a = a[idx]
    first = int(np.argmax(ok))
    a[:first] = a[first]
    return a


class DE2Replay(OSSE):

    def __init__(self, window, prior="2.1", **overrides):
        self.window, self.prior_name = window, prior
        overrides.setdefault("GAPS", False)
        super().__init__(n_phases=1, **overrides)

    def _tables(self, cache_dir):
        d = np.load(REPO / "data" / "de2" / f"{self.window}.npz")
        self.de2 = d
        self.cover_np = d["cover"][None, :]
        self.truth_wiggles = False
        self.n_days = int(d["n_days"])
        truth = _fill(d["truth"])[None]
        prior = _fill(d["prior21" if self.prior_name == "2.1" else "prior00"])[None]
        return truth, prior, int(round(5880 / self.dt))

    def _local_time(self):
        return _fill(self.de2["lst"])[:, 0][None]

    def _windows(self):
        return {f"day{d + 1}": (24.0 * d, 24.0 * (d + 1)) for d in range(self.n_days)}
    
    def _altitude(self):
        return _fill(self.de2["alt"])[:, 0][None]