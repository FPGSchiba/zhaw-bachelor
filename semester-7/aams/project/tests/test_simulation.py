import csv

import numpy as np

from app.recorder import CsvRecorder
from app.simulation import Simulation
from lenia.species import load_catalogue

CAT = load_catalogue("species.json")


def sim(**params):
    return Simulation(params, CAT, rng=np.random.default_rng(0))


def test_loading_a_multi_channel_creature_resizes_the_state():
    s = sim()
    s.apply(("load", "222 #1"))
    assert s.a.shape[0] == 2 and len(s.kffts) == len(s.params["kernels"]) == 6
    s.step()
    assert s.step_count == 1 and s.stats["mass"] > 0


def test_changing_channels_pads_and_truncates():
    s = sim()
    s.apply(("set", {"channels": 3}))
    assert s.a.shape[0] == 3 and s.a[1:].sum() == 0
    s.apply(("set", {"channels": 1}))
    assert s.a.shape[0] == 1


def test_local_weights_exist_only_in_flow_mode():
    s = sim()
    s.apply(("set", {"local": True}))
    assert s.weights is None  # classic rule
    s.apply(("set", {"rule": "flow"}))
    assert s.weights.shape == (1, 256, 256) and np.allclose(s.weights, 1.0)
    s.apply(("add_kernel", None))
    assert s.weights.shape[0] == 2
    s.apply(("set", {"rule": "classic"}))
    assert s.weights is None


def test_painting_stamps_the_brush_weights():
    s = sim(rule="flow", local=True)
    s.apply(("clear", None))  # clear resets every cell to the current weights (h = 1)
    s.apply(("set_kernel", (0, {"h": 0.3})))  # the brush now carries h = 0.3
    s.paint(100, 100, radius=4)
    assert np.isclose(s.weights[0, 100, 100], 0.3) and np.isclose(s.weights[0, 10, 10], 1.0)
    assert s.a[0, 100, 100] >= 0.5


def test_flow_with_local_weights_and_mutation_conserves_mass():
    s = sim(rule="flow", local=True, mutation_rate=1.0)
    s.apply(("load", "Orbium"))
    s.apply(("random_weights", None))
    s.apply(("add", None))
    mass = s.a.sum()
    for _ in range(20):
        s.step()
    assert np.isclose(s.a.sum(), mass, rtol=1e-10)
    assert not np.allclose(s.weights, s.weights[:, :1, :1])  # mutations left their mark


def test_recorder_writes_one_row_per_step(tmp_path):
    s = sim()
    rec = CsvRecorder(str(tmp_path))
    path = rec.start()
    for _ in range(3):
        s.step()
        rec.write(s.step_count, s.params, s.stats)
    rec.stop()
    with open(path) as f:
        rows = list(csv.reader(f))
    assert rows[0][0] == "step" and len(rows) == 4 and rows[-1][0] == "3"
    rec.write(4, s.params, s.stats)  # writing after stop is a no-op
