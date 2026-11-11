# Gauss-Markov structure: each gas group's log correction = slow model gap (random walk) + common wiggle + its own wiggle (both AR(1), matching the truth).

import torch
import math
import numpy as np

STATES = ("gap_O", "gap_N2", "gap_He", "w_common", "w_O", "w_N2", "w_He",
          "gauge_gain", "o_gain", "cd_bias", "n2_c1", "n2_s1", "n2_c2", "n2_s2", "ln_so")
IDX = {name: i for i, name in enumerate(STATES)}
N_STATES = len(STATES)
GAP = slice(0, 3)
WC = IDX["w_common"]
WG = slice(4, 7)
HARM = slice(IDX["n2_c1"], IDX["n2_c1"] + 4)
N2G = 1
CONSIDER = (IDX["ln_so"],)
NEES_STATES = STATES[:IDX["cd_bias"] + 1] + ("ln_so",)

def lt_basis(lt_hours):
    w = 2 * math.pi * lt_hours / 24
    return np.stack([np.cos(w), np.sin(w), np.cos(2 * w), np.sin(2 * w)], axis=-1)


def correction(x, basis=None):
    c = x[:, GAP] + x[:, WC:WC + 1] + x[:, WG]
    if basis is not None:
        c = c.clone()
        c[:, N2G] = c[:, N2G] + (x[:, HARM] * basis).sum(1)
    return c



def group_H(terms, G, col, basis=None):
    tot = terms.sum(1)
    share = (terms / tot[:, None]) @ G
    H = torch.zeros(terms.shape[0], N_STATES, device=terms.device, dtype=terms.dtype)
    H[:, GAP] = share
    H[:, WC] = share.sum(1)
    H[:, WG] = share
    if basis is not None:
        H[:, HARM] = share[:, N2G:N2G + 1] * basis
    H[:, col] = 1.0
    return H, tot


import math

STATES = ("gap_O", "gap_N2", "gap_He", "w_common", "w_O", "w_N2", "w_He",
          "gauge_gain", "o_gain", "cd_bias", "n2_c1", "n2_s1", "n2_c2", "n2_s2", "ln_so")
IDX = {name: i for i, name in enumerate(STATES)}
N_STATES = len(STATES)
GAP = slice(0, 3)
WC = IDX["w_common"]
WG = slice(4, 7)
HARM = slice(IDX["n2_c1"], IDX["n2_c1"] + 4)
N2G = 1
CONSIDER = (IDX["ln_so"],)
NEES_STATES = STATES[:IDX["cd_bias"] + 1] + ("ln_so",)


def lt_basis(lt_hours):
    w = 2 * math.pi * lt_hours / 24
    return np.stack([np.cos(w), np.sin(w), np.cos(2 * w), np.sin(2 * w)], axis=-1)


def correction(x, basis=None):
    c = x[:, GAP] + x[:, WC:WC + 1] + x[:, WG]
    if basis is not None:
        c = c.clone()
        c[:, N2G] = c[:, N2G] + (x[:, HARM] * basis).sum(1)
    return c


def group_H(terms, G, col, basis=None):
    tot = terms.sum(1)
    share = (terms / tot[:, None]) @ G
    H = torch.zeros(terms.shape[0], N_STATES, device=terms.device, dtype=terms.dtype)
    H[:, GAP] = share
    H[:, WC] = share.sum(1)
    H[:, WG] = share
    if basis is not None:
        H[:, HARM] = share[:, N2G:N2G + 1] * basis
    H[:, col] = 1.0
    return H, tot


def density(n_prior, x, gidx, mass, amu, basis=None):
    return (n_prior * torch.exp(correction(x, basis)[:, gidx]) * mass).sum(1) * amu

def consider_update(x, P, H, z, h, r2, consider=(), mask=None, gate=None):
    PH = (P @ H.unsqueeze(-1)).squeeze(-1)
    S = (H * PH).sum(1) + r2
    nu = z - h
    nis = nu ** 2 / S
    accept = torch.isfinite(nu)
    if mask is not None:
        accept = accept & mask
    if gate is not None:
        accept = accept & (nis < gate)
    K = PH / S[:, None] * accept[:, None].to(PH.dtype)
    if consider:
        K[:, list(consider)] = 0.0
    nu = torch.where(accept, nu, torch.zeros_like(nu))
    x = x + K * nu[:, None]
    I = torch.eye(P.shape[-1], device=P.device, dtype=P.dtype)
    A = I - K[:, :, None] * H[:, None, :]
    P = A @ P @ A.mT + r2 * (K[:, :, None] * K[:, None, :])
    return x, P, {"nis": nis, "accepted": accept}
