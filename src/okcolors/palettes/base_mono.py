from okcolors.color import ColorDict, ColorPalette, OkLab


def get_colors() -> ColorPalette:
    colors: ColorDict = {}
    for L in range(0, 101):
        c = OkLab(L / 100, 0, 0)
        name = f"base_{L:02.0f}"
        colors[name] = c
    base = ColorPalette(colors=colors, name="OkColors Grayscale Tones")
    return base
