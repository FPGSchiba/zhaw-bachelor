"""Automatic creature search: random worlds, run headless, keep what moves.

For every try a random world is drawn (random kernels: rings, radius ratio, mu, sigma,
weight h and channel wiring, in the spirit of the Flow Lenia paper) and run from random
blobs. Runs whose outcome is accepted (default: "moving") are ranked; the best ones are
cut out of the grid, checked once more from the cut-out alone, and saved to
discovered.json, which the app loads next to species.json.

examples:
  python -m tools.search --rule flow --tries 200
  python -m tools.search --rule flow --channels 2 --tries 100 --keep 5
  python -m tools.search --rule classic --tries 300 --accept moving dynamic
"""
import argparse
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from lenia.experiment import crop_creature, evaluate
from lenia.metrics import OUTCOMES
from lenia.patterns import init_state, place_pattern
from lenia.species import save_catalogue, to_json_entry
from lenia.world import DEFAULT_WORLD, MAX_CHANNELS, RULES, apply_world, random_world

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTE = "Creatures found by tools/search.py (random worlds, kept if they move as one compact object)."


def make_world(seed, rule, channels, radius):
    world = random_world(np.random.default_rng(seed), channels, radius=radius)
    return apply_world({**DEFAULT_WORLD, "rule": rule}, world)


def score(result):
    """Higher is better: fast, compact movers first; for other outcomes, compact and active."""
    if result["outcome"] == "moving":
        return result["speed"] * result["concentration"]
    return result["activity"] * result["concentration"]


def try_seed(job):
    seed, rule, channels, radius, size, steps = job
    world = make_world(seed, rule, channels, radius)
    result = evaluate(world, init_state(seed, radius, channels, size), steps)
    return seed, world, result


def recheck(job):
    """Run the cut-out creature alone; returns the new result or None if it cannot be cut out."""
    seed, world, final, size, steps = job
    cells = crop_creature(final)
    if cells is None:
        return seed, None, None
    a0 = place_pattern(np.zeros((world["channels"], size, size)), cells, size // 2, size // 2)
    result = evaluate(world, a0, steps)
    return seed, cells, {k: v for k, v in result.items() if k != "final"}


def search(args):
    jobs = [(args.seed + i, args.rule, args.channels, args.radius, args.size, args.steps) for i in range(args.tries)]
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(try_seed, jobs, chunksize=2))
        counts = {name: sum(r["outcome"] == name for _, _, r in results) for name in OUTCOMES}
        print("outcomes of the random worlds:", ", ".join(f"{k} {v}" for k, v in counts.items()))
        hits = sorted((r for r in results if r[2]["outcome"] in args.accept), key=lambda r: -score(r[2]))
        shortlist = hits[: args.keep * 2]  # some will fail the re-check
        checks = list(pool.map(recheck, [(s, w, r["final"], args.size, args.steps) for s, w, r in shortlist]))
    worlds = {seed: world for seed, world, _ in shortlist}
    kept = {}
    for seed, cells, result in checks:
        if result is None or result["outcome"] not in args.accept or len(kept) >= args.keep:
            continue
        name = f"found {args.rule} {args.channels}ch #{seed}"
        source = (f"tools/search.py seed {seed}: {result['outcome']}, speed {result['speed']:.3f}, "
                  f"concentration {result['concentration']:.2f}")
        kept[name] = to_json_entry(worlds[seed], cells, source, with_rule=True)
        print(f"  keep {name:28s} {result['outcome']:8s} speed {result['speed']:.3f} "
              f"concentration {result['concentration']:.2f} size {cells.shape[1]}x{cells.shape[2]}")
    return kept


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--rule", choices=RULES, default="flow")
    parser.add_argument("--channels", type=int, choices=range(1, MAX_CHANNELS + 1), default=1)
    parser.add_argument("--tries", type=int, default=200)
    parser.add_argument("--keep", type=int, default=10, help="how many creatures to save at most")
    parser.add_argument("--accept", nargs="+", choices=OUTCOMES, default=["moving"])
    parser.add_argument("--seed", type=int, default=0, help="first seed; tries use seed, seed+1, ...")
    parser.add_argument("--radius", type=int, default=13)
    parser.add_argument("--steps", type=int, default=600)
    parser.add_argument("--size", type=int, default=128, help="grid size (smaller = faster)")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--out", default=os.path.join(HERE, "discovered.json"))
    args = parser.parse_args()
    if args.tries < 1 or args.keep < 1:
        parser.error("--tries and --keep must be positive")

    print(f"{args.tries} random {args.rule} worlds with {args.channels} channel(s), {args.steps} steps each")
    kept = search(args)
    if kept:
        save_catalogue(args.out, kept, NOTE)
        print(f"saved {len(kept)} creatures to {args.out} (the app loads them on start)")
    else:
        print("nothing passed; try more --tries or --accept moving dynamic")


if __name__ == "__main__":
    main()
