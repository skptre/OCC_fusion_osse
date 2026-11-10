import torch


def rts(xf, Pf, F, Q):
    # Rauch-Tung-Striebel smoother for x[k+1] = F x[k] + w, w ~ N(0, Q).
    # xf (K, N, n): filtered means after each step's updates; Pf (K, N, n, n): their covariances.
    # Returns smoothed means and covariances, same shapes.
    xs, Ps = xf.clone(), Pf.clone()
    for k in range(xf.shape[0] - 2, -1, -1):
        Pp = F @ Pf[k] @ F.T + Q
        C = torch.linalg.solve(Pp, F @ Pf[k]).mT
        xp = xf[k] @ F.T
        xs[k] = xf[k] + (C @ (xs[k + 1] - xp).unsqueeze(-1)).squeeze(-1)
        Ps[k] = Pf[k] + C @ (Ps[k + 1] - Pp) @ C.mT
    return xs, Ps