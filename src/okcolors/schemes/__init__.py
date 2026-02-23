from typing import Literal, TypedDict, get_args

from okcolors.color import Color, ColorPalette, Variant
from okcolors.contrast import apca_contrast, wcag_contrast
from okcolors.palettes import OkColorPalette, get_tinter
from okcolors.schemes.roles import get_roles

__all__ = ["OkColorscheme", "colorscheme_report", "get_colorscheme"]


OkColorscheme = Literal["sharp", "smooth"]

# Per-variant background parameters: (bg_L, bg_step)
_APCA_PARAMS: dict[str, dict[str, tuple[float, float]]] = {
    "smooth": {"dark": (0.20, 0.05), "light": (0.99, 0.025)},
    "sharp": {"dark": (0.00, 0.05), "light": (1.00, 0.025)},
}


def get_colorscheme(
    name: OkColorPalette = "smooth", kind: Variant = "dark"
) -> ColorPalette:
    if name not in get_args(OkColorscheme):
        raise ValueError(
            f"Unknown colorscheme name, must be one of {get_args(OkColorscheme)}"
        )
    high_contrast = name == "sharp"
    tinter = get_tinter(mono=high_contrast)
    bg_L, bg_step = _APCA_PARAMS[name][kind]

    if name == "smooth":
        from okcolors.palettes import smooth

        variant_colors = smooth.get_colors(bg_dark=tinter(0.20), bg_light=tinter(0.99))
    else:  # sharp
        from okcolors.palettes import sharp

        variant_colors = sharp.get_colors(bg_dark=tinter(0.00), bg_light=tinter(1.00))

    # Sharp dark starts at true black; boost surface to L=0.20
    # so the ladder sits above the range where screens can't show
    # discernible differences.
    surface_L = 0.20 if high_contrast and kind == "dark" else None

    return get_roles(
        color_palette=variant_colors,
        base_tinter=tinter,
        kind=kind,
        bg_L=bg_L,
        bg_step=bg_step,
        surface_L=surface_L,
    )


class ColorReport(TypedDict):
    role: str
    L: float
    C: float
    h: float
    hex: str
    apca_lc: float
    wcag: float


def colorscheme_report(scheme: ColorPalette) -> list[ColorReport]:
    """Return per-color contrast metrics for every role in *scheme*.

    Contrast is measured against the scheme's ``bg`` color.
    """
    bg: Color = scheme.colors["bg"]
    rows: list[ColorReport] = []
    for role, color in scheme.colors.items():
        lch = color.to_oklch()
        rows.append(
            ColorReport(
                role=role,
                L=round(lch.L, 4),
                C=round(lch.C, 4),
                h=round(lch.h, 1),
                hex=color.to_hex(),
                apca_lc=round(apca_contrast(color, bg), 2),
                wcag=round(wcag_contrast(color, bg), 2),
            )
        )
    return rows
