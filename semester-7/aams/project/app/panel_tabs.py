"""Layout of the four control-panel tabs. Each builder stores the widgets it creates on the panel."""
import tkinter as tk
from tkinter import ttk

from app.commands import APP_LIMITS, MIX_RULES, VIEWS
from app.widgets import KernelProfile, Sparkline
from lenia.kernels import GROWTH_KINDS, KERNEL_CORES
from lenia.world import KERNEL_LIMITS, MAX_CHANNELS, MAX_RINGS, RULES, WORLD_LIMITS

WORLD_RES = {"radius": 1, "dt": 0.001, "flow_dt": 0.01, "theta": 0.01, "mutation_rate": 0.001, "mutation_scale": 0.01}
KERNEL_RES = {"mu": 0.0001, "sigma": 0.0001, "h": 0.01, "r": 0.01}
RING_RES = 0.0001
NUDGE = {"mu": 0.001, "sigma": 0.001, "h": 0.01, "radius": 1}


def section(parent, title):
    frame = tk.LabelFrame(parent, text=title, padx=6, pady=4)
    frame.pack(fill="x", padx=6, pady=3)
    return frame


def world_slider(panel, parent, key, label, row, limits=None):
    lo, hi = (limits or WORLD_LIMITS)[key]
    var = tk.DoubleVar()
    panel.world_vars[key] = var
    tk.Label(parent, text=label, width=8, anchor="w").grid(row=row, column=0)
    panel.drag.slider(parent, var, lo, hi, WORLD_RES[key], lambda v, k=key: panel.on_world_scale(k, v)).grid(
        row=row, column=1, columnspan=3)


def build_run_tab(panel, tab, names):
    sim = section(tab, "Simulation")
    for col, (label, cmd) in enumerate([("Run", ("run", None)), ("Pause", ("pause", None)),
                                        ("Step", ("step", None)), ("Clear", ("clear", None))]):
        tk.Button(sim, text=label, width=6, command=lambda c=cmd: panel.send(c)).grid(row=0, column=col, padx=2)
    tk.Label(sim, text="Seed").grid(row=1, column=0, pady=(6, 0))
    panel.seed_var = tk.StringVar()
    panel.seed_entry = tk.Entry(sim, textvariable=panel.seed_var, width=11)
    panel.seed_entry.grid(row=1, column=1, pady=(6, 0))
    panel.seed_entry.bind("<Return>", lambda _e: panel.reset())
    tk.Button(sim, text="Reset", command=panel.reset).grid(row=1, column=2, pady=(6, 0))
    tk.Button(sim, text="Random", command=lambda: panel.send(("reset", "random"))).grid(row=1, column=3, pady=(6, 0))

    rule = section(tab, "Update rule")
    panel.rule_var = tk.StringVar()
    labels = {"classic": "classic Lenia", "flow": "Flow Lenia (mass conserved)"}
    for col, name in enumerate(RULES):
        tk.Radiobutton(rule, text=labels[name], variable=panel.rule_var, value=name,
                       command=lambda: panel.send(("set", {"rule": panel.rule_var.get()}))).grid(
            row=0, column=col * 2, columnspan=2, sticky="w")
    world_slider(panel, rule, "dt", "dt", 1)
    world_slider(panel, rule, "flow_dt", "flow dt", 2)
    world_slider(panel, rule, "theta", "theta", 3)
    panel.binary_var = tk.BooleanVar()
    panel.binary_box = tk.Checkbutton(rule, text="binary (classic only; needs dt = 1 to change anything)",
                                      variable=panel.binary_var,
                                      command=lambda: panel.send(("set", {"binary": panel.binary_var.get()})))
    panel.binary_box.grid(row=4, column=0, columnspan=4, sticky="w")

    creatures = section(tab, f"Creatures ({len(names)}, from Chan's catalogue + search)")
    panel.species_var = tk.StringVar(value=names[0] if names else "")
    ttk.Combobox(creatures, textvariable=panel.species_var, values=names, state="readonly", width=34).grid(
        row=0, column=0, columnspan=3, sticky="w")
    tk.Button(creatures, text="Load", command=lambda: panel.send(("load", panel.species_var.get()))).grid(
        row=1, column=0, sticky="w")
    tk.Button(creatures, text="Add another (O)", command=lambda: panel.send(("add", None))).grid(row=1, column=1)

    view = section(tab, "View")
    panel.view_var = tk.StringVar()
    for col, name in enumerate(VIEWS):
        tk.Radiobutton(view, text=name, variable=panel.view_var, value=name,
                       command=lambda: panel.send(("set", {"view": panel.view_var.get()}))).grid(row=0, column=col)


def build_kernels_tab(panel, tab):
    world = section(tab, "World")
    tk.Label(world, text="channels").grid(row=0, column=0, sticky="w")
    panel.channels_var = tk.IntVar()
    tk.Spinbox(world, from_=1, to=MAX_CHANNELS, textvariable=panel.channels_var, width=3, state="readonly",
               command=lambda: panel.send(("set", {"channels": panel.channels_var.get()}))).grid(row=0, column=1)
    tk.Button(world, text="Random world", command=lambda: panel.send(("random_world", None))).grid(row=0, column=2)
    world_slider(panel, world, "radius", "R", 1)

    listing = section(tab, "Kernels (source -> target channel)")
    panel.kernel_list = tk.Listbox(listing, height=6, width=44, font=("Menlo", 10), exportselection=False)
    panel.kernel_list.grid(row=0, column=0, columnspan=3)
    panel.kernel_list.bind("<<ListboxSelect>>", lambda _e: panel.on_kernel_select())
    tk.Button(listing, text="Add (copy)", command=lambda: panel.send(("add_kernel", None))).grid(row=1, column=0)
    tk.Button(listing, text="Remove", command=lambda: panel.send(("remove_kernel", None))).grid(row=1, column=1)

    edit = section(tab, "Selected kernel")
    panel.edit_frame = edit
    panel.src_var, panel.dst_var = tk.IntVar(), tk.IntVar()
    for col, (label, var, field) in enumerate((("from", panel.src_var, "src"), ("to", panel.dst_var, "dst"))):
        tk.Label(edit, text=label).grid(row=0, column=col * 2, sticky="e")
        tk.Spinbox(edit, from_=0, to=MAX_CHANNELS - 1, textvariable=var, width=3, state="readonly",
                   command=lambda f=field, v=var: panel.send_kernel({f: v.get()})).grid(row=0, column=col * 2 + 1,
                                                                                      sticky="w")
    panel.kernel_vars = {}
    for row, key in enumerate(("mu", "sigma", "h", "r"), start=1):
        var = tk.DoubleVar()
        panel.kernel_vars[key] = var
        tk.Label(edit, text=key, width=5, anchor="w").grid(row=row, column=0)
        if key in NUDGE:
            tk.Button(edit, text="-", width=1, command=lambda k=key: panel.send(("nudge", (k, -NUDGE[k])))).grid(
                row=row, column=1)
            tk.Button(edit, text="+", width=1, command=lambda k=key: panel.send(("nudge", (k, NUDGE[k])))).grid(
                row=row, column=3)
        lo, hi = KERNEL_LIMITS[key]
        panel.drag.slider(edit, var, lo, hi, KERNEL_RES[key], lambda v, k=key: panel.on_kernel_scale(k, v),
                          length=200).grid(row=row, column=2)

    rings = section(tab, "Rings of the selected kernel")
    tk.Label(rings, text="rings").grid(row=0, column=0, sticky="w")
    panel.ring_count = tk.IntVar(value=1)
    tk.Spinbox(rings, from_=1, to=MAX_RINGS, textvariable=panel.ring_count, width=3, state="readonly",
               command=panel.on_rings).grid(row=0, column=1, sticky="w")
    panel.ring_vars, panel.ring_scales = [], []
    for i in range(MAX_RINGS):
        var = tk.DoubleVar(value=1.0)
        panel.ring_vars.append(var)
        scale = panel.drag.slider(rings, var, 0, 1, RING_RES, lambda _v: panel.on_rings(), length=200)
        scale.grid(row=i + 1, column=1, columnspan=3)
        tk.Label(rings, text=f"ring {i + 1}").grid(row=i + 1, column=0, sticky="w")
        panel.ring_scales.append(scale)
    shapes = tk.Frame(rings)
    shapes.grid(row=5, column=0, columnspan=4, sticky="w")
    panel.core_var, panel.growth_var = tk.StringVar(), tk.StringVar()
    tk.Label(shapes, text="kernel").pack(side="left")
    tk.OptionMenu(shapes, panel.core_var, *KERNEL_CORES, command=lambda v: panel.send_kernel({"core": v})).pack(
        side="left")
    tk.Label(shapes, text="growth").pack(side="left")
    tk.OptionMenu(shapes, panel.growth_var, *GROWTH_KINDS,
                  command=lambda v: panel.send_kernel({"growth": v})).pack(side="left")
    panel.profile = KernelProfile(rings)
    panel.profile.canvas.grid(row=6, column=0, columnspan=4, pady=(4, 0))


def build_species_tab(panel, tab):
    info = ("Flow Lenia only. With local weights on, every cell carries its own kernel\n"
            "weights h, which move with its mass. Painting or adding creatures stamps the\n"
            "current h values (Kernels tab) into those cells: change h, paint again, and a\n"
            "second species with other weights shares the grid. Use view 'species'.")
    tk.Label(tab, text=info, justify="left", fg="gray").pack(padx=8, pady=6, anchor="w")
    local = section(tab, "Per-cell kernel weights")
    panel.local_var = tk.BooleanVar()
    tk.Checkbutton(local, text="local weights (parameter localisation)", variable=panel.local_var,
                   command=lambda: panel.send(("set", {"local": panel.local_var.get()}))).grid(
        row=0, column=0, columnspan=4, sticky="w")
    tk.Label(local, text="mixing").grid(row=1, column=0, sticky="w")
    panel.mix_var = tk.StringVar()
    mix_labels = {"stoch": "random source (paper)", "avg": "average"}
    for col, name in enumerate(MIX_RULES, start=1):
        tk.Radiobutton(local, text=mix_labels[name], variable=panel.mix_var, value=name,
                       command=lambda: panel.send(("set", {"mix": panel.mix_var.get()}))).grid(row=1, column=col)
    tk.Button(local, text="Random species weights", command=lambda: panel.send(("random_weights", None))).grid(
        row=2, column=0, columnspan=4, sticky="w", pady=(4, 0))

    mutation = section(tab, "Mutation (random weight changes in 20x20 patches)")
    world_slider(panel, mutation, "mutation_rate", "rate/step", 0, APP_LIMITS)
    world_slider(panel, mutation, "mutation_scale", "strength", 1, APP_LIMITS)


def build_plots_tab(panel, tab):
    panel.sparks = {
        "mass": Sparkline(tab, "mass", fmt="{:.1f}"),
        "live": Sparkline(tab, "live cells", fmt="{:.0f}"),
        "speed": Sparkline(tab, "centroid speed (cells/step)", fmt="{:.3f}"),
        "activity": Sparkline(tab, "activity (mean |change| per mass)", fmt="{:.4f}"),
        "concentration": Sparkline(tab, "concentration (1 = one compact object)", fmt="{:.2f}"),
    }
    rec = section(tab, "Recording")
    panel.record_button = tk.Button(rec, text="Start CSV recording", command=lambda: panel.send(("toggle_record", None)))
    panel.record_button.grid(row=0, column=0, sticky="w")
    tk.Button(rec, text="Clear plots", command=panel.clear_plots).grid(row=0, column=1)
    panel.record_label = tk.Label(rec, text="", fg="gray", anchor="w")
    panel.record_label.grid(row=1, column=0, columnspan=2, sticky="w")
