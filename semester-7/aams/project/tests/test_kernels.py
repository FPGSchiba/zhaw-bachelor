import numpy as np
import pytest

from lenia.kernels import growth, kernel_shell, make_kernel


@pytest.mark.parametrize("rings", [(1.0,), (0.5, 1, 2 / 3), (1, 0, 1), (1, 1 / 3, 2 / 3, 1)])
@pytest.mark.parametrize("core", ["exp", "poly"])
@pytest.mark.parametrize("radius", [13, 7.5, 2.0])
def test_kernel_sums_to_one_and_is_symmetric(rings, core, radius):
    kernel = np.fft.irfft2(make_kernel(radius, rings, core, size=64), s=(64, 64))
    assert np.isclose(kernel.sum(), 1.0)
    centred = np.roll(kernel, (32, 32), axis=(0, 1))
    assert np.allclose(centred[1:, 1:], centred[1:, 1:][::-1, ::-1], atol=1e-12)


def test_single_ring_matches_original_formula():
    r = np.linspace(0.001, 0.999, 500)
    expected = np.exp(4 - 1 / (r * (1 - r)))
    assert np.allclose(kernel_shell(r, (1.0,), "exp"), expected)


def test_ring_peaks_sit_in_the_middle_of_their_bands():
    r = np.linspace(0, 0.999, 3000)
    shell = kernel_shell(r, (0.5, 1, 2 / 3), "poly")
    peaks = [r[np.argmax(np.where((r >= i / 3) & (r < (i + 1) / 3), shell, 0))] for i in range(3)]
    assert np.allclose(peaks, [1 / 6, 3 / 6, 5 / 6], atol=2e-3)
    assert np.isclose(shell.max(), 1.0, atol=1e-3)


@pytest.mark.parametrize("kind", ["gauss", "poly"])
def test_growth_is_one_at_mu_and_minus_one_far_away(kind):
    assert np.isclose(growth(0.2, 0.2, 0.02, kind), 1.0)
    assert np.isclose(growth(0.9, 0.2, 0.02, kind), -1.0)


def test_invalid_kernels_are_rejected():
    with pytest.raises(ValueError):
        make_kernel(13, (0, 0))
    with pytest.raises(ValueError):
        make_kernel(40, size=64)
