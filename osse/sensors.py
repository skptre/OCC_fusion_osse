import torch 

from osse.filter import IDX, group_H

def gauge_true(n_true, r_true, gain, drift, tk, sd, noise):
    return torch.log((n_true * r_true).sum(1)) + gain + drift * tk + sd * noise

def gauge_predict(n_prior, e, r_filt, G, x):
    H, tot = group_H(r_filt * n_prior * e, G, IDX["gauge_gain"])
    return torch.log(tot) + x[:, IDX["gauge_gain"]], H

def o_true(n_o, gain, drift, tk, sd, noise):
    return torch.log(n_o) + gain + drift * tk + sd * noise

def o_predict(n_prior_o, x):
    H = torch.zeros_like(x)
    for name in ("gap_O", "w_common", "w_O", "o_gain"):
        H[:, IDX[name]] = 1.0
    h = torch.log(n_prior_o) + x[:, IDX["gap_O"]] + x[:, IDX["w_common"]] + x[:, IDX["w_O"]] + x[:, IDX["o_gain"]]
    return h, H

def drag_true(rho_window_mean, cd_bias, sd, noise):
    return torch.log(rho_window_mean) + cd_bias + sd * noise 

def drag_predict(mass, prior_mean, e, G, window_sum, n_steps, x):
    H, _ = group_H(mass * prior_mean * e, G, IDX["cd_bias"])
    return torch.log(window_sum / n_steps) + x[:, IDX["cd_bias"]], H

def leak_true(gain, drift, tk, sd, noise):
    return gain + drift * tk + sd * noise

def leak_predict(x):
    H = torch.zeros_like(x)
    H[:, IDX["gauge_gain"]] = 1.0
    return x[:, IDX["gauge_gain"]], H