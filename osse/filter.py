import torch

STATES = ("dO", "dN2", "dHe", "gauge_gain", "o_gain", "cd_bias")
IDX = {name: i for i, name in enumerate(STATES)}
N_STATES = len(STATES)
N_ATOMS = 3

def group_H(terms, G, col):
    tot = terms.sum(1)
    H = torch.zeros(terms.shape[0], N_STATES, device=terms.device, dtype=terms.dtype)
    H[:, :N_ATOMS] = (terms / tot[:, None]) @ G
    H[:, col] = 1.0
    return H, tot

def density(n_prior, x, gidx, mass, amu):
    return (n_prior * torch.exp(x[:, gidx]) * mass).sum(1) * amu