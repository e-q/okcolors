import numpy as np

from okcolors.color import ColorDict, ColorPalette, OkLab

# Interpolation points for the chromatic tint curve (b-axis).
# Cool (negative b) in darks, warm (positive b) in lights.
_L_INTERP = [0, 0.1, 0.5, 0.7, 0.99, 1]
_B_INTERP = [0, -0.01, -0.01, 0.01, 0.01, 0]


def tone_at(L: float) -> OkLab:
    """Return a chromatically-tinted OkLab color at lightness *L*."""
    b = float(np.interp(L, _L_INTERP, _B_INTERP))
    return OkLab(L, 0, round(b, 3))


def get_tones(lightnesses: dict[str, float]) -> ColorPalette:
    """Build a palette from a ``{role: L}`` mapping using the tint curve."""
    colors: ColorDict = {role: tone_at(L) for role, L in lightnesses.items()}
    return ColorPalette(colors=colors, name="OkColors Base Tones")


def get_colors() -> ColorPalette:
    l_vals = np.arange(101) / 100
    colors: ColorDict = {}
    for i, L in enumerate(l_vals):
        colors[f"base_{i:02.0f}"] = tone_at(float(L))
    return ColorPalette(colors=colors, name="OkColors Base Tones")
