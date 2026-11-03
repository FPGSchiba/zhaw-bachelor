"""Build species.json from Bert Wang-Chak Chan's Lenia catalogue (https://github.com/Chakazul/Lenia, MIT).

Sources (download them first, e.g. with `gh api repos/Chakazul/Lenia/contents/<path> -H "Accept: application/vnd.github.raw"`):
  Matlab/Lenia.m         single-channel creatures (Orbium, Hydrogeminium, ...)
  Python/found/2CK.json  multi-channel creatures (C channels), comma-separated JSON objects

Every creature is simulated with our classic rule and only kept if it survives;
single-channel ones that fail with Chan's native shapes are retried with exp/gauss.

usage: python -m tools.import_chan --matlab Lenia.m --found 222.json 233p.json ... --out species.json
"""
import argparse
import json
import os
import re
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction

import numpy as np

from lenia.experiment import evaluate
from lenia.patterns import place_pattern
from lenia.species import save_catalogue, to_json_entry
from lenia.world import GRID, MAX_CHANNELS, MAX_KERNELS, clean_world

CORES = {1: "poly", 2: "exp"}     # Chan's kernel types we support ("kn")
GROWTHS = {1: "poly", 2: "gauss"}  # Chan's growth types we support ("gn")
NOTE = ("Creatures from Bert Wang-Chak Chan's Lenia (https://github.com/Chakazul/Lenia, MIT licence), "
        "converted by tools/import_chan.py and verified to survive in this implementation.")


# ---------- decoding ----------
def rle_value(token):
    """Chan's cell encoding: '.'/'b' = 0, 'o' = 255, 'A'..'X' = 1..24, 'pA'..'yO' = 25..255; scaled to [0, 1]."""
    if token in (".", "b"):
        return 0.0
    if token == "o":
        return 1.0
    if len(token) == 1:
        return (ord(token) - ord("A") + 1) / 255
    return ((ord(token[0]) - ord("p")) * 24 + ord(token[1]) - ord("A") + 25) / 255


def decode_rle(st):
    """2D run-length encoding: '<count><value>' runs, '$' ends a row ('<count>$' adds empty rows), '!' ends."""
    rows, row, count, prefix = [], [], "", ""
    for ch in st.rstrip("!") + "$":
        if ch.isdigit():
            count += ch
        elif ch in "pqrstuvwxy":
            prefix = ch
        elif ch == "$":
            rows.append(row)
            rows.extend([] for _ in range(int(count or 1) - 1))
            row, count = [], ""
        else:
            row.extend([rle_value(prefix + ch)] * int(count or 1))
            prefix, count = "", ""
    width = max(len(r) for r in rows)
    return np.array([r + [0.0] * (width - len(r)) for r in rows])


def parse_matlab(path):
    """Single-channel creatures from Lenia.m (polynomial kernel and growth by default)."""
    found = {}
    with open(path) as f:
        lines = f.read().splitlines()
    for line in lines:
        s = line.strip()
        m = re.search(r"name='([^']+)'.*?R=(\d+);peaks=\[([^\]]+)\];mu=([\d.]+);sigma=([\d.]+);"
                      r"dt=([\d.]+);cells=\[([^\]]+)\]", s)
        if not m or "deltaType" in s:  # Vagopteron uses other kernel/growth types
            continue
        name, radius, peaks, mu, sigma, dt, cells = m.groups()
        if s.startswith("%") and name != "Orbium":
            continue
        name = name if s.startswith("%") or name != "Orbium" else "Orbium (variant)"
        if name in found:
            continue
        rings = [float(Fraction(p)) for p in peaks.split(",")]
        kernel = {"src": 0, "dst": 0, "r": 1.0, "rings": rings, "core": "poly", "growth": "poly",
                  "mu": float(mu), "sigma": float(sigma), "h": 1.0}
        grid = np.array([[float(v) for v in row.split(",")] for row in cells.split(";")])
        found[name] = ({"channels": 1, "radius": int(radius), "kernels": [kernel], "dt": float(dt)},
                       grid[None], "Chan, Matlab/Lenia.m")
    return found


def default_channel_pairs(code, channels):
    """Chan's implicit kernel order when a kernel has no "c" field (Board.set_channels in LeniaNDKC.py).

    File code "2CK[X]": K kernels per channel onto itself, then X (default 1) kernels per ordered
    pair of different channels.
    """
    digits = re.match(r"2(\d)(\d)(\d?)", code)
    if not digits:
        return []
    k, x = int(digits.group(2)), int(digits.group(3) or 1)
    own = [[c, c] for c in range(channels) for _ in range(k)]
    cross = [[c0, c1] for c0 in range(channels) for c1 in range(channels) if c0 != c1 for _ in range(x)]
    return own + cross


def parse_found(path):
    """Multi-channel creatures from a Python/found/*.json file (comma-separated JSON objects, as Chan reads them)."""
    code = os.path.splitext(os.path.basename(path))[0]
    found = {}
    try:
        with open(path) as f:
            entries = json.loads("[" + f.read().rstrip(", \n\r\t") + "]")
    except ValueError as err:
        print(f"skipping {path}: not valid JSON ({err})")
        return found
    for i, data in enumerate(e for e in entries if isinstance(e, dict) and "params" in e and "cells" in e):
        params, rle = data["params"], data["cells"]
        rle = rle if isinstance(rle, list) else [rle]
        if len(rle) > MAX_CHANNELS or len(params) > MAX_KERNELS or params[0].get("gn") not in GROWTHS:
            continue
        if any(p.get("kn") not in CORES for p in params):
            continue
        pairs = default_channel_pairs(code, len(rle))
        if any("c" not in p for p in params) and len(pairs) != len(params):
            continue
        params = [{**p, "c": p.get("c", pair)} for p, pair in zip(params, pairs)] if pairs else params
        kernels = [{"src": p["c"][0], "dst": p["c"][1], "r": float(p.get("r", 1)),
                    "rings": [float(Fraction(b)) for b in str(p["b"]).split(",")],
                    "core": CORES[p["kn"]], "growth": GROWTHS[params[0]["gn"]],
                    "mu": p["m"], "sigma": p["s"], "h": float(p.get("h", 1))} for p in params]
        channels = [decode_rle(r) for r in rle]
        h, w = max(c.shape[0] for c in channels), max(c.shape[1] for c in channels)
        cells = np.stack([np.pad(c, ((0, h - c.shape[0]), (0, w - c.shape[1]))) for c in channels])
        label = " ".join(x for x in (data.get("name", ""), data.get("cname", "")) if x and x != "object")
        name = f"{code} #{i + 1}" + (f" {label}" if label else "")
        found[name] = ({"channels": len(rle), "radius": int(params[0]["R"]), "kernels": kernels,
                        "dt": 1 / params[0].get("T", 10)}, cells, f"Chan, Python/found/{code}.json")
    return found


# ---------- verification ----------
def survives(world, cells, steps):
    """Run the classic rule; return the outcome if the creature stays alive and compact, else None."""
    world = clean_world({**world, "kernels": tuple(world["kernels"])})
    if cells.shape[1] > GRID // 2 or cells.shape[2] > GRID // 2 or world["radius"] > GRID // 4:
        return None
    a0 = place_pattern(np.zeros((world["channels"], GRID, GRID)), cells, GRID // 2, GRID // 2)
    result = evaluate(world, a0, steps)
    alive = result["outcome"] in ("moving", "static", "dynamic") and 0.2 < result["mass_ratio"] < 5
    compact = result["concentration"] > 0.5
    return result["outcome"] if alive and compact else None


def verify(item):
    name, (world, cells, source), steps = item
    outcome = survives(world, cells, steps)
    if outcome is None and world["channels"] == 1:  # retry with the other kernel/growth shapes
        alt = {**world, "kernels": [{**k, "core": "exp", "growth": "gauss"} for k in world["kernels"]]}
        outcome = survives(alt, cells, steps)
        world = alt if outcome else world
    return name, world, cells, source, outcome


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--matlab", help="path to Chan's Matlab/Lenia.m")
    parser.add_argument("--found", nargs="*", default=[], help="paths to Chan's Python/found/*.json files")
    parser.add_argument("--out", default="species.json")
    parser.add_argument("--steps", type=int, default=800, help="verification steps per creature")
    parser.add_argument("--per-file", type=int, default=12, help="max creatures taken from each found file")
    args = parser.parse_args()

    candidates = parse_matlab(args.matlab) if args.matlab else {}
    for path in args.found:
        candidates.update(dict(list(parse_found(path).items())[: args.per_file]))
    print(f"verifying {len(candidates)} creatures ({args.steps} steps each)")
    kept = {}
    with ProcessPoolExecutor() as pool:
        for name, world, cells, source, outcome in pool.map(verify, [(n, c, args.steps) for n, c in candidates.items()]):
            print(f"  {'keep' if outcome else 'drop'} {name:40s} {outcome or ''}")
            if outcome:
                kept[name] = to_json_entry(clean_world({**world, "kernels": tuple(world["kernels"])}), cells,
                                           f"{source}; classic rule: {outcome}")
    if os.path.exists(args.out):
        os.remove(args.out)  # rebuild from scratch
    save_catalogue(args.out, kept, NOTE)
    print(f"wrote {len(kept)} creatures to {args.out}")


if __name__ == "__main__":
    main()
