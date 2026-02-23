"""Sharp accent palette with APCA-driven lightness and gamut-maximized chroma.

For each hue angle, lightness is adjusted to hit a target APCA Lc value against
pure black/white backgrounds, then chroma is maximized to the sRGB gamut boundary.
"""

from okcolors.color import Color, ColorDict, ColorPalette
from okcolors.contrast import adjust_for_contrast_max_chroma

_HUES: list[tuple[str, float]] = [
    ("magenta", 342),
    ("red", 18),
    ("orange", 54),
    ("yellow", 90),
    ("green", 150),
    ("cyan", 210),
    ("blue", 270),
    ("purple", 306),
]


def get_colors(
    bg_dark: Color,
    bg_light: Color,
    target_lc: float = 70.0,
    max_C_dark: float = 0.2,
    max_C_light: float = 0.2,
) -> ColorPalette:
    """Build accent palette with max-chroma colors tuned to *target_lc* APCA contrast."""
    colors: ColorDict = {}

    for name, h in _HUES:
        # Dark variant: dark fg on light bg → positive Lc
        colors[f"{name}_dark"] = adjust_for_contrast_max_chroma(
            h, bg_light, target_lc, max_C=max_C_dark
        )
        # Light variant: light fg on dark bg → negative Lc
        colors[f"{name}_light"] = adjust_for_contrast_max_chroma(
            h, bg_dark, -target_lc, max_C=max_C_light
        )

    return ColorPalette(colors=colors, name="OkColors-Sharp Accent Colors")
