from typing import Literal, get_args

from okcolors.color import ColorPalette

from . import base, base_mono, sharp, sharp_apca, smooth, smooth_apca, v1
from .base import tone_at as _tinted_tone_at
from .base_mono import tone_at as _mono_tone_at

__all__ = ["OkColorPalette", "get_base_tones", "get_color_palette", "get_tinter"]


OkColorPalette = Literal["sharp", "sharp-apca", "smooth", "smooth-apca", "v1"]


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
        case "sharp-apca":
            bp = get_base_palette(mono=True)
            palette = sharp_apca.get_colors(
                bg_dark=bp.colors["base_00"], bg_light=bp.colors["base_100"]
            )
        case "v1":
            palette = v1.get_colors()
        case _:
            raise ValueError(
                f"Unknown palette name, must be one of {get_args(OkColorPalette)}"
            )

    return palette


def get_tinter(mono: bool = False):
    """Return the tone_at function for chromatic or achromatic base tones."""
    return _mono_tone_at if mono else _tinted_tone_at


def get_base_tones(lightnesses: dict[str, float], mono: bool = False) -> ColorPalette:
    """Build a base palette from a ``{role: L}`` mapping."""
    if mono:
        return base_mono.get_tones(lightnesses)
    return base.get_tones(lightnesses)


def get_base_palette(mono: bool = False) -> ColorPalette:
    palette = base_mono.get_colors() if mono else base.get_colors()
    return palette
