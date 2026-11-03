"""Kernels and growth functions (numpy only).

A kernel K is a ring-shaped weighting of the neighbourhood; K * A (convolution)
gives every cell the weighted mean of its surroundings. A growth function G maps
that mean to [-1, 1]: positive where the neighbourhood suits the rule.
"""
import math

import numpy as np

# Kernel "core": the shape of one ring as a function of x in (0, 1), peaking at x = 0.5 with value 1.
#   exp:  exp(4 - 1 / (x (1 - x)))   smooth bump (Lenia "bump4")
#   poly: (4 x (1 - x))^4            polynomial bump, used by most creatures in Chan's catalogue
KERNEL_CORES = ("exp", "poly")
# Growth mapping G(u) in [-1, 1], with G(mu) = 1:
#   gauss: 2 exp(-(u - mu)^2 / (2 sigma^2)) - 1
#   poly:  2 max(0, 1 - (u - mu)^2 / (9 sigma^2))^4 - 1
GROWTH_KINDS = ("gauss", "poly")


def kernel_core(x, core):
    x = np.asarray(x, dtype=float)
    if core == "poly":
        return (4 * x * (1 - x)) ** 4
    out = np.zeros_like(x)
    inside = (x > 0) & (x < 1)
    out[inside] = np.exp(4 - 1 / (x[inside] * (1 - x[inside])))
    return out


def kernel_shell(r, rings, core):
    """Multi-ring kernel shell (Chan 2019): split 0 <= r < 1 into B = len(rings) equal bands.

    Band i holds one bump of height rings[i], so rings=(1,) is the classic single ring
    and e.g. rings=(1/2, 1, 2/3) gives three concentric rings of different strength.
    A cell then reacts differently to neighbours at different distances, which is
    what makes the richer multi-ring creatures possible.
    """
    b = len(rings)
    br = b * r
    heights = np.asarray(rings, dtype=float)[np.minimum(br.astype(int), b - 1)]
    return np.where(r < 1, kernel_core(br % 1, core) * heights, 0.0)


def make_kernel(radius, rings=(1.0,), core="exp", size=256):
    """Kernel K reaching `radius` cells (may be fractional), returned as its rFFT on a size x size torus.

    The kernel is normalised to sum 1, so K * A is a weighted mean of the
    neighbourhood: u = K * A tells each cell how "full" its surrounding rings are.
    """
    if not any(w > 0 for w in rings):
        raise ValueError("at least one ring weight must be > 0")
    if not 1 <= radius < size / 2:
        raise ValueError(f"kernel radius {radius} must be in [1, {size // 2})")
    reach = math.ceil(radius)
    y, x = np.mgrid[-reach:reach + 1, -reach:reach + 1]
    k = kernel_shell(np.sqrt(x**2 + y**2) / radius, rings, core)
    k /= k.sum()

    assert np.isclose(k.sum(), 1.0), "kernel must sum to 1"
    assert np.allclose(k, k[::-1, :]) and np.allclose(k, k[:, ::-1]) and np.allclose(k, k.T), \
        "kernel must be symmetric"

    # Embed in the full grid with the kernel centre at (0, 0); the wrap-around of
    # the FFT convolution gives us periodic boundaries for free.
    full = np.zeros((size, size))
    full[:2 * reach + 1, :2 * reach + 1] = k
    full = np.roll(full, (-reach, -reach), axis=(0, 1))
    return np.fft.rfft2(full)


def growth(u, mu, sigma, kind="gauss"):
    """Growth mapping: cells whose neighbourhood mean u is close to mu grow (G > 0),
    anything too sparse or too crowded decays (G -> -1). sigma sets the tolerance."""
    if kind == "poly":
        return 2 * np.maximum(0, 1 - (u - mu) ** 2 / (9 * sigma**2)) ** 4 - 1
    return 2 * np.exp(-((u - mu) ** 2) / (2 * sigma**2)) - 1


def convolve(a_fft, kernel_fft, shape):
    """K * A from the precomputed FFTs."""
    return np.fft.irfft2(a_fft * kernel_fft, s=shape)
