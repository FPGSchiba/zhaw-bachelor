"""Initial states and stamping patterns onto the (channels, H, W) state."""
import numpy as np


def disc_mask(cy, cx, radius, size):
    """Boolean mask of a disc on the periodic size x size grid."""
    y, x = np.ogrid[:size, :size]
    dy = np.minimum(np.abs(y - cy), size - np.abs(y - cy))
    dx = np.minimum(np.abs(x - cx), size - np.abs(x - cx))
    return dy**2 + dx**2 <= radius**2


def init_state(seed, radius, channels=1, size=256):
    """A few random circular blobs with random values near the grid centre, in every channel."""
    rng = np.random.default_rng(seed)
    a = np.zeros((channels, size, size))
    for _ in range(rng.integers(3, 7)):
        cy, cx = size // 2 + rng.integers(-radius, radius + 1, size=2)
        mask = disc_mask(cy, cx, rng.integers(radius // 2, radius + 1), size)
        a[:, mask] = rng.random((channels, mask.sum()))
    return a


def place_pattern(a, cells, cy, cx, quarter_turns=0):
    """Return a copy of `a` with `cells` (channels, h, w), rotated by 90 deg * quarter_turns, centred at (cy, cx).

    Wraps around the periodic edges; existing cells keep the larger value.
    """
    pattern = np.rot90(np.asarray(cells, dtype=float), quarter_turns, axes=(1, 2))
    _, h, w = pattern.shape
    rows = (np.arange(h) + cy - h // 2) % a.shape[1]
    cols = (np.arange(w) + cx - w // 2) % a.shape[2]
    out = a.copy()
    region = (slice(None), rows[:, None], cols[None, :])
    out[region] = np.maximum(out[region], pattern[: a.shape[0]])
    return out


def pattern_mask(a_shape, cells, cy, cx, quarter_turns=0):
    """Where place_pattern() would put matter (used to stamp species weights there)."""
    placed = place_pattern(np.zeros(a_shape), cells, cy, cx, quarter_turns)
    return placed.sum(axis=0) > 0


def stamp_weights(weights, mask, vector):
    """Copy of the per-cell weights with `vector` written into the cells under `mask`."""
    out = weights.copy()
    out[:, mask] = np.asarray(vector, dtype=float)[:, None]
    return out
