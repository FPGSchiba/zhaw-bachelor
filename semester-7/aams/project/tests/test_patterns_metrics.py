import numpy as np

from lenia.metrics import circular_stats, classify, snapshot, wrapped_distance
from lenia.patterns import disc_mask, init_state, pattern_mask, place_pattern, stamp_weights

SIZE = 64


def test_place_pattern_wraps_rotates_and_copies():
    z = np.zeros((2, SIZE, SIZE))
    cells = np.ones((2, 3, 5))
    out = place_pattern(z, cells, 0, 0, quarter_turns=1)
    assert out.sum() == 30 and z.sum() == 0
    assert out[0, SIZE - 2, SIZE - 1] == 1  # wrapped around both edges
    assert pattern_mask(z.shape, cells, 0, 0, 1).sum() == 15


def test_stamp_weights_only_touches_mask():
    weights = np.zeros((2, SIZE, SIZE))
    mask = disc_mask(10, 10, 3, SIZE)
    out = stamp_weights(weights, mask, [0.3, 0.7])
    assert np.allclose(out[:, mask], [[0.3], [0.7]]) and out[:, ~mask].sum() == 0 and weights.sum() == 0


def test_init_state_is_reproducible():
    assert np.array_equal(init_state(5, 8, 2, SIZE), init_state(5, 8, 2, SIZE))
    assert not np.array_equal(init_state(5, 8, 2, SIZE), init_state(6, 8, 2, SIZE))


def test_centroid_handles_wrap_around():
    m = np.zeros((SIZE, SIZE))
    m[0:3, 0:3] = 1
    m[-2:, -2:] = 1  # one object straddling the corner
    centroid, concentration = circular_stats(m)
    assert wrapped_distance(centroid, (0, 0), SIZE) < 1.5 and concentration.min() > 0.95


def test_speed_of_a_moving_blob():
    a = np.zeros((1, SIZE, SIZE))
    a[0, 10:14, 10:14] = 1
    s0 = snapshot(a)
    moved = np.roll(a, 3, axis=2)
    s1 = snapshot(moved, a, s0["centroid"])
    assert np.isclose(s1["speed"], 3.0) and s1["activity"] > 0 and s1["mass"] == 16


def test_classify():
    a0 = np.zeros((1, SIZE, SIZE))
    a0[0, 10:20, 10:20] = 1
    still = [{"activity": 0.0, "speed": 0.0, "concentration": 0.99}] * 5
    moving = [{"activity": 0.1, "speed": 0.5, "concentration": 0.99}] * 5
    churning = [{"activity": 0.1, "speed": 0.0, "concentration": 0.7}] * 5
    spread = [{"activity": 0.1, "speed": 0.0, "concentration": 0.05}] * 5
    assert classify(a0, a0 * 0.001, still) == "dies"
    assert classify(a0, np.ones_like(a0), still) == "fills"
    assert classify(a0, a0, still) == "static"
    assert classify(a0, a0, moving) == "moving"
    assert classify(a0, a0, churning) == "dynamic"
    assert classify(a0, a0, spread) == "pattern"
