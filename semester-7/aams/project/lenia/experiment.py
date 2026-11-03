"""Headless runs for the analysis tools: simulate a world from a start state and classify the outcome."""
import numpy as np

from lenia.classic import classic_step
from lenia.flow import flow_step
from lenia.metrics import circular_stats, classify, snapshot
from lenia.world import kernel_ffts


def run(world, a0, steps, trace_steps=100):
    """Simulate `steps` steps; returns (final state, snapshots of the last `trace_steps` steps)."""
    kf = kernel_ffts(world, a0.shape[1])
    a, trace, prev_centroid = a0, [], None
    for i in range(steps):
        prev = a
        if world["rule"] == "flow":
            a, _ = flow_step(a, kf, world["kernels"], world["theta"], world["flow_dt"])
        else:
            a = classic_step(a, kf, world["kernels"], world["dt"], world["binary"])
        if i >= steps - trace_steps:
            snap = snapshot(a, prev, prev_centroid)
            trace.append(snap)
            prev_centroid = snap["centroid"]
    return a, trace[1:]  # the first snapshot has no previous centroid, so no speed


def evaluate(world, a0, steps, trace_steps=100):
    """Run and summarise: outcome class plus the numbers it was based on."""
    a, trace = run(world, a0, steps, trace_steps)
    mean = (lambda key: float(np.mean([s[key] for s in trace]))) if trace else (lambda key: 0.0)
    return {"outcome": classify(a0, a, trace), "mass_ratio": float(a.sum() / max(a0.sum(), 1e-12)),
            "speed": mean("speed"), "activity": mean("activity"), "concentration": mean("concentration"),
            "final": a}


def crop_creature(a, margin=6, max_size=128):
    """Cut the object out of the torus: centre it on its mass centroid, then crop to where there is mass."""
    m = a.sum(axis=0)
    if m.sum() <= 0:
        return None
    centroid, _ = circular_stats(m)
    size = np.array(m.shape)
    shift = (size // 2 - np.round(centroid).astype(int)) % size
    centred = np.roll(a, tuple(shift), axis=(1, 2))
    ys, xs = np.nonzero(centred.sum(axis=0) > 0.01)
    if len(ys) == 0:
        return None
    y0, y1 = max(ys.min() - margin, 0), min(ys.max() + margin + 1, m.shape[0])
    x0, x1 = max(xs.min() - margin, 0), min(xs.max() + margin + 1, m.shape[1])
    if y1 - y0 > max_size or x1 - x0 > max_size:
        return None
    return np.clip(centred[:, y0:y1, x0:x1], 0, 1)
