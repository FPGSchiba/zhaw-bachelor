"""Lenia playground - classic and Flow Lenia with multi-channel creatures (numpy + pygame).

The simulation core is the `lenia` package, the app (simulation state, commands,
rendering, control panel) is the `app` package; this file is the pygame loop.
"""
import argparse
import multiprocessing as mp
import os
import queue
import time

import pygame

from app.recorder import CsvRecorder
from app.render import colourise, draw, make_palette, overlay_lines
from app.simulation import Simulation
from lenia.species import load_catalogue
from lenia.world import GRID, RULES

WINDOW = 768
FPS = 30
PAINT_RADIUS = 4
STATE_EVERY = 3  # send state to the control panel every N frames
HERE = os.path.dirname(os.path.abspath(__file__))
CATALOGUES = (os.path.join(HERE, "species.json"), os.path.join(HERE, "discovered.json"))

# Keyboard shortcuts map onto the same commands the control panel sends.
KEY_COMMANDS = {
    pygame.K_SPACE: ("toggle_pause", None), pygame.K_r: ("reset", "random"), pygame.K_c: ("clear", None),
    pygame.K_b: ("toggle_binary", None), pygame.K_PERIOD: ("step", None), pygame.K_o: ("add", None),
    pygame.K_f: ("toggle_rule", None), pygame.K_v: ("cycle_view", None), pygame.K_w: ("random_world", None),
    pygame.K_UP: ("nudge", ("mu", 0.001)), pygame.K_DOWN: ("nudge", ("mu", -0.001)),
    pygame.K_RIGHT: ("nudge", ("sigma", 0.001)), pygame.K_LEFT: ("nudge", ("sigma", -0.001)),
    pygame.K_RIGHTBRACKET: ("nudge", ("radius", 1)), pygame.K_LEFTBRACKET: ("nudge", ("radius", -1)),
}


def start_panel(params, species_names):
    """Launch the tkinter control panel in a separate process; returns (process, cmd_q, state_q)."""
    from app.panel import run_panel
    ctx = mp.get_context("spawn")
    cmd_q, state_q = ctx.Queue(), ctx.Queue(maxsize=12)
    state_q.cancel_join_thread()  # don't block on exit if the panel stopped reading
    proc = ctx.Process(target=run_panel, args=(cmd_q, state_q, params, species_names), daemon=True)
    proc.start()
    return proc, cmd_q, state_q


def collect_commands(cmd_q, screen, step_count):
    """Keyboard/window events and panel commands of this frame; returns (commands, quit_requested)."""
    commands, quit_requested = [], False
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            quit_requested = True
        elif event.type == pygame.KEYDOWN and event.key in KEY_COMMANDS:
            commands.append(KEY_COMMANDS[event.key])
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            os.makedirs("screenshots", exist_ok=True)
            path = os.path.join("screenshots", f"lenia_{time.strftime('%Y%m%d_%H%M%S')}_step{step_count}.png")
            pygame.image.save(screen, path)
            print(f"saved {path}")
    if cmd_q is not None:
        try:
            while True:
                commands.append(cmd_q.get_nowait())
        except queue.Empty:
            pass
    return commands, quit_requested


def parse_args(species_names):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=0, help="random seed for the initial state")
    parser.add_argument("--species", help="start from a creature in the catalogue, e.g. Orbium")
    parser.add_argument("--rule", choices=RULES, default="classic", help="update rule (flow = Flow Lenia)")
    parser.add_argument("--max-frames", type=int, default=0, help="quit after N frames (0 = run forever)")
    parser.add_argument("--no-panel", action="store_true", help="don't open the control panel window")
    args = parser.parse_args()
    if args.species and args.species not in species_names:
        parser.error(f"unknown species {args.species!r}; see species.json for names")
    return args


def main():
    catalogue = load_catalogue(*CATALOGUES)
    args = parse_args(catalogue)
    sim = Simulation({"seed": args.seed, "rule": args.rule}, catalogue)
    if args.species:
        sim.apply(("load", args.species))
    panel, cmd_q, state_q = (None, None, None) if args.no_panel else start_panel(sim.params, list(catalogue))

    pygame.init()
    screen = pygame.display.set_mode((WINDOW, WINDOW))
    pygame.display.set_caption("Lenia playground")
    font = pygame.font.SysFont("menlo,consolas,monospace", 14)
    clock = pygame.time.Clock()
    palette = make_palette()
    recorder = CsvRecorder()
    scale = WINDOW / GRID
    frame, running = 0, True
    try:
        while running:
            commands, quit_requested = collect_commands(cmd_q, screen, sim.step_count)
            running = not quit_requested
            one_step = False
            for cmd in commands:
                action = sim.apply(cmd)
                one_step = one_step or action == "step"
                if action == "record" and sim.params["recording"]:
                    print(f"recording to {recorder.start()}")
                elif action == "record":
                    recorder.stop()
                    print("recording stopped")

            if pygame.mouse.get_pressed()[0]:  # click / drag paints live cells under the cursor
                mx, my = pygame.mouse.get_pos()
                sim.paint(int(my / scale), int(mx / scale), PAINT_RADIUS)

            if not sim.params["paused"] or one_step:
                sim.step()
                recorder.write(sim.step_count, sim.params, sim.stats)

            image = colourise(sim.a, sim.params["view"], palette, sim.weights)
            draw(screen, image, font, overlay_lines(sim.params, sim.step_count, sim.stats, clock.get_fps()), WINDOW)
            if state_q is not None and frame % STATE_EVERY == 0:
                try:
                    state_q.put_nowait({**sim.params, "step": sim.step_count, "fps": clock.get_fps(),
                                        "stats": sim.public_stats(),
                                        "record_path": recorder.path if recorder.active else None})
                except queue.Full:
                    pass  # panel is closed or busy; it only needs the latest state anyway
            clock.tick(FPS)
            frame += 1
            if args.max_frames and frame >= args.max_frames:
                running = False
    finally:
        recorder.stop()
        if panel is not None:
            panel.terminate()
        pygame.quit()


if __name__ == "__main__":
    main()
