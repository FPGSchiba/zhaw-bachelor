import json
import os

import numpy as np
import pytest

from lenia.classic import classic_step
from lenia.metrics import snapshot, wrapped_distance
from lenia.patterns import place_pattern
from lenia.species import load_catalogue, parse_species, save_catalogue, to_json_entry
from lenia.world import GRID, clean_world, kernel_ffts
from tools.import_chan import decode_rle, default_channel_pairs, rle_value

CATALOGUE = os.path.join(os.path.dirname(__file__), "..", "species.json")


@pytest.fixture(scope="module")
def catalogue():
    return load_catalogue(CATALOGUE)


def test_catalogue_has_single_and_multi_channel_creatures(catalogue):
    assert len(catalogue) > 50 and "Orbium" in catalogue
    assert {e["world"]["channels"] for e in catalogue.values()} == {1, 2, 3}
    for entry in catalogue.values():
        assert entry["cells"].shape[0] == entry["world"]["channels"]


@pytest.mark.slow
def test_orbium_glides_and_keeps_its_size(catalogue):
    entry = catalogue["Orbium"]
    world = entry["world"]
    a = place_pattern(np.zeros((1, GRID, GRID)), entry["cells"], GRID // 2, GRID // 2)
    kf = kernel_ffts(world)
    start = snapshot(a)
    for _ in range(300):
        a = classic_step(a, kf, world["kernels"], world["dt"])
    end = snapshot(a)
    assert 0.7 < end["mass"] / start["mass"] < 1.3
    assert wrapped_distance(start["centroid"], end["centroid"], GRID) > 10


def test_json_round_trip(catalogue, tmp_path):
    entry = catalogue["Hydrogeminium natans"]
    path = tmp_path / "c.json"
    save_catalogue(str(path), {"x": to_json_entry(entry["world"], entry["cells"], "test")}, "note")
    again = load_catalogue(str(path))["x"]
    assert again["world"] == entry["world"] and np.allclose(again["cells"], entry["cells"], atol=1e-4)


def test_invalid_entries_are_skipped(tmp_path, capsys):
    world = clean_world({"channels": 1, "radius": 13, "kernels": ({"mu": 0.15},), "dt": 0.1})
    good = to_json_entry(world, np.ones((1, 2, 2)), "")
    bad = {**good, "cells": [[[2.0]]]}
    wrong_channels = {**good, "world": {**good["world"], "channels": 2}}
    path = tmp_path / "c.json"
    path.write_text(json.dumps({"species": {"good": good, "bad": bad, "wrong": wrong_channels}}))
    assert list(load_catalogue(str(path))) == ["good"]
    assert parse_species("x", {"cells": "nope"}) is None
    assert load_catalogue(str(tmp_path / "missing.json")) == {}


def test_rle_decoding():
    assert rle_value(".") == 0 and rle_value("o") == 1 and rle_value("yO") == 1
    assert np.isclose(rle_value("A"), 1 / 255)
    grid = decode_rle("2.yO$3yO$2$A!")
    assert grid.shape == (5, 3)
    assert np.allclose(grid[0], [0, 0, 1]) and np.allclose(grid[1], [1, 1, 1])
    assert grid[2:4].sum() == 0 and np.isclose(grid[4, 0], 1 / 255)


def test_default_channel_pairs_follow_chans_order():
    assert default_channel_pairs("212", 1) == [[0, 0], [0, 0]]
    assert default_channel_pairs("221", 2) == [[0, 0], [1, 1], [0, 1], [1, 0]]
