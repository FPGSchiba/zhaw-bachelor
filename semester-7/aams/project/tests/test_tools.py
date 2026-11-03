import argparse
import csv
from types import SimpleNamespace

import numpy as np
import pytest

from lenia.experiment import crop_creature, evaluate
from lenia.patterns import init_state
from lenia.species import load_catalogue, save_catalogue
from lenia.world import DEFAULT_WORLD, apply_world
from tools import phase_map, search


def test_parse_axis():
    field, values = phase_map.parse_axis("mu:0.1:0.3:3")
    assert field == "mu" and np.allclose(values, [0.1, 0.2, 0.3])
    for bad in ("mu:0.1:0.3", "evil:0:1:3", "mu:a:b:3", "mu:0:1:1"):
        with pytest.raises(argparse.ArgumentTypeError):
            phase_map.parse_axis(bad)


def test_with_value_changes_kernel_or_world():
    world = apply_world(DEFAULT_WORLD, {})
    assert phase_map.with_value(world, 0, "sigma", 0.03)["kernels"][0]["sigma"] == 0.03
    assert phase_map.with_value(world, 0, "radius", 9.6)["radius"] == 10
    assert world["kernels"][0]["sigma"] == 0.015  # input untouched


def test_crop_creature_handles_wrap_around():
    a = np.zeros((1, 64, 64))
    a[0, 0:5, 60:64] = 1
    a[0, 0:5, 0:3] = 1  # one object split by the edge
    cells = crop_creature(a, margin=2)
    assert cells.shape == (1, 9, 11) and np.isclose(cells.sum(), a.sum())
    assert crop_creature(np.zeros((1, 64, 64))) is None


def test_small_sweep_writes_png_and_csv(tmp_path):
    world = apply_world(DEFAULT_WORLD, {"rule": "flow"})
    a0 = init_state(0, 13, 1, 64)
    x, y = phase_map.parse_axis("mu:0.1:0.2:2"), phase_map.parse_axis("sigma:0.01:0.05:2")
    results = phase_map.sweep(world, a0, x, y, 0, steps=20, workers=2)
    assert set(results) == {(0, 0), (0, 1), (1, 0), (1, 1)}
    phase_map.draw_map(results, x, y, "test", str(tmp_path / "m.png"))
    phase_map.write_csv(results, x, y, str(tmp_path / "m.csv"))
    with open(tmp_path / "m.csv") as f:
        rows = list(csv.reader(f))
    assert (tmp_path / "m.png").stat().st_size > 0 and rows[0][:3] == ["mu", "sigma", "outcome"] and len(rows) == 5


def test_evaluate_reports_conserved_mass_in_flow_mode():
    world = apply_world(DEFAULT_WORLD, {"rule": "flow"})
    result = evaluate(world, init_state(1, 13, 1, 64), steps=30, trace_steps=10)
    assert np.isclose(result["mass_ratio"], 1.0) and result["outcome"] != "dies"


def test_search_saves_loadable_creatures(tmp_path):
    out = tmp_path / "found.json"
    args = SimpleNamespace(rule="flow", channels=1, tries=4, keep=2, accept=["moving", "dynamic", "static"],
                           seed=0, radius=8, steps=40, size=64, workers=2, out=str(out))
    kept = search.search(args)
    assert kept, "with every localised outcome accepted, something should pass"
    save_catalogue(str(out), kept, "test")
    catalogue = load_catalogue(str(out))
    assert len(catalogue) == len(kept)
    assert all(entry["world"]["rule"] == "flow" for entry in catalogue.values())
