"""Phase map: sweep two parameters, run every combination headless and colour each cell by its outcome.

Outcomes (lenia.metrics.classify): dies, fills, pattern (spots/stripes over the whole grid),
static (a still object), moving (one compact travelling object), dynamic (a localised object
that keeps changing: oscillating, rotating, splitting).

Axes are "field:start:stop:count". Kernel fields (mu, sigma, h, r) change kernel --kernel;
world fields (theta, flow_dt, dt, radius) change the whole world.

examples:
  python -m tools.phase_map --rule classic --x mu:0.05:0.35:24 --y sigma:0.005:0.06:24
  python -m tools.phase_map --rule flow --x mu:0.05:0.35:24 --y sigma:0.005:0.06:24
  python -m tools.phase_map --species Orbium --x mu:0.12:0.18:20 --y sigma:0.008:0.025:20
"""
import argparse
import csv
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

from lenia.experiment import evaluate
from lenia.metrics import OUTCOMES
from lenia.patterns import init_state, place_pattern
from lenia.species import load_catalogue
from lenia.world import DEFAULT_WORLD, RULES, apply_world

KERNEL_AXES = ("mu", "sigma", "h", "r")
WORLD_AXES = ("theta", "flow_dt", "dt", "radius")
COLOURS = {"dies": (45, 45, 50), "fills": (230, 110, 40), "pattern": (150, 150, 160), "static": (60, 110, 220),
           "moving": (60, 200, 90), "dynamic": (170, 80, 210)}
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_axis(text):
    try:
        field, start, stop, count = text.split(":")
        values = np.linspace(float(start), float(stop), int(count))
    except ValueError as err:
        raise argparse.ArgumentTypeError(f"axis must be field:start:stop:count, got {text!r}") from err
    if field not in KERNEL_AXES + WORLD_AXES:
        raise argparse.ArgumentTypeError(f"unknown axis field {field!r}; use one of {KERNEL_AXES + WORLD_AXES}")
    if int(count) < 2:
        raise argparse.ArgumentTypeError("an axis needs at least 2 values")
    return field, values


def with_value(world, kernel, field, value):
    if field in KERNEL_AXES:
        kernels = tuple({**k, field: value} if i == kernel else k for i, k in enumerate(world["kernels"]))
        return apply_world(world, {"kernels": kernels})
    return apply_world(world, {field: round(value) if field == "radius" else value})


def run_cell(job):
    (ix, iy), world, a0, steps = job
    result = evaluate(world, a0, steps)
    return ix, iy, {k: v for k, v in result.items() if k != "final"}


def sweep(world, a0, x_axis, y_axis, kernel, steps, workers=None):
    """Evaluate every (x, y) combination; returns {(ix, iy): result}."""
    jobs = []
    for ix, xv in enumerate(x_axis[1]):
        for iy, yv in enumerate(y_axis[1]):
            w = with_value(with_value(world, kernel, x_axis[0], xv), kernel, y_axis[0], yv)
            jobs.append(((ix, iy), w, a0, steps))
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return {(ix, iy): r for ix, iy, r in pool.map(run_cell, jobs, chunksize=4)}


def draw_map(results, x_axis, y_axis, title, path, cell=18):
    """Save the map as a PNG: x to the right, y upwards, with axis ticks and a legend."""
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    import pygame
    pygame.font.init()
    font = pygame.font.SysFont("menlo,consolas,monospace", 13)
    nx, ny = len(x_axis[1]), len(y_axis[1])
    left, top, bottom, legend = 80, 36, 56, 130
    surf = pygame.Surface((left + nx * cell + legend, top + ny * cell + bottom))
    surf.fill((250, 250, 248))
    for (ix, iy), r in results.items():
        rect = (left + ix * cell, top + (ny - 1 - iy) * cell, cell - 1, cell - 1)
        pygame.draw.rect(surf, COLOURS[r["outcome"]], rect)
    def text(s, pos):
        surf.blit(font.render(s, True, (30, 30, 30)), pos)

    text(title, (left, 10))
    for ix in range(0, nx, max(1, nx // 6)):
        text(f"{x_axis[1][ix]:.3g}", (left + ix * cell, top + ny * cell + 4))
    for iy in range(0, ny, max(1, ny // 6)):
        text(f"{y_axis[1][iy]:.3g}", (8, top + (ny - 1 - iy) * cell + 2))
    text(f"{x_axis[0]} ->", (left + nx * cell // 2 - 20, top + ny * cell + 24))
    text(f"{y_axis[0]}", (8, top - 18))
    for i, name in enumerate(OUTCOMES):
        y = top + i * 22
        pygame.draw.rect(surf, COLOURS[name], (left + nx * cell + 16, y, 14, 14))
        text(name, (left + nx * cell + 36, y))
    pygame.image.save(surf, path)


def write_csv(results, x_axis, y_axis, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([x_axis[0], y_axis[0], "outcome", "mass_ratio", "speed", "activity", "concentration"])
        for (ix, iy), r in sorted(results.items()):
            writer.writerow([f"{x_axis[1][ix]:.5g}", f"{y_axis[1][iy]:.5g}", r["outcome"], f"{r['mass_ratio']:.4f}",
                             f"{r['speed']:.4f}", f"{r['activity']:.5f}", f"{r['concentration']:.3f}"])


def start_state(args, catalogue):
    """(world, a0) from --species (its world and cells) or the default world with random blobs."""
    if args.species:
        entry = catalogue[args.species]
        world = apply_world({**DEFAULT_WORLD, "rule": args.rule}, entry["world"])
        empty = np.zeros((world["channels"], args.size, args.size))
        return world, place_pattern(empty, entry["cells"], args.size // 2, args.size // 2)
    world = apply_world(DEFAULT_WORLD, {"rule": args.rule})
    return world, init_state(args.seed, world["radius"], world["channels"], args.size)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--x", type=parse_axis, default="mu:0.05:0.35:24")
    parser.add_argument("--y", type=parse_axis, default="sigma:0.005:0.06:24")
    parser.add_argument("--rule", choices=RULES, default="classic")
    parser.add_argument("--species", help="start from this creature (and its world) instead of random blobs")
    parser.add_argument("--kernel", type=int, default=0, help="which kernel the kernel axes change")
    parser.add_argument("--seed", type=int, default=0, help="seed of the random-blob start state")
    parser.add_argument("--steps", type=int, default=600)
    parser.add_argument("--size", type=int, default=128, help="grid size (smaller = faster)")
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--out", default="maps/phase_map", help="output path without extension")
    args = parser.parse_args()

    catalogue = load_catalogue(os.path.join(HERE, "species.json"), os.path.join(HERE, "discovered.json"))
    if args.species and args.species not in catalogue:
        parser.error(f"unknown species {args.species!r}")
    world, a0 = start_state(args, catalogue)
    if not 0 <= args.kernel < len(world["kernels"]):
        parser.error(f"--kernel must be in [0, {len(world['kernels']) - 1}]")
    x_axis, y_axis = args.x, args.y
    print(f"{len(x_axis[1]) * len(y_axis[1])} runs x {args.steps} steps, rule {world['rule']}, "
          f"grid {args.size}, start {args.species or 'seed ' + str(args.seed)}")
    results = sweep(world, a0, x_axis, y_axis, args.kernel, args.steps, args.workers)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    title = f"{world['rule']} Lenia, start: {args.species or 'random blobs (seed ' + str(args.seed) + ')'}"
    draw_map(results, x_axis, y_axis, title, args.out + ".png")
    write_csv(results, x_axis, y_axis, args.out + ".csv")
    counts = {name: sum(r["outcome"] == name for r in results.values()) for name in OUTCOMES}
    print("outcomes:", ", ".join(f"{k} {v}" for k, v in counts.items()))
    print(f"wrote {args.out}.png and {args.out}.csv")


if __name__ == "__main__":
    main()
