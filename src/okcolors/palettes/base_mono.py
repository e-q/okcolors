from okcolors.color import ColorDict, ColorPalette, OkLab


def tone_at(L: float) -> OkLab:
    """Return a pure achromatic OkLab color at lightness *L*."""
    return OkLab(L, 0, 0)


def get_tones(lightnesses: dict[str, float]) -> ColorPalette:
    """Build an achromatic palette from a ``{role: L}`` mapping."""
    colors: ColorDict = {role: tone_at(L) for role, L in lightnesses.items()}
    return ColorPalette(colors=colors, name="OkColors Grayscale Tones")


def get_colors() -> ColorPalette:
    colors: ColorDict = {}
    for L in range(101):
        colors[f"base_{L:02.0f}"] = tone_at(L / 100)
    return ColorPalette(colors=colors, name="OkColors Grayscale Tones")
