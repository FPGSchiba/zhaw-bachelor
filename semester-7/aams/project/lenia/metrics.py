"""Measurements of a running simulation, shared by the live plots, the phase map and the search.

All positions are on the torus, so centroids use circular means: each coordinate
is mapped to an angle, averaged as a complex number and mapped back.
"""
import numpy as np

LIVE_THRESHOLD = 0.1
OUTCOMES = ("dies", "fills", "pattern", "static", "moving", "dynamic")
LOCALISED = 0.5  # concentration above which the mass counts as one object (or a few close ones)


def circular_stats(m):
    """Centroid (y, x) of the mass field m on the torus, and its concentration in [0, 1] per axis.

    Concentration ~1 means one compact object, ~0 means mass spread over the whole grid.
    """
    total = m.sum()
    if total <= 0:
        return np.array([np.nan, np.nan]), np.array([0.0, 0.0])
    size = np.array(m.shape)
    out_c, out_r = [], []
    for axis, n in ((1, size[0]), (0, size[1])):
        angles = np.exp(2j * np.pi * np.arange(n) / n)
        z = (m.sum(axis=axis) * angles).sum() / total
        out_c.append((np.angle(z) % (2 * np.pi)) * n / (2 * np.pi))
        out_r.append(abs(z))
    return np.array(out_c), np.array(out_r)


def wrapped_distance(p, q, size):
    """Shortest distance between two points on a size x size torus."""
    d = (np.asarray(q) - np.asarray(p) + size / 2) % size - size / 2
    return float(np.hypot(*d))


def snapshot(a, prev=None, prev_centroid=None):
    """Numbers for one frame: mass, live cells, centroid speed and activity (mean |change| per unit mass)."""
    m = a.sum(axis=0)
    mass = float(m.sum())
    centroid, concentration = circular_stats(m)
    speed = activity = 0.0
    if prev is not None and mass > 0:
        activity = float(np.abs(a - prev).sum() / mass)
    if prev_centroid is not None and not np.isnan(prev_centroid).any() and not np.isnan(centroid).any():
        speed = wrapped_distance(prev_centroid, centroid, m.shape[0])
    return {"mass": mass, "live": int((m > LIVE_THRESHOLD).sum()), "speed": speed, "activity": activity,
            "concentration": float(concentration.min()), "centroid": centroid}


def classify(a0, a, trace):
    """Outcome of a run, from the start state a0, final state a and a list of late snapshot() dicts.

    dies:    mass dropped below 1% of the start
    fills:   live cells cover more than 40% of the grid
    pattern: mass spread over the grid in spots/stripes (not one object), changing or not
    moving:  one compact object whose centroid keeps travelling
    static:  a localised object that (almost) stops changing
    dynamic: a localised object that keeps changing (oscillating, rotating, splitting, chaotic)
    """
    m0, m = a0.sum(), a.sum()
    cells = a.shape[1] * a.shape[2]
    if m < 0.01 * m0 or m < 1e-6:
        return "dies"
    if (a.sum(axis=0) > LIVE_THRESHOLD).sum() > 0.4 * cells:
        return "fills"
    activity = np.mean([s["activity"] for s in trace]) if trace else 0.0
    speed = np.mean([s["speed"] for s in trace]) if trace else 0.0
    concentration = min(s["concentration"] for s in trace) if trace else 0.0
    if concentration < LOCALISED:
        return "pattern"
    if concentration > 0.8 and speed > 0.02:
        return "moving"
    if activity < 1e-3:
        return "static"
    return "dynamic"
