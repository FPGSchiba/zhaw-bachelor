"""Classic (multi-channel) Lenia update, as in Chan's "Lenia and Expanded Universe" (2020)."""
import numpy as np

from lenia.kernels import convolve, growth


def growth_fields(a, kffts, kernels):
    """G_k(K_k * A_src) for every kernel k; `a` has shape (channels, H, W)."""
    a_fft = np.fft.rfft2(a)  # one FFT per channel, shared by all kernels reading it
    shape = a.shape[1:]
    return [growth(convolve(a_fft[k["src"]], kf, shape), k["mu"], k["sigma"], k["growth"])
            for k, kf in zip(kernels, kffts)]


def classic_step(a, kffts, kernels, dt=0.1, binary=False):
    """A_dst <- clip(A_dst + dt * sum_k h_k G_k / sum_k h_k, 0, 1) for every channel.

    With one channel and one kernel this is exactly A <- clip(A + dt * G(K * A), 0, 1).
    Channels that no kernel writes into stay unchanged.
    """
    fields = growth_fields(a, kffts, kernels)
    change = np.zeros_like(a)
    weight = np.zeros(a.shape[0])
    for k, g in zip(kernels, fields):
        change[k["dst"]] += k["h"] * g
        weight[k["dst"]] += k["h"]
    has_input = weight > 0
    out = a.copy()
    out[has_input] = np.clip(a[has_input] + dt * change[has_input] / weight[has_input, None, None], 0, 1)
    return (out > 0.5).astype(float) if binary else out
