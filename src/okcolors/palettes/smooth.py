"""Smooth accent palette with lightness driven by APCA contrast targets.

Hue angles and chromas are fixed; OkLCh lightness is computed via bisection
to hit a specific APCA Lc value against the provided background colors.
"""

from okcolors.color import Color, ColorDict, ColorPalette, OkLCh
from okcolors.contrast import adjust_foreground_for_contrast

_ACCENTS: list[tuple[str, float, float]] = [
    ("magenta", 0.2, 342),
    ("red", 0.2, 18),
    ("orange", 0.1, 54),
    ("yellow", 0.1, 90),
    ("green", 0.1, 150),
    ("cyan", 0.1, 210),
    ("blue", 0.1, 270),
    ("purple", 0.1, 306),
]

# Magenta and red have higher chroma in the light variant.
_LIGHT_CHROMA_OVERRIDES: dict[str, float] = {"magenta": 0.17, "red": 0.125}


def get_colors(
    bg_dark: Color, bg_light: Color, target_lc: float = 70.0
) -> ColorPalette:
    """Build accent palette with lightness tuned to *target_lc* APCA contrast.

    *bg_dark* and *bg_light* are the background colors for the dark and light
    scheme variants respectively.  Each accent is seeded at an arbitrary
    mid-lightness and then adjusted to achieve the requested contrast.

    APCA is asymmetric: light-on-dark text (negative Lc) needs a different
    absolute value than dark-on-light (positive Lc) to look equally readable.
    ``target_lc`` is applied with the correct sign for each polarity.
    """
    colors: ColorDict = {}

    for name, C, h in _ACCENTS:
        seed = OkLCh(0.5, C, h)
        # Dark variant: light fg on dark bg → negative Lc
        colors[f"{name}_dark"] = adjust_foreground_for_contrast(
            seed, bg_light, target_lc
        )
        # Light variant: dark fg on light bg → positive Lc  (but APCA gives
        # negative Lc for light-on-dark, so we negate the target)
        C_light = _LIGHT_CHROMA_OVERRIDES.get(name, C)
        seed_light = OkLCh(0.5, C_light, h)
        colors[f"{name}_light"] = adjust_foreground_for_contrast(
            seed_light, bg_dark, -target_lc
        )

    return ColorPalette(colors=colors, name="OkColors-Smooth Accent Colors")
