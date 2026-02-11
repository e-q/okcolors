from typing import Literal, get_args

from okcolors.color import ColorPalette, Variant
from okcolors.palettes import OkColorPalette, get_base_palette, get_color_palette
from okcolors.schemes.roles import get_roles

__all__ = ["OkColorscheme", "get_colorscheme"]


OkColorscheme = Literal["sharp", "sharp-apca", "smooth", "smooth-apca", "v1"]


def get_colorscheme(
    name: OkColorPalette = "smooth", kind: Variant = "dark"
) -> ColorPalette:
    if name not in get_args(OkColorscheme):
        raise ValueError(
            f"Unknown colorscheme name, must be one of {get_args(OkColorscheme)}"
        )
    high_contrast = name in ("sharp", "sharp-apca")
    base_palette = get_base_palette(mono=high_contrast)
    if name == "smooth-apca":
        from okcolors.palettes import smooth_apca

        bg_dark = base_palette.colors["base_20"]
        bg_light = base_palette.colors["base_99"]
        variant_colors = smooth_apca.get_colors(bg_dark=bg_dark, bg_light=bg_light)
    elif name == "sharp-apca":
        from okcolors.palettes import sharp_apca

        bg_dark = base_palette.colors["base_00"]
        bg_light = base_palette.colors["base_100"]
        variant_colors = sharp_apca.get_colors(bg_dark=bg_dark, bg_light=bg_light)
    else:
        variant_colors = get_color_palette(name)
    colorscheme = get_roles(
        color_palette=variant_colors,
        base_palette=base_palette,
        kind=kind,
        high_contrast=high_contrast,
    )
    return colorscheme
