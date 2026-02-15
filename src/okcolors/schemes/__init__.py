from typing import Literal, TypedDict, get_args

from okcolors.color import Color, ColorPalette, Variant
from okcolors.contrast import apca_contrast, wcag_contrast
from okcolors.palettes import OkColorPalette, get_base_palette, get_color_palette
from okcolors.schemes.roles import get_roles

__all__ = ["OkColorscheme", "colorscheme_report", "get_colorscheme"]


OkColorscheme = Literal["sharp", "smooth", "v1"]


def get_colorscheme(
    name: OkColorPalette = "smooth", kind: Variant = "dark"
) -> ColorPalette:
    if name not in get_args(OkColorscheme):
        raise ValueError(
            f"Unknown colorscheme name, must be one of {get_args(OkColorscheme)}"
        )
    high_contrast = name == "sharp"
    variant_colors = get_color_palette(name)
    base_palette = get_base_palette(mono=high_contrast)
    colorscheme = get_roles(
        color_palette=variant_colors,
        base_palette=base_palette,
        kind=kind,
        high_contrast=high_contrast,
    )
    return colorscheme


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
