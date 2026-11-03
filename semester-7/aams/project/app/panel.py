"""Tkinter control panel, running in its own process.

pygame can only open one window per process, so the panel lives in a child
process. It sends commands to the simulation over `cmd_q` and mirrors the
simulation state it receives on `state_q`, so keyboard changes in the pygame
window show up here too. Tk also fires slider callbacks when we set a slider
during a sync; values are therefore only sent when they differ from the last
known value at slider precision.
"""
import queue
import tkinter as tk
from tkinter import ttk

from app.panel_tabs import (
    KERNEL_RES,
    RING_RES,
    WORLD_RES,
    build_kernels_tab,
    build_plots_tab,
    build_run_tab,
    build_species_tab,
)
from app.widgets import DragTracker, same

POLL_MS = 100


def kernel_label(i, k):
    rings = "/".join(f"{w:.2g}" for w in k["rings"])
    return f"k{i:<2} {k['src']}->{k['dst']}  mu {k['mu']:.3f}  s {k['sigma']:.3f}  h {k['h']:.2f}  [{rings}]"


class ControlPanel:
    def __init__(self, root, cmd_q, state_q, params, species_names):
        self.root, self.cmd_q, self.state_q = root, cmd_q, state_q
        self.drag = DragTracker()
        self.world_vars = {}
        self.last, self.last_rings, self.selected = {}, (), 0
        root.title("Lenia controls")
        root.resizable(False, False)
        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", padx=4, pady=4)
        tabs = {name: tk.Frame(notebook) for name in ("Run", "Kernels", "Species", "Plots")}
        for name, frame in tabs.items():
            notebook.add(frame, text=name)
        build_run_tab(self, tabs["Run"], species_names)
        build_kernels_tab(self, tabs["Kernels"])
        build_species_tab(self, tabs["Species"])
        build_plots_tab(self, tabs["Plots"])
        self.error = tk.Label(root, fg="red", anchor="w")
        self.error.pack(fill="x", padx=10)
        self.status = tk.Label(root, font=("Menlo", 11), justify="left", anchor="w")
        self.status.pack(fill="x", padx=10, pady=(0, 8))
        if not species_names:
            self.error.config(text="species.json not found - creature loading disabled")
        self.sync_sliders(params)  # show the real values before the first state arrives
        self.sync_choices(params)
        self.sync_kernel_list(params)
        root.after(POLL_MS, self.poll)

    # ---------- sending ----------
    def send(self, cmd):
        self.cmd_q.put(cmd)

    def send_kernel(self, fields):
        self.send(("set_kernel", (self.selected, fields)))

    def reset(self):
        text = self.seed_var.get().strip()
        if not text.isdigit():
            self.error.config(text="Seed must be a non-negative integer")
            return
        self.error.config(text="")
        self.send(("reset", int(text)))
        self.root.focus_set()  # leave the entry so the field follows the simulation again

    def on_world_scale(self, key, value):
        value = round(float(value), 4)
        if key in self.last and not same(value, self.last[key], WORLD_RES[key]):
            self.last[key] = value
            self.send(("set", {key: int(value) if key == "radius" else value}))

    def on_kernel_scale(self, key, value):
        value = round(float(value), 4)
        if "k." + key in self.last and not same(value, self.last["k." + key], KERNEL_RES[key]):
            self.last["k." + key] = value
            self.send_kernel({key: value})

    def on_kernel_select(self):
        chosen = self.kernel_list.curselection()
        if chosen and chosen[0] != self.selected:
            self.selected = chosen[0]
            self.send(("select_kernel", chosen[0]))

    def current_rings(self):
        return tuple(round(self.ring_vars[i].get(), 4) for i in range(self.ring_count.get()))

    def on_rings(self):
        self.update_ring_states()
        rings = self.current_rings()
        if not any(w > 0 for w in rings):
            self.error.config(text="At least one ring needs a weight > 0")
            return
        self.error.config(text="")
        changed = len(rings) != len(self.last_rings) or \
            not all(same(a, b, RING_RES) for a, b in zip(rings, self.last_rings))
        if changed:
            self.last_rings = rings
            self.send_kernel({"rings": list(rings)})

    def update_ring_states(self):
        for i, scale in enumerate(self.ring_scales):
            scale.config(state="normal" if i < self.ring_count.get() else "disabled")

    def clear_plots(self):
        for spark in self.sparks.values():
            spark.clear()

    # ---------- receiving ----------
    def poll(self):
        states = []
        try:
            while True:
                states.append(self.state_q.get_nowait())
        except queue.Empty:
            pass
        for state in states:  # every state carries stats; the plots want all of them
            for key, spark in self.sparks.items():
                spark.push(state["stats"][key])
        if states:
            self.sync(states[-1])
            for spark in self.sparks.values():
                spark.redraw()
        self.root.after(POLL_MS, self.poll)

    def sync(self, state):
        if not self.drag.active:
            self.sync_sliders(state)
        self.sync_choices(state)
        self.sync_kernel_list(state)
        stats = state["stats"]
        start = state["species"] or f"seed {state['seed']}"
        self.status.config(text=(
            f"{'PAUSED' if state['paused'] else 'running'}   step {state['step']}   fps {state['fps']:.0f}   "
            f"{state['rule']}{' local' if state['local'] and state['rule'] == 'flow' else ''}\n"
            f"mass {stats['mass']:.1f}   live {stats['live']}   start: {start}"))
        recording = state["recording"]
        self.record_button.config(text="Stop CSV recording" if recording else "Start CSV recording")
        self.record_label.config(text=state.get("record_path") or "")

    def sync_sliders(self, state):
        for key, var in self.world_vars.items():
            self.last[key] = state[key]
            var.set(state[key])
        kernel = state["kernels"][state["selected"]]
        for key, var in self.kernel_vars.items():
            self.last["k." + key] = kernel[key]
            var.set(kernel[key])
        self.last_rings = tuple(kernel["rings"])
        self.ring_count.set(len(kernel["rings"]))
        for var, w in zip(self.ring_vars, kernel["rings"]):
            var.set(w)
        self.update_ring_states()

    def sync_choices(self, state):
        kernel = state["kernels"][state["selected"]]
        self.selected = state["selected"]
        for var, key in ((self.rule_var, "rule"), (self.view_var, "view"), (self.mix_var, "mix"),
                         (self.binary_var, "binary"), (self.local_var, "local"), (self.channels_var, "channels")):
            var.set(state[key])
        self.binary_box.config(state="normal" if state["rule"] == "classic" else "disabled")
        self.src_var.set(kernel["src"])
        self.dst_var.set(kernel["dst"])
        self.core_var.set(kernel["core"])
        self.growth_var.set(kernel["growth"])
        self.profile.draw(kernel["rings"], kernel["core"])
        if state["species"]:
            self.species_var.set(state["species"])
        if self.root.focus_get() is not self.seed_entry:
            self.seed_var.set(str(state["seed"]))

    def sync_kernel_list(self, state):
        labels = [kernel_label(i, k) for i, k in enumerate(state["kernels"])]
        if list(self.kernel_list.get(0, "end")) != labels:
            self.kernel_list.delete(0, "end")
            for label in labels:
                self.kernel_list.insert("end", label)
        if self.kernel_list.curselection() != (state["selected"],):
            self.kernel_list.selection_clear(0, "end")
            self.kernel_list.selection_set(state["selected"])


def run_panel(cmd_q, state_q, params, species_names):
    """Entry point for the panel process."""
    root = tk.Tk()
    ControlPanel(root, cmd_q, state_q, params, species_names)
    root.mainloop()
