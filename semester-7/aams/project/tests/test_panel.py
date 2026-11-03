"""Control panel against fake queues (opens a real, briefly visible Tk window)."""
import queue

import numpy as np
import pytest

from app.commands import DEFAULTS, apply_command
from lenia.species import load_catalogue

tk = pytest.importorskip("tkinter")
pytestmark = pytest.mark.gui
CAT = load_catalogue("species.json")


@pytest.fixture
def panel():
    from app.panel import ControlPanel
    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display")
    cmd_q, state_q = queue.Queue(), queue.Queue()
    p = ControlPanel(root, cmd_q, state_q, dict(DEFAULTS), list(CAT))
    yield p, root, cmd_q, state_q
    root.destroy()


def drain(root, cmd_q):
    root.update()
    out = []
    while not cmd_q.empty():
        out.append(cmd_q.get())
    return out


def state(params):
    stats = {"mass": 1.0, "live": 1, "speed": 0.0, "activity": 0.0, "concentration": 1.0}
    return {**params, "step": 1, "fps": 30.0, "stats": stats, "record_path": None}


def test_startup_and_sync_send_nothing(panel):
    p, root, cmd_q, state_q = panel
    assert drain(root, cmd_q) == []
    loaded, _ = apply_command(dict(DEFAULTS), ("load", "Rotorbium"), CAT)  # sigma 0.0224
    state_q.put(state(loaded))
    p.poll()
    p.on_kernel_scale("sigma", str(p.kernel_vars["sigma"].get()))
    p.on_world_scale("dt", str(p.world_vars["dt"].get()))
    p.on_rings()
    assert drain(root, cmd_q) == []
    assert p.kernel_vars["sigma"].get() == 0.0224


def test_multi_kernel_sync_and_editing(panel):
    p, root, cmd_q, state_q = panel
    loaded, _ = apply_command(dict(DEFAULTS), ("load", "231 #9 nexus"), CAT)
    loaded = {**loaded, "selected": 4}
    state_q.put(state(loaded))
    p.poll()
    assert p.kernel_list.size() == 9 and p.kernel_list.curselection() == (4,)
    assert drain(root, cmd_q) == []
    p.on_kernel_scale("mu", "0.2")
    p.ring_count.set(1)
    p.ring_vars[0].set(0.5)
    p.on_rings()
    assert drain(root, cmd_q) == [("set_kernel", (4, {"mu": 0.2})), ("set_kernel", (4, {"rings": [0.5]}))]


def test_plots_receive_every_state(panel):
    p, _, _, state_q = panel
    for mass in (1.0, 2.0, 3.0):
        s = state(DEFAULTS)
        state_q.put({**s, "stats": {**s["stats"], "mass": mass}})
    p.poll()
    assert p.sparks["mass"].values[-3:] == [1.0, 2.0, 3.0]
    p.clear_plots()
    assert p.sparks["mass"].values == []


def test_invalid_seed_is_rejected(panel):
    p, root, cmd_q, _ = panel
    p.seed_var.set("abc")
    p.reset()
    assert drain(root, cmd_q) == [] and p.error.cget("text")
    p.seed_var.set("42")
    p.reset()
    assert drain(root, cmd_q) == [("reset", 42)]


def test_species_view_colours_by_weights():
    from app.render import colourise, make_palette
    a = np.ones((1, 4, 4))
    w = np.concatenate([np.zeros((1, 4, 2)), np.ones((1, 4, 2))], axis=2)
    img = colourise(a, "species", make_palette(), w)
    assert img.shape == (4, 4, 3) and not np.array_equal(img[0, 0], img[0, 3])
