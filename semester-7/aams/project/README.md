# Lenia playground

Classic Lenia and Flow Lenia with multi-channel creatures, per-cell species weights and analysis tools (numpy + pygame + tkinter).

**Install:** `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt` (tests: `pip install -r requirements-dev.txt`)

**Run:** `python lenia_poc.py` opens the simulation and a control panel. Options: `--species "Orbium"`, `--rule flow`, `--seed N`, `--no-panel`, `--max-frames N`.

**Keys (simulation window):** SPACE pause · `.` step · R reset (new seed) · C clear · O add creature · F classic/flow · V view · W random world · B binary · UP/DOWN mu · LEFT/RIGHT sigma (selected kernel) · `[` `]` radius · S screenshot · mouse drag paints · ESC quit.

**Control panel tabs**
- *Run*: run/pause/step/clear, seed, update rule (classic dt; flow dt and theta), creature catalogue (load / add another), view (mass, channels as RGB, species).
- *Kernels*: 1-3 channels, the kernel list (source -> target channel), add/remove/random world, and for the selected kernel: mu, sigma, weight h, radius ratio r, 1-4 ring weights, kernel/growth shape, profile plot.
- *Species* (flow only): per-cell kernel weights that travel with the mass; painting and adding creatures stamps the current h values, so several species can share a grid. Mixing rule (random source as in the paper, or average) and mutation.
- *Plots*: live mass, live cells, centroid speed, activity, concentration; CSV recording to `./runs`.

**Tools**
- `python -m tools.phase_map --rule classic` (or `--rule flow`, `--species NAME`, `--x mu:0.05:0.35:24 --y sigma:0.005:0.06:24`): runs every parameter combination headless and saves a colour-coded outcome map (dies / fills / pattern / static / moving / dynamic) plus CSV to `./maps`.
- `python -m tools.search --rule flow --tries 200`: random worlds, keeps creatures that move as one compact object, saves them to `discovered.json` (loaded by the app).
- `python -m tools.import_chan --matlab Lenia.m --found 2*.json`: rebuilds `species.json` from Chan's catalogue, keeping only creatures that survive here.

**Tests:** `python -m pytest` (`-m "not gui"` skips the tests that open a Tk window).

**Layout:** `lenia/` simulation core (kernels, classic and flow update, world config, patterns, metrics, catalogue, headless runs) · `app/` simulation state, commands, rendering, panel, recorder · `tools/` command-line tools · `lenia_poc.py` pygame entry point.

**Credits:** creatures in `species.json` are from Bert Wang-Chak Chan's Lenia (https://github.com/Chakazul/Lenia, MIT licence). Flow Lenia follows Plantec et al. 2023 (https://github.com/erwanplantec/FlowLenia); `lenia/flow.py` is written from the paper's formulas, not copied.
