from typing import Literal, get_args

from okcolors.color import ColorPalette, Variant
from okcolors.palettes import OkColorPalette, get_base_palette, get_color_palette
from okcolors.schemes.roles import get_roles

__all__ = ["OkColorscheme", "get_colorscheme"]


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
