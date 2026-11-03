"""World configuration: channels, kernels and global settings, as plain (picklable) dicts.

A world has 1-3 channels (state layers) and one or more kernels. Every kernel reads
one channel (`src`), applies its own ring shape and growth function, and writes
into one channel (`dst`) with weight `h`:

    classic:  A_dst += dt * sum_k h_k G_k(K_k * A_src) / sum_k h_k     (Chan 2020)
    flow:     U_dst  =      sum_k h_k G_k(K_k * A_src)                  (Plantec et al. 2023)

All updates return new dicts; nothing is mutated in place.
"""
import numpy as np

from lenia.kernels import GROWTH_KINDS, KERNEL_CORES, make_kernel

GRID = 256
MAX_CHANNELS = 3
MAX_KERNELS = 16
MAX_RINGS = 4
RULES = ("classic", "flow")

KERNEL_LIMITS = {"r": (0.1, 1.0), "mu": (0.001, 0.5), "sigma": (0.001, 0.2), "h": (0.0, 1.0)}
WORLD_LIMITS = {"radius": (3, GRID // 2 - 1), "dt": (0.01, 1.0), "flow_dt": (0.05, 1.0), "theta": (0.1, 3.0)}

DEFAULT_KERNEL = {"src": 0, "dst": 0, "r": 1.0, "rings": (1.0,), "core": "exp", "growth": "gauss",
                  "mu": 0.15, "sigma": 0.015, "h": 1.0}
DEFAULT_WORLD = {"channels": 1, "radius": 13, "kernels": (DEFAULT_KERNEL,), "rule": "classic",
                 "dt": 0.1, "flow_dt": 0.2, "theta": 1.0, "binary": False}


def clamp(value, limits):
    lo, hi = limits
    return min(max(value, lo), hi)


def number(value, default):
    """float(value) if it is a finite number, else `default` (values arrive from the UI and from files)."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        return float(default)
    return value if np.isfinite(value) else float(default)


def valid_rings(rings):
    """Ring weights as a rounded tuple, or None if they don't form a usable kernel."""
    try:
        rings = tuple(round(float(w), 4) for w in rings)
    except (TypeError, ValueError):
        return None
    ok = 1 <= len(rings) <= MAX_RINGS and all(0 <= w <= 1 for w in rings) and any(w > 0 for w in rings)
    return rings if ok else None


def clean_kernel(kernel, channels, radius):
    """Return a validated copy of `kernel`; invalid fields fall back to the defaults.

    The effective radius R * r is kept at >= 2 cells so the kernel is never degenerate.
    """
    k = {**DEFAULT_KERNEL, **{f: v for f, v in kernel.items() if f in DEFAULT_KERNEL}}
    rings = valid_rings(k["rings"]) or DEFAULT_KERNEL["rings"]
    numeric = {f: round(clamp(number(k[f], DEFAULT_KERNEL[f]), KERNEL_LIMITS[f]), 4) for f in KERNEL_LIMITS}
    numeric = {**numeric, "r": max(numeric["r"], round(2 / radius, 4))}
    return {
        **numeric, "rings": rings,
        "src": int(clamp(number(k["src"], 0), (0, channels - 1))),
        "dst": int(clamp(number(k["dst"], 0), (0, channels - 1))),
        "core": k["core"] if k["core"] in KERNEL_CORES else DEFAULT_KERNEL["core"],
        "growth": k["growth"] if k["growth"] in GROWTH_KINDS else DEFAULT_KERNEL["growth"],
    }


def clean_world(world):
    """Validated copy of a world dict (unknown keys are kept, e.g. app state like 'paused')."""
    channels = int(clamp(number(world.get("channels", 1), 1), (1, MAX_CHANNELS)))
    radius = int(clamp(number(world.get("radius", 13), 13), WORLD_LIMITS["radius"]))
    kernels = tuple(clean_kernel(k, channels, radius) for k in world.get("kernels", ())[:MAX_KERNELS])
    numeric = {f: round(clamp(number(world.get(f, DEFAULT_WORLD[f]), DEFAULT_WORLD[f]), lim), 4)
               for f, lim in WORLD_LIMITS.items() if f != "radius"}
    rule = world.get("rule") if world.get("rule") in RULES else "classic"
    return {**world, **numeric, "channels": channels, "radius": radius,
            "kernels": kernels or (DEFAULT_KERNEL,), "rule": rule,
            # binary thresholding would create/destroy mass, so it is off in flow mode
            "binary": bool(world.get("binary", False)) and rule == "classic"}


def kernel_key(world):
    """Everything the kernel FFTs depend on; rebuild them when this changes."""
    return (world["radius"],) + tuple((k["r"], k["rings"], k["core"]) for k in world["kernels"])


def kernel_ffts(world, size=GRID):
    return tuple(make_kernel(world["radius"] * k["r"], k["rings"], k["core"], size) for k in world["kernels"])


def random_world(rng, channels=1, n_kernels=None, radius=13):
    """A random world in the spirit of the Flow Lenia paper's parameter sampling.

    The first `channels` kernels map every channel onto itself so no channel is left
    without input; the remaining kernels connect random channel pairs.
    """
    n_kernels = n_kernels or int(rng.integers(channels, 3 * channels + 1))
    kernels = []
    for i in range(n_kernels):
        src = i if i < channels else int(rng.integers(channels))
        dst = i if i < channels else int(rng.integers(channels))
        rings = tuple(int(rng.integers(1, 13)) / 12 for _ in range(int(rng.integers(1, 4))))
        kernels.append({"src": src, "dst": dst, "r": float(rng.uniform(0.3, 1.0)), "rings": rings,
                        "core": str(rng.choice(KERNEL_CORES)), "growth": str(rng.choice(GROWTH_KINDS)),
                        "mu": float(rng.uniform(0.05, 0.4)), "sigma": float(rng.uniform(0.005, 0.08)),
                        "h": float(rng.uniform(0.1, 1.0))})
    return {"channels": channels, "radius": radius, "kernels": tuple(kernels)}


def apply_world(params, fields):
    """Merge world fields (channels, radius, kernels, dt, ...) into params and re-validate."""
    return clean_world({**params, **fields})


def species_weights(world):
    """The kernel weight vector h of a world, as used for per-cell weights in flow mode."""
    return np.array([k["h"] for k in world["kernels"]], dtype=float)

