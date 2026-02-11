from typing import Literal, get_args

from okcolors.color import ColorPalette

from . import base, base_mono, sharp, smooth, smooth_apca, v1

__all__ = ["OkColorPalette", "get_color_palette"]


OkColorPalette = Literal["sharp", "smooth", "smooth-apca", "v1"]


def get_color_palette(name: OkColorPalette) -> ColorPalette:
    match name.casefold():
        case "smooth":
            palette = smooth.get_colors()
        case "smooth-apca":
            bp = get_base_palette()
            palette = smooth_apca.get_colors(
                bg_dark=bp.colors["base_20"], bg_light=bp.colors["base_99"]
            )
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
    palette = base_mono.get_colors() if mono else base.get_colors()

    return palette
