"""The running simulation: state arrays plus app parameters, independent of pygame and tkinter.

State arrays are replaced, never modified in place, so a reference kept by a caller
(e.g. the previous frame for metrics) stays valid.
"""
import numpy as np

from app.commands import DEFAULTS, apply_command
from lenia.classic import classic_step
from lenia.flow import flow_step, mutate
from lenia.metrics import snapshot
from lenia.patterns import disc_mask, init_state, pattern_mask, place_pattern, stamp_weights
from lenia.world import GRID, apply_world, kernel_ffts, kernel_key, species_weights

MUTATION_PATCH = 20
STRUCTURE_ACTIONS = ("structure", "load", "reset", "clear")


class Simulation:
    def __init__(self, params=None, catalogue=None, size=GRID, rng=None):
        self.catalogue = catalogue or {}
        self.size = size
        self.rng = rng or np.random.default_rng()
        self.params = apply_world({**DEFAULTS, **(params or {})}, {})
        self.a = init_state(self.params["seed"], self.params["radius"], self.params["channels"], size)
        self.weights = None
        self.kffts, self.kkey = None, None
        self.step_count = 0
        self.refresh()
        self.stats = snapshot(self.a)

    # ---------- commands ----------
    def apply(self, cmd):
        """Apply one command and carry out its action; returns the action (or None)."""
        self.params, action = apply_command(self.params, cmd, self.catalogue)
        p = self.params
        if action == "reset":
            self.a, self.step_count = init_state(p["seed"], p["radius"], p["channels"], self.size), 0
        elif action == "load":
            cells = self.catalogue[p["species"]]["cells"]
            empty = np.zeros((p["channels"], self.size, self.size))
            self.a, self.step_count = place_pattern(empty, cells, self.size // 2, self.size // 2), 0
        elif action == "clear":
            self.a, self.step_count = np.zeros_like(self.a), 0
        self.refresh(force_weights=action in STRUCTURE_ACTIONS)
        if action == "add":
            self.add_creature()
        self.stats = snapshot(self.a)
        return action

    def refresh(self, force_weights=False):
        """Bring arrays in line with params: channel count, kernel FFTs and per-cell weights."""
        p = self.params
        channels = p["channels"]
        if self.a.shape[0] < channels:
            self.a = np.concatenate([self.a, np.zeros((channels - self.a.shape[0], self.size, self.size))])
        elif self.a.shape[0] > channels:
            self.a = self.a[:channels]
        if kernel_key(p) != self.kkey:
            self.kkey, self.kffts = kernel_key(p), kernel_ffts(p, self.size)
        local = p["local"] and p["rule"] == "flow"
        if not local:
            self.weights = None
        elif force_weights or self.weights is None or self.weights.shape[0] != len(p["kernels"]):
            self.weights = np.broadcast_to(species_weights(p)[:, None, None],
                                           (len(p["kernels"]), self.size, self.size)).copy()

    # ---------- changing the grid ----------
    def add_creature(self):
        """Place one more creature (the loaded species, else the first one) at a random spot and rotation."""
        if not self.catalogue:
            return
        name = self.params["species"] if self.params["species"] in self.catalogue else next(iter(self.catalogue))
        cells = self.catalogue[name]["cells"]
        cy, cx = self.rng.integers(0, self.size, size=2)
        turns = int(self.rng.integers(0, 4))
        self.a = place_pattern(self.a, cells, cy, cx, turns)
        if self.weights is not None:
            mask = pattern_mask(self.a.shape, cells, cy, cx, turns)
            self.weights = stamp_weights(self.weights, mask, species_weights(self.params))

    def paint(self, cy, cx, radius=4):
        """Paint a small blob of live cells (all channels); with local weights, stamp the current h there."""
        mask = disc_mask(cy, cx, radius, self.size)
        a = self.a.copy()
        a[:, mask] = np.maximum(a[:, mask], 0.5 + 0.5 * self.rng.random((a.shape[0], mask.sum())))
        self.a = a
        if self.weights is not None:
            self.weights = stamp_weights(self.weights, mask, species_weights(self.params))
        self.stats = snapshot(self.a)

    # ---------- time ----------
    def step(self):
        p, prev, prev_centroid = self.params, self.a, self.stats["centroid"]
        if p["rule"] == "flow":
            self.a, weights = flow_step(self.a, self.kffts, p["kernels"], p["theta"], p["flow_dt"],
                                        self.weights, p["mix"], self.rng)
            if weights is not None:
                self.weights = mutate(weights, self.rng, p["mutation_rate"], MUTATION_PATCH, p["mutation_scale"])
        else:
            self.a = classic_step(self.a, self.kffts, p["kernels"], p["dt"], p["binary"])
        self.step_count += 1
        self.stats = snapshot(self.a, prev, prev_centroid)

    def public_stats(self):
        return {k: v for k, v in self.stats.items() if k != "centroid"}
