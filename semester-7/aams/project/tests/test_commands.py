import pytest

from app.commands import DEFAULTS, apply_command
from lenia.species import load_catalogue
from lenia.world import MAX_KERNELS

CAT = load_catalogue("species.json")


def run(params, *cmds):
    actions = []
    for cmd in cmds:
        params, action = apply_command(params, cmd, CAT)
        actions.append(action)
    return params, actions


def test_set_validates_world_and_app_fields():
    p, _ = run(dict(DEFAULTS), ("set", {"theta": 99, "view": "species", "mix": "bogus", "mutation_rate": 2,
                                        "rule": "quantum", "channels": 2}))
    assert p["theta"] == 3.0 and p["view"] == "species" and p["mix"] == "stoch"
    assert p["mutation_rate"] == 1.0 and p["rule"] == "classic" and p["channels"] == 2


def test_kernel_editing_targets_the_selected_kernel():
    p, actions = run(dict(DEFAULTS), ("add_kernel", None), ("set_kernel", (1, {"mu": 0.3, "evil": 1})),
                     ("nudge", ("sigma", 0.001)))
    assert actions[0] == "structure" and p["selected"] == 1
    assert p["kernels"][0]["mu"] == 0.15 and p["kernels"][1]["mu"] == 0.3
    assert p["kernels"][1]["sigma"] == 0.016 and "evil" not in p["kernels"][1]


def test_remove_keeps_at_least_one_kernel_and_add_respects_limit():
    p, _ = run(dict(DEFAULTS), ("remove_kernel", None))
    assert len(p["kernels"]) == 1
    p, _ = run(p, *[("add_kernel", None)] * (MAX_KERNELS + 3))
    assert len(p["kernels"]) == MAX_KERNELS


def test_load_sets_the_whole_world_but_keeps_the_rule():
    p, actions = run({**DEFAULTS, "rule": "flow"}, ("load", "231 #9 nexus"))
    assert actions == ["load"] and p["channels"] == 3 and p["rule"] == "flow" and len(p["kernels"]) == 9


def test_flow_rule_switches_binary_off():
    p, _ = run({**DEFAULTS, "binary": True}, ("toggle_rule", None), ("toggle_binary", None))
    assert p["rule"] == "flow" and p["binary"] is False


@pytest.mark.parametrize("cmd,action", [(("reset", 5), "reset"), (("clear", None), "clear"),
                                        (("step", None), "step"), (("add", None), "add"),
                                        (("random_world", 3), "structure"), (("toggle_record", None), "record")])
def test_actions(cmd, action):
    assert run(dict(DEFAULTS), cmd)[1] == [action]


def test_unknown_commands_change_nothing(capsys):
    p, actions = run(dict(DEFAULTS), ("bogus", 1), ("load", "Nope"), ("select_kernel", 5))
    assert p == DEFAULTS and actions == [None, None, None]


def test_random_world_is_reproducible_and_keeps_channels():
    a, _ = run({**DEFAULTS, "channels": 2}, ("random_world", 7))
    b, _ = run({**DEFAULTS, "channels": 2}, ("random_world", 7))
    assert a["kernels"] == b["kernels"] and a["channels"] == 2


@pytest.mark.parametrize("cmd", [("set_kernel", 5), ("select_kernel", "x"), ("reset", "abc"), ("nudge", 3),
                                 ("set", None), "not a tuple", ("set_kernel", (0, None))])
def test_malformed_commands_are_ignored(cmd):
    assert run(dict(DEFAULTS), cmd) == (DEFAULTS, [None])
