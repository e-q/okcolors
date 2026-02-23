from okcolors.color import ColorDict, ColorPalette, Variant
from okcolors.tones import (
    TintFn,
    ansi_lightnesses,
    background_lightnesses,
    text_lightnesses,
)

_ACCENT_NAMES = (
    "red",
    "orange",
    "yellow",
    "green",
    "cyan",
    "blue",
    "purple",
    "magenta",
)


def _accent_colors(color_palette: ColorPalette, dark: bool) -> ColorDict:
    suffix = "_light" if dark else "_dark"
    return {name: color_palette.colors[f"{name}{suffix}"] for name in _ACCENT_NAMES}


def get_roles(
    color_palette: ColorPalette,
    base_tinter: TintFn,
    kind: Variant,
    bg_L: float,
    bg_step: float,
    tx_lc: float = 100,
    subtle_lc: float = 85,
    muted_lc: float = 70,
    surface_L: float | None = None,
) -> ColorPalette:
    dark = kind == "dark"

    bg_ls = background_lightnesses(bg_L, bg_step, dark, surface_L=surface_L)
    tx_ls = text_lightnesses(bg_L, tx_lc, subtle_lc, muted_lc, dark)
    ansi_ls = ansi_lightnesses()

    all_ls = bg_ls | tx_ls | ansi_ls
    base_tones: ColorDict = {role: base_tinter(L) for role, L in all_ls.items()}

    name = color_palette.name.split()[0] + " " + kind.title()
    return ColorPalette(
        colors=base_tones | _accent_colors(color_palette, dark), name=name
    ).quantize()
