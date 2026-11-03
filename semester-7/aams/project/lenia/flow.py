"""Flow Lenia (Plantec et al. 2023; reference code github.com/erwanplantec/FlowLenia).

Growth no longer adds or removes matter; it only says where matter wants to go, so
the total mass is exactly conserved. Optionally every cell carries its own kernel
weights h ("parameter localisation"); they travel with the mass, so different
species can live on one grid, compete for matter and - with mutation - evolve.
"""
import numpy as np

from lenia.classic import growth_fields

SPREAD = 0.65  # half-width of the square each cell's moved mass is spread over
WINDOW = 2     # mass can move at most WINDOW - SPREAD cells per step
MIX_RULES = ("stoch", "avg")


def sobel(a):
    """Periodic Sobel gradients (unnormalised, as in the reference); returns (d/d axis0, d/d axis1)."""
    def d(x, axis):  # central difference along `axis`, smoothed 1-2-1 along the other axis
        diff = np.roll(x, -1, axis) - np.roll(x, 1, axis)
        other = 1 - axis
        return np.roll(diff, 1, other) + 2 * diff + np.roll(diff, -1, other)
    return d(a, 0), d(a, 1)


def affinity(a, kffts, kernels, weights=None):
    """U_dst = sum_k h_k G_k(K_k * A_src); h_k is the kernel's weight, or per cell if `weights` (K, H, W) is given."""
    u = np.zeros_like(a)
    for i, (k, g) in enumerate(zip(kernels, growth_fields(a, kffts, kernels))):
        u[k["dst"]] += (weights[i] if weights is not None else k["h"]) * g
    return u


def flow_velocity(a, u, theta, dt):
    """Per-channel displacement dt * F with F = (1 - alpha) grad U - alpha grad A_total.

    alpha = clip((A / theta)^2, 0, 1): below the critical mass theta matter climbs the
    affinity U; above it "pressure" pushes it away from crowded areas instead.
    """
    g0, g1 = sobel(a.sum(axis=0))
    max_move = WINDOW - SPREAD
    v0, v1 = np.empty_like(a), np.empty_like(a)
    for c in range(a.shape[0]):
        alpha = np.clip((a[c] / theta) ** 2, 0, 1)
        u0, u1 = sobel(u[c])
        v0[c] = np.clip(dt * ((1 - alpha) * u0 - alpha * g0), -max_move, max_move)
        v1[c] = np.clip(dt * ((1 - alpha) * u1 - alpha * g1), -max_move, max_move)
    return v0, v1


def overlap(v):
    """Per-axis overlap of the moved square [v - s, v + s] with the cell at each offset d.

    Only the offset between source and target matters, so this also works on the torus.
    The overlaps of one source over all offsets sum to 2 * SPREAD, i.e. mass is conserved.
    """
    cap = min(1.0, 2 * SPREAD)
    return {d: np.clip(0.5 + SPREAD - np.abs(d - v), 0, cap) for d in range(-WINDOW, WINDOW + 1)}


def flow_step(a, kffts, kernels, theta=1.0, dt=0.2, weights=None, mix="stoch", rng=None):
    """One Flow Lenia update ("reintegration tracking"); returns (new_a, new_weights).

    Each cell's mass moves by its displacement and is shared among the cells its square
    overlaps. With per-cell `weights`, every target cell takes over the weights of the
    mass arriving in it: one source picked at random in proportion to its mass ("stoch",
    as in the paper), or the mass-weighted average ("avg"). Cells nothing flows into keep
    their old weights (they hold no mass, so this only affects where new mass can go).
    """
    v0, v1 = flow_velocity(a, affinity(a, kffts, kernels, weights), theta, dt)
    w0 = [overlap(v0[c]) for c in range(a.shape[0])]
    w1 = [overlap(v1[c]) for c in range(a.shape[0])]
    norm = a / (4 * SPREAD**2)
    out = np.zeros_like(a)
    tracking = weights is not None
    if tracking:
        rng = rng or np.random.default_rng()
        arrived = np.zeros(a.shape[1:])
        chosen = np.full(a.shape[1:], -1)  # stoch: index of the offset whose mass we keep, -1 = none
        mixed = np.zeros_like(weights) if mix == "avg" else None
    offsets = [(d0, d1) for d0 in range(-WINDOW, WINDOW + 1) for d1 in range(-WINDOW, WINDOW + 1)]
    for i, (d0, d1) in enumerate(offsets):
        moved = np.roll(np.stack([norm[c] * w0[c][d0] * w1[c][d1] for c in range(a.shape[0])]),
                        (d0, d1), axis=(1, 2))
        out += moved
        if tracking:
            incoming = moved.sum(axis=0)
            arrived += incoming
            if mix == "stoch":  # weighted reservoir sampling: keeps one source with p = mass share
                take = (incoming > 0) & (rng.random(incoming.shape) * arrived < incoming)
                chosen[take] = i
            else:
                mixed += incoming * np.roll(weights, (d0, d1), axis=(1, 2))
    if not tracking:
        return out, None
    if mix == "avg":
        return out, np.where(arrived > 0, mixed / np.maximum(arrived, 1e-12), weights)
    return out, gather_sources(weights, chosen, offsets)


def gather_sources(weights, chosen, offsets):
    """New weights: each cell copies the weights of the source cell its chosen offset points back to."""
    h, w = weights.shape[1:]
    d = np.array(offsets + [(0, 0)])[chosen]  # chosen == -1 (no incoming mass) -> keep own weights
    rows = (np.arange(h)[:, None] - d[..., 0]) % h
    cols = (np.arange(w)[None, :] - d[..., 1]) % w
    return weights[:, rows, cols]


def mutate(weights, rng, rate=0.0, size=20, scale=0.2):
    """With probability `rate`, add one random vector N(0, scale) to the weights of a size x size patch.

    This is the "beam mutation" of the reference code; weights are kept in [0, 1].
    """
    if rate <= 0 or rng.random() >= rate:
        return weights
    _, h, w = weights.shape
    y, x = rng.integers(0, h), rng.integers(0, w)
    rows, cols = (np.arange(size) + y) % h, (np.arange(size) + x) % w
    out = weights.copy()
    patch = out[:, rows[:, None], cols[None, :]] + rng.normal(0, scale, (weights.shape[0], 1, 1))
    out[:, rows[:, None], cols[None, :]] = np.clip(patch, 0, 1)
    return out
