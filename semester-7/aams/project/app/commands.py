"""Commands from the keyboard and the control panel, applied to the app state.

The app state ("params") is a plain dict: the world (see lenia.world) plus app-only
fields such as paused, seed, the selected kernel and the view. Every command returns
a new dict and an optional action for the main loop; nothing is mutated in place.
"""
import time

import numpy as np

from lenia.world import DEFAULT_WORLD, MAX_KERNELS, RULES, apply_world, clamp, number, random_world

SEED_MAX = 2**31 - 1
VIEWS = ("mass", "channels", "species")
MIX_RULES = ("stoch", "avg")
APP_LIMITS = {"mutation_rate": (0.0, 1.0), "mutation_scale": (0.01, 1.0)}
APP_DEFAULTS = {"paused": False, "seed": 0, "species": None, "selected": 0, "view": "mass",
                "local": False, "mix": "stoch", "mutation_rate": 0.0, "mutation_scale": 0.2, "recording": False}
DEFAULTS = {**DEFAULT_WORLD, **APP_DEFAULTS}

WORLD_FIELDS = ("channels", "radius", "rule", "dt", "flow_dt", "theta", "binary")
KERNEL_FIELDS = ("src", "dst", "r", "rings", "core", "growth", "mu", "sigma", "h")


def with_kernel(params, index, fields):
    """Params with kernel `index` updated by `fields` (validated by apply_world)."""
    kernels = tuple({**k, **fields} if i == index else k for i, k in enumerate(params["kernels"]))
    return apply_world(params, {"kernels": kernels})


def set_fields(params, value):
    """The "set" command: world fields are validated by the world, app fields here."""
    world = {k: v for k, v in value.items() if k in WORLD_FIELDS}
    app = {}
    if value.get("view") in VIEWS:
        app["view"] = value["view"]
    if value.get("mix") in MIX_RULES:
        app["mix"] = value["mix"]
    if "local" in value:
        app["local"] = bool(value["local"])
    for key, limits in APP_LIMITS.items():
        if key in value:
            app[key] = round(clamp(number(value[key], params[key]), limits), 4)
    if world.get("rule") not in (None, *RULES):
        world.pop("rule")
    return apply_world({**params, **app}, world)


def apply_command(params, cmd, catalogue):
    """Apply one (name, value) command; returns (new_params, action).

    Actions for the main loop: None, "reset" (random blobs), "load" (place the species
    alone), "add" (one more creature), "step" (one step while paused), "clear" (empty grid),
    "structure" (kernels added/removed/replaced: per-cell weights must be rebuilt), "record".
    Malformed commands are reported and ignored, so a bad message can't stop the simulation.
    """
    try:
        return dispatch(params, cmd, catalogue)
    except (TypeError, ValueError, KeyError, IndexError, AttributeError) as err:
        print(f"ignoring malformed command {cmd!r}: {err}")
        return params, None


def dispatch(params, cmd, catalogue):
    name, value = cmd
    selected = params["selected"]
    if name == "set":
        return set_fields(params, value), None
    if name == "set_kernel":
        index, fields = value
        if 0 <= index < len(params["kernels"]):
            return with_kernel(params, index, {f: v for f, v in fields.items() if f in KERNEL_FIELDS}), None
    elif name == "select_kernel" and 0 <= value < len(params["kernels"]):
        return {**params, "selected": int(value)}, None
    elif name == "add_kernel" and len(params["kernels"]) < MAX_KERNELS:
        new = apply_world(params, {"kernels": params["kernels"] + (params["kernels"][selected],)})
        return {**new, "selected": len(new["kernels"]) - 1}, "structure"
    elif name == "remove_kernel" and len(params["kernels"]) > 1:
        kernels = tuple(k for i, k in enumerate(params["kernels"]) if i != selected)
        return {**apply_world(params, {"kernels": kernels}), "selected": max(0, selected - 1)}, "structure"
    elif name == "nudge":
        key, delta = value
        if key == "radius":
            return apply_world(params, {"radius": params["radius"] + delta}), None
        if key in ("mu", "sigma", "h"):
            return with_kernel(params, selected, {key: params["kernels"][selected][key] + delta}), None
    elif name in ("run", "pause", "toggle_pause"):
        paused = name == "pause" or (name == "toggle_pause" and not params["paused"])
        return {**params, "paused": paused}, None
    elif name == "toggle_binary":
        return apply_world(params, {"binary": not params["binary"]}), None
    elif name == "toggle_rule":
        return apply_world(params, {"rule": "flow" if params["rule"] == "classic" else "classic"}), None
    elif name == "cycle_view":
        return {**params, "view": VIEWS[(VIEWS.index(params["view"]) + 1) % len(VIEWS)]}, None
    elif name == "step":
        return {**params, "paused": True}, "step"
    elif name == "reset":
        seed = int(time.time_ns() % SEED_MAX) if value == "random" else int(value)
        return {**params, "seed": int(clamp(seed, (0, SEED_MAX))), "species": None}, "reset"
    elif name == "clear":
        return {**params, "species": None}, "clear"
    elif name == "load" and value in catalogue:
        world = catalogue[value]["world"]
        new = apply_world(params, {**world, "binary": False})
        return {**new, "species": value, "selected": 0}, "load"
    elif name == "add" and catalogue:
        return params, "add"
    elif name == "random_world":
        seed = int(time.time_ns() % SEED_MAX) if value in (None, "random") else int(value)
        world = random_world(np.random.default_rng(seed), params["channels"], radius=params["radius"])
        return {**apply_world(params, world), "selected": 0, "species": None}, "structure"
    elif name == "random_weights":
        rng = np.random.default_rng()
        kernels = tuple({**k, "h": float(rng.uniform(0.05, 1.0))} for k in params["kernels"])
        return apply_world(params, {"kernels": kernels}), None
    elif name == "toggle_record":
        return {**params, "recording": not params["recording"]}, "record"
    print(f"ignoring command {cmd!r}")
    return params, None
