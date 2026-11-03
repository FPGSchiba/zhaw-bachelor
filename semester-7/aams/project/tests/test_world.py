import numpy as np

from lenia.world import (
    DEFAULT_WORLD,
    MAX_KERNELS,
    apply_world,
    clean_kernel,
    clean_world,
    kernel_ffts,
    random_world,
    valid_rings,
)


def test_clean_kernel_clamps_and_falls_back():
    k = clean_kernel({"mu": 5, "sigma": -1, "h": 2, "src": 7, "dst": -3, "core": "evil", "rings": [0, 0],
                      "unknown": 1}, channels=2, radius=13)
    assert k["mu"] == 0.5 and k["sigma"] == 0.001 and k["h"] == 1.0
    assert k["src"] == 1 and k["dst"] == 0
    assert k["core"] == "exp" and k["rings"] == (1.0,) and "unknown" not in k


def test_effective_radius_never_below_two_cells():
    assert clean_kernel({"r": 0.1}, channels=1, radius=10)["r"] == 0.2


def test_clean_world_limits_and_flow_disables_binary():
    w = clean_world({**DEFAULT_WORLD, "channels": 9, "radius": 1000, "rule": "quantum", "binary": True})
    assert w["channels"] == 3 and w["radius"] == 127 and w["rule"] == "classic" and w["binary"]
    assert not clean_world({**w, "rule": "flow"})["binary"]
    many = clean_world({**DEFAULT_WORLD, "kernels": DEFAULT_WORLD["kernels"] * 40})
    assert len(many["kernels"]) == MAX_KERNELS


def test_apply_world_does_not_mutate_input():
    params = dict(DEFAULT_WORLD)
    out = apply_world(params, {"radius": 20})
    assert out["radius"] == 20 and params["radius"] == 13


def test_valid_rings():
    assert valid_rings([0.5, 0.25]) == (0.5, 0.25)
    for bad in ([0, 0], [1] * 5, [0.5, 2], ["x"], []):
        assert valid_rings(bad) is None


def test_random_world_is_valid_and_feeds_every_channel():
    for seed in range(20):
        world = random_world(np.random.default_rng(seed), channels=3)
        clean = clean_world({**DEFAULT_WORLD, **world})
        assert clean["kernels"] == tuple(clean_kernel(k, 3, 13) for k in world["kernels"])
        assert {k["dst"] for k in clean["kernels"]} == {0, 1, 2}
        assert len(kernel_ffts(clean, size=64)) == len(clean["kernels"])


def test_non_numeric_values_fall_back_to_defaults():
    k = clean_kernel({"mu": "x", "sigma": float("nan"), "src": "?", "h": None}, channels=2, radius=13)
    assert k["mu"] == 0.15 and k["sigma"] == 0.015 and k["src"] == 0 and k["h"] == 1.0
    w = clean_world({**DEFAULT_WORLD, "theta": "abc", "radius": float("inf"), "channels": "two"})
    assert w["theta"] == 1.0 and w["radius"] == 13 and w["channels"] == 1
