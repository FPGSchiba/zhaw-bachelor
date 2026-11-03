import numpy as np

from lenia.classic import classic_step
from lenia.kernels import growth, make_kernel
from lenia.patterns import init_state
from lenia.world import DEFAULT_KERNEL, clean_kernel

SIZE = 64


def kernels(*overrides, channels=1):
    return tuple(clean_kernel({**DEFAULT_KERNEL, **o}, channels, 10) for o in overrides)


def test_single_channel_equals_original_update():
    a = init_state(1, 10, 1, SIZE)
    ks = kernels({})
    kf = make_kernel(10, size=SIZE)
    u = np.fft.irfft2(np.fft.rfft2(a[0]) * kf, s=(SIZE, SIZE))
    expected = np.clip(a[0] + 0.1 * growth(u, 0.15, 0.015), 0, 1)
    assert np.allclose(classic_step(a, (kf,), ks, 0.1)[0], expected)


def test_weighted_average_of_kernels_into_one_channel():
    a = init_state(2, 10, 1, SIZE)
    kf = make_kernel(10, size=SIZE)
    one = classic_step(a, (kf,), kernels({"mu": 0.15}), 0.1)
    two = classic_step(a, (kf, kf), kernels({"mu": 0.15, "h": 0.3}, {"mu": 0.15, "h": 0.9}), 0.1)
    assert np.allclose(one, two)  # identical kernels: the weights cancel out


def test_channel_without_input_is_unchanged_and_input_is_not_mutated():
    a = init_state(3, 10, 2, SIZE)
    before = a.copy()
    out = classic_step(a, (make_kernel(10, size=SIZE),), kernels({"src": 0, "dst": 0}, channels=2), 0.1)
    assert np.array_equal(out[1], a[1]) and np.array_equal(a, before)


def test_binary_mode_only_produces_zero_and_one():
    a = init_state(4, 10, 1, SIZE)
    out = classic_step(a, (make_kernel(10, size=SIZE),), kernels({}), 1.0, binary=True)
    assert set(np.unique(out)) <= {0.0, 1.0}
