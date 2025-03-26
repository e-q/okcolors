import numpy as np

from okcolors.color import ColorDict, ColorPalette, OkLab


def get_colors() -> ColorPalette:
    # Interpolation points
    l_interp = [0, 0.1, 0.5, 0.7, 0.99, 1]
    # a always zero, i.e. along blue/yellow line
    b_interp = [0, -0.01, -0.01, 0.01, 0.01, 0]

    l_vals = np.arange(101) / 100
    b_vals = np.interp(l_vals, l_interp, b_interp)

    colors: ColorDict = {}
    for L, b in enumerate(b_vals):
        c = OkLab(L / 100, 0, round(b, 3))
        name = f"base_{L:02.0f}"
        colors[name] = c
    base = ColorPalette(colors=colors, name="OkColors Base Tones")
    return base
