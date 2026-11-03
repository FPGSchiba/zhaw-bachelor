"""Creature catalogue: JSON files mapping a name to a world (channels, radius, kernels, dt) and its cells.

Format: {"_source": "...", "species": {name: {"world": {...}, "cells": [channel][row][col], "source": "..."}}}
"""
import json
import os

import numpy as np

from lenia.world import MAX_CHANNELS, clean_world

WORLD_FIELDS = ("channels", "radius", "kernels", "dt")
OPTIONAL_FIELDS = ("rule", "theta", "flow_dt")  # stored only for creatures that need them (e.g. found in flow mode)


def load_catalogue(*paths):
    """Read and validate one or more catalogue files; returns {name: {"world", "cells", "source"}}.

    Missing files are skipped quietly (the search results file may not exist yet);
    unreadable files and invalid entries are reported and skipped.
    """
    catalogue = {}
    for path in paths:
        if not os.path.exists(path):
            continue
        try:
            with open(path) as f:
                raw = json.load(f)["species"]
        except (OSError, ValueError, KeyError) as err:
            print(f"could not load species from {path}: {err}")
            continue
        for name, spec in raw.items():
            entry = parse_species(name, spec)
            if entry is None:
                print(f"skipping invalid species {name!r} in {path}")
            else:
                catalogue[name] = entry
    return catalogue


def parse_species(name, spec):
    try:
        cells = np.asarray(spec["cells"], dtype=float)
        world = spec["world"]
    except (KeyError, TypeError, ValueError):
        return None
    if cells.ndim != 3 or cells.size == 0 or cells.min() < 0 or cells.max() > 1:
        return None
    if not 1 <= cells.shape[0] <= MAX_CHANNELS or world.get("channels") != cells.shape[0]:
        return None
    clean = clean_world({**world, "kernels": tuple(world.get("kernels", ()))})
    fields = WORLD_FIELDS + tuple(f for f in OPTIONAL_FIELDS if f in world)
    return {"world": {f: clean[f] for f in fields}, "cells": cells, "source": spec.get("source", "")}


def to_json_entry(world, cells, source, with_rule=False):
    """Serialisable catalogue entry (inverse of parse_species).

    with_rule=True also stores rule, theta and flow_dt, so loading the creature switches to that rule.
    """
    kernels = [{**k, "rings": list(k["rings"])} for k in world["kernels"]]
    fields = WORLD_FIELDS + (OPTIONAL_FIELDS if with_rule else ())
    return {"world": {**{f: world[f] for f in fields}, "kernels": kernels},
            "cells": np.round(np.asarray(cells), 4).tolist(), "source": source}


def save_catalogue(path, entries, note):
    """Write {name: to_json_entry(...)} to `path`, merging with what is already there."""
    existing = {}
    if os.path.exists(path):
        with open(path) as f:
            existing = json.load(f).get("species", {})
    with open(path, "w") as f:
        json.dump({"_source": note, "species": {**existing, **entries}}, f, separators=(",", ":"))
