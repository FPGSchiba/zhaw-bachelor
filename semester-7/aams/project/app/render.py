"""Turning the state into pixels: colour views and the text overlay (numpy + pygame)."""
import numpy as np
import pygame

CHANNEL_COLOURS = np.array([[1.0, 0.25, 0.2], [0.25, 1.0, 0.35], [0.3, 0.5, 1.0]])
# Fixed, irrational-ish weights so different kernel-weight vectors get clearly different hues.
HUE_WEIGHTS = (np.arange(1, 13) * 0.6180339887) % 1 + 0.5


def make_palette():
    """256-entry magma-like colour lookup table, interpolated from a few anchors."""
    anchors = np.array([[0, 0, 4], [40, 11, 84], [101, 21, 110], [159, 42, 99],
                        [212, 72, 66], [245, 125, 21], [250, 193, 39], [252, 253, 191]])
    pos = np.linspace(0, 1, len(anchors))
    t = np.linspace(0, 1, 256)
    return np.stack([np.interp(t, pos, anchors[:, c]) for c in range(3)], axis=1).astype(np.uint8)


def hsv_to_rgb(h, s, v):
    """Vectorised HSV -> RGB, all inputs and outputs in [0, 1]."""
    i = np.floor(h * 6).astype(int) % 6
    f = h * 6 - np.floor(h * 6)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    choices = [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]
    return np.stack([np.choose(i, [c[ch] for c in choices]) for ch in range(3)], axis=-1)


def colourise(a, view, palette, weights=None):
    """(H, W, 3) uint8 image of the state `a` (channels, H, W) in the chosen view.

    mass:     total mass through the palette (flow mode can exceed 1; it is clipped)
    channels: channel 0/1/2 as red/green/blue (one channel falls back to the palette)
    species:  hue from the per-cell kernel weights, brightness from mass (flow + local weights)
    """
    mass = np.clip(a.sum(axis=0), 0, 1)
    if view == "species" and weights is not None:
        hue = (np.tensordot(HUE_WEIGHTS[: weights.shape[0]], weights, axes=1)) % 1
        return (hsv_to_rgb(hue, np.full_like(hue, 0.8), mass) * 255).astype(np.uint8)
    if view in ("channels", "species") and a.shape[0] > 1:
        rgb = np.tensordot(np.clip(a, 0, 1), CHANNEL_COLOURS[: a.shape[0]], axes=(0, 0))
        return (np.clip(rgb, 0, 1) * 255).astype(np.uint8)
    return palette[(mass * 255).astype(np.uint8)]


def draw(screen, image, font, lines, window):
    surf = pygame.surfarray.make_surface(image.transpose(1, 0, 2))  # pygame wants (W, H, 3)
    screen.blit(pygame.transform.scale(surf, (window, window)), (0, 0))
    box = pygame.Surface((300, 16 * len(lines) + 8), pygame.SRCALPHA)
    box.fill((0, 0, 0, 150))
    screen.blit(box, (4, 4))
    for i, text in enumerate(lines):
        screen.blit(font.render(text, True, (235, 235, 235)), (10, 8 + 16 * i))
    pygame.display.flip()


def overlay_lines(params, step_count, stats, fps):
    k = params["kernels"][params["selected"]]
    if params["rule"] == "flow":
        rule = f"flow  theta {params['theta']:.2f}  dt {params['flow_dt']:.2f}"
        if params["local"]:
            rule += f"  local/{params['mix']}"
    else:
        rule = f"classic  dt {params['dt']:.3f}{'  binary' if params['binary'] else ''}"
    rings = ", ".join(f"{w:.2f}" for w in k["rings"])
    return [
        f"step   {step_count}{'  (paused)' if params['paused'] else ''}{'  REC' if params['recording'] else ''}",
        f"rule   {rule}",
        f"world  {params['channels']} ch, {len(params['kernels'])} kernels, R {params['radius']}",
        f"k{params['selected']}     {k['src']}->{k['dst']} mu {k['mu']:.3f} sigma {k['sigma']:.4f} h {k['h']:.2f}",
        f"       r {k['r']:.2f} rings {rings} {k['core']}/{k['growth']}",
        f"mass   {stats['mass']:.1f}   live {stats['live']}",
        f"speed  {stats['speed']:.3f}   activity {stats['activity']:.4f}",
        f"view   {params['view']}   start {params['species'] or 'seed ' + str(params['seed'])}",
        f"fps    {fps:.1f}",
    ]
