import numpy as np
import pytest

from lenia import flow
from lenia.flow import affinity, flow_step, flow_velocity, mutate, sobel
from lenia.kernels import make_kernel
from lenia.patterns import init_state
from lenia.world import DEFAULT_KERNEL, clean_kernel

SIZE = 48


def setup(channels=1, n_kernels=1, seed=0):
    ks = tuple(clean_kernel({**DEFAULT_KERNEL, "src": i % channels, "dst": (i + 1) % channels,
                             "mu": 0.15 + 0.05 * i, "sigma": 0.03, "h": 0.5 + 0.1 * i}, channels, 8)
               for i in range(n_kernels))
    kf = tuple(make_kernel(8 * k["r"], k["rings"], k["core"], SIZE) for k in ks)
    return init_state(seed, 8, channels, SIZE) * 2, kf, ks


def test_sobel_points_uphill():
    ramp = np.tile(np.arange(SIZE, dtype=float), (SIZE, 1))
    g0, g1 = sobel(ramp)
    assert g1[5, 5] == 8.0 and g0[5, 5] == 0.0


@pytest.mark.parametrize("channels,n_kernels", [(1, 1), (2, 3), (3, 5)])
@pytest.mark.parametrize("theta,dt", [(1.0, 0.2), (0.1, 1.0), (3.0, 0.05)])
def test_mass_is_conserved(channels, n_kernels, theta, dt):
    a, kf, ks = setup(channels, n_kernels)
    total = a.sum(axis=(1, 2))
    for _ in range(30):
        a, _ = flow_step(a, kf, ks, theta, dt)
    assert np.allclose(a.sum(axis=(1, 2)), total, rtol=1e-10) and a.min() >= 0


@pytest.mark.parametrize("mix", ["stoch", "avg"])
def test_mass_is_conserved_with_local_weights(mix):
    a, kf, ks = setup(2, 3)
    rng = np.random.default_rng(0)
    weights = rng.random((3, SIZE, SIZE))
    total = a.sum()
    for _ in range(30):
        a, weights = flow_step(a, kf, ks, weights=weights, mix=mix, rng=rng)
    assert np.isclose(a.sum(), total, rtol=1e-10)
    assert weights.min() >= 0 and weights.max() <= 1


def test_matches_brute_force_geometric_overlap():
    a, kf, ks = setup(1, 1, seed=3)
    out, _ = flow_step(a, kf, ks, 1.0, 0.2)
    v0, v1 = flow_velocity(a, affinity(a, kf, ks), 1.0, 0.2)
    ref, s = np.zeros_like(a[0]), flow.SPREAD
    for i, j in zip(*np.nonzero(a[0])):
        cy, cx = i + 0.5 + v0[0, i, j], j + 0.5 + v1[0, i, j]
        for ti in range(int(np.floor(cy - s)), int(np.floor(cy + s)) + 1):
            for tj in range(int(np.floor(cx - s)), int(np.floor(cx + s)) + 1):
                oy = max(0, min(ti + 1, cy + s) - max(ti, cy - s))
                ox = max(0, min(tj + 1, cx + s) - max(tj, cx - s))
                ref[ti % SIZE, tj % SIZE] += a[0, i, j] * oy * ox / (4 * s * s)
    assert np.allclose(out[0], ref, atol=1e-12)


def test_pressure_spreads_a_dense_block():
    a = np.zeros((1, SIZE, SIZE))
    a[0, 20:28, 20:28] = 3.0
    ks = (clean_kernel({**DEFAULT_KERNEL, "mu": 0.5, "sigma": 0.001}, 1, 8),)  # U = -1 everywhere: no pull
    out, _ = flow_step(a, (make_kernel(8, size=SIZE),), ks)
    assert out.max() < a.max() and np.isclose(out.sum(), a.sum())


def test_stochastic_mixing_copies_existing_weight_vectors():
    a, kf, ks = setup(1, 2)
    vectors = np.array([[0.1, 0.9], [0.7, 0.3]])
    left = (np.arange(SIZE)[None, None, :] < SIZE // 2) & np.ones((1, SIZE, SIZE), dtype=bool)
    weights = np.where(left, vectors[0][:, None, None], vectors[1][:, None, None])
    _, new = flow_step(a, kf, ks, weights=weights, mix="stoch", rng=np.random.default_rng(1))
    found = {tuple(np.round(v, 6)) for v in new.reshape(2, -1).T}
    assert found <= {tuple(v) for v in vectors}


def test_average_mixing_stays_between_sources():
    a, kf, ks = setup(1, 1)
    weights = np.where(np.arange(SIZE)[None, :, None] < SIZE // 2, 0.2, 0.8) * np.ones((1, SIZE, SIZE))
    _, new = flow_step(a, kf, ks, weights=weights, mix="avg")
    assert new.min() >= 0.2 - 1e-12 and new.max() <= 0.8 + 1e-12


def test_mutation_changes_one_patch_and_stays_in_range():
    rng = np.random.default_rng(0)
    weights = np.full((3, SIZE, SIZE), 0.5)
    assert mutate(weights, rng, rate=0.0) is weights
    out = mutate(weights, rng, rate=1.0, size=10, scale=5.0)
    changed = (out != weights).any(axis=0)
    assert changed.sum() == 100 and out.min() >= 0 and out.max() <= 1
    assert np.all(weights == 0.5)  # input untouched
