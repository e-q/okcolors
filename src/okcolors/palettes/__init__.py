from typing import Literal, get_args

from okcolors.color import ColorPalette

from . import base, base_mono, sharp, smooth, v1

__all__ = ["OkColorPalette", "get_color_palette"]


OkColorPalette = Literal["sharp", "smooth", "v1"]


def get_color_palette(name: OkColorPalette) -> ColorPalette:
    match name.casefold():
        case "smooth":
            palette = smooth.get_colors()
        case "sharp":
            palette = sharp.get_colors()
        case "v1":
            palette = v1.get_colors()
        case _:
            raise ValueError(
                f"Unknown palette name, must be one of {get_args(OkColorPalette)}"
            )

    return palette


def get_base_palette(mono: bool = False) -> ColorPalette:
    if mono:
        palette = base_mono.get_colors()
    else:
        palette = base.get_colors()

    return palette
