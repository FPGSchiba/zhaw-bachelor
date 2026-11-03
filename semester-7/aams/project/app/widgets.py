"""Small tkinter building blocks for the control panel."""
import tkinter as tk

import numpy as np

from lenia.kernels import kernel_shell


def same(a, b, resolution):
    """True if two values are equal at slider precision (Tk rounds slider values to `resolution`)."""
    return round(a / resolution) == round(b / resolution)


class DragTracker:
    """Remembers whether the user is currently dragging any slider, so syncs don't fight the mouse."""

    def __init__(self):
        self.active = False

    def slider(self, parent, var, lo, hi, resolution, command, length=220):
        scale = tk.Scale(parent, variable=var, from_=lo, to=hi, resolution=resolution, orient="horizontal",
                         length=length, command=command, showvalue=True)
        scale.bind("<ButtonPress-1>", lambda _e: setattr(self, "active", True))
        scale.bind("<ButtonRelease-1>", lambda _e: setattr(self, "active", False))
        return scale


class Sparkline:
    """A tiny line chart of the last `capacity` values, with the current value as text."""

    def __init__(self, parent, label, width=300, height=46, capacity=300, fmt="{:.3f}"):
        self.label, self.fmt, self.capacity = label, fmt, capacity
        self.values = []
        self.text = tk.Label(parent, anchor="w", font=("Menlo", 11))
        self.text.pack(fill="x")
        self.canvas = tk.Canvas(parent, width=width, height=height, bg="#111", highlightthickness=0)
        self.canvas.pack(pady=(0, 4))
        self.width, self.height = width, height

    def push(self, value):
        self.values = (self.values + [float(value)])[-self.capacity:]

    def clear(self):
        self.values = []

    def redraw(self):
        self.canvas.delete("all")
        if not self.values:
            self.text.config(text=f"{self.label}: -")
            return
        lo, hi = min(self.values), max(self.values)
        span = hi - lo or 1.0
        n = len(self.values)
        xs = np.linspace(0, self.width - 1, n) if n > 1 else np.array([0.0])
        ys = self.height - 3 - (np.asarray(self.values) - lo) / span * (self.height - 6)
        if n > 1:
            self.canvas.create_line(*np.column_stack([xs, ys]).ravel(), fill="#f5a623", width=1.5)
        self.text.config(text=f"{self.label}: {self.fmt.format(self.values[-1])}   "
                              f"(min {self.fmt.format(lo)}, max {self.fmt.format(hi)})")


class KernelProfile:
    """Plot of K(r) from the kernel centre (left) to its edge (right)."""

    def __init__(self, parent, width=300, height=56):
        self.canvas = tk.Canvas(parent, width=width, height=height, bg="#111", highlightthickness=0)
        self.width, self.height, self.key = width, height, None

    def draw(self, rings, core):
        if (tuple(rings), core) == self.key:
            return
        self.key = (tuple(rings), core)
        k = kernel_shell(np.linspace(0, 1, self.width, endpoint=False), rings, core)
        k = k / k.max() if k.max() > 0 else k
        points = np.column_stack([np.arange(self.width), self.height - 4 - k * (self.height - 8)]).ravel()
        self.canvas.delete("all")
        self.canvas.create_line(*points, fill="#f5a623", width=2)
