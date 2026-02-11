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
    )


# --- Legacy path (smooth, sharp, v1) — remove when fully migrated to APCA --- #


def get_roles_legacy(
    color_palette: ColorPalette,
    base_palette: ColorPalette,
    kind: Variant,
    high_contrast: bool,
) -> ColorPalette:
    match kind:
        case "dark":
            if high_contrast:
                base_tones = {
                    "bg": base_palette.colors["base_00"],
                    "surface": base_palette.colors["base_33"],
                    "overlay": base_palette.colors["base_44"],
                    "hilite_lo": base_palette.colors["base_39"],
                    "hilite_mid": base_palette.colors["base_49"],
                    "hilite_hi": base_palette.colors["base_53"],
                    "muted": base_palette.colors["base_85"],
                    "subtle": base_palette.colors["base_92"],
                    "tx": base_palette.colors["base_97"],
                    "black": base_palette.colors["base_25"],
                    "dark_grey": base_palette.colors["base_35"],
                    "lite_grey": base_palette.colors["base_80"],
                    "white": base_palette.colors["base_90"],
                }
            else:
                base_tones = {
                    "bg": base_palette.colors["base_20"],
                    "surface": base_palette.colors["base_33"],
                    "overlay": base_palette.colors["base_44"],
                    "hilite_lo": base_palette.colors["base_39"],
                    "hilite_mid": base_palette.colors["base_49"],
                    "hilite_hi": base_palette.colors["base_53"],
                    "muted": base_palette.colors["base_85"],
                    "subtle": base_palette.colors["base_92"],
                    "tx": base_palette.colors["base_97"],
                    "black": base_palette.colors["base_25"],
                    "dark_grey": base_palette.colors["base_35"],
                    "lite_grey": base_palette.colors["base_80"],
                    "white": base_palette.colors["base_90"],
                }
        case "light":
            if high_contrast:
                base_tones = {
                    "bg": base_palette.colors["base_100"],
                    "surface": base_palette.colors["base_98"],
                    "overlay": base_palette.colors["base_93"],
                    "hilite_lo": base_palette.colors["base_95"],
                    "hilite_mid": base_palette.colors["base_90"],
                    "hilite_hi": base_palette.colors["base_87"],
                    "muted": base_palette.colors["base_54"],
                    "subtle": base_palette.colors["base_41"],
                    "tx": base_palette.colors["base_31"],
                    "black": base_palette.colors["base_25"],
                    "dark_grey": base_palette.colors["base_35"],
                    "lite_grey": base_palette.colors["base_80"],
                    "white": base_palette.colors["base_90"],
                }
            else:
                base_tones = {
                    "bg": base_palette.colors["base_99"],
                    "surface": base_palette.colors["base_96"],
                    "overlay": base_palette.colors["base_91"],
                    "hilite_lo": base_palette.colors["base_94"],
                    "hilite_mid": base_palette.colors["base_89"],
                    "hilite_hi": base_palette.colors["base_86"],
                    "muted": base_palette.colors["base_52"],
                    "subtle": base_palette.colors["base_39"],
                    "tx": base_palette.colors["base_27"],
                    "black": base_palette.colors["base_25"],
                    "dark_grey": base_palette.colors["base_35"],
                    "lite_grey": base_palette.colors["base_80"],
                    "white": base_palette.colors["base_90"],
                }
    dark = kind == "dark"
    name = color_palette.name.split()[0] + " " + kind.title()
    return ColorPalette(
        colors=base_tones | _accent_colors(color_palette, dark), name=name
    )
