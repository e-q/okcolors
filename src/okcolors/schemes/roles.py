from okcolors.color import ColorPalette, Variant


def get_roles(
    color_palette: ColorPalette,
    base_palette: ColorPalette,
    kind: Variant,
    high_contrast: bool,
) -> ColorPalette:
    match kind:
        case "dark":
            accent_colors = {
                "red": color_palette.colors["red_light"],
                "orange": color_palette.colors["orange_light"],
                "yellow": color_palette.colors["yellow_light"],
                "green": color_palette.colors["green_light"],
                "cyan": color_palette.colors["cyan_light"],
                "blue": color_palette.colors["blue_light"],
                "purple": color_palette.colors["purple_light"],
                "magenta": color_palette.colors["magenta_light"],
            }
            if high_contrast:
                base_tones = {
                    "bg": base_palette.colors["base_05"],
                    "surface": base_palette.colors["base_20"],
                    "overlay": base_palette.colors["base_30"],
                    "hilite_lo": base_palette.colors["base_25"],
                    "hilite_mid": base_palette.colors["base_35"],
                    "hilite_hi": base_palette.colors["base_45"],
                    "muted": base_palette.colors["base_75"],
                    "subtle": base_palette.colors["base_85"],
                    "tx": base_palette.colors["base_99"],
                    "black": base_palette.colors["base_10"],
                    "dark_grey": base_palette.colors["base_20"],
                    "lite_grey": base_palette.colors["base_90"],
                    "white": base_palette.colors["base_99"],
                }
            else:
                base_tones = {
                    "bg": base_palette.colors["base_20"],
                    "surface": base_palette.colors["base_23"],
                    "overlay": base_palette.colors["base_27"],
                    "hilite_lo": base_palette.colors["base_25"],
                    "hilite_mid": base_palette.colors["base_35"],
                    "hilite_hi": base_palette.colors["base_45"],
                    "muted": base_palette.colors["base_65"],
                    "subtle": base_palette.colors["base_75"],
                    "tx": base_palette.colors["base_90"],
                    "black": base_palette.colors["base_25"],
                    "dark_grey": base_palette.colors["base_35"],
                    "lite_grey": base_palette.colors["base_80"],
                    "white": base_palette.colors["base_90"],
                }
        case "light":
            accent_colors = {
                "red": color_palette.colors["red_dark"],
                "orange": color_palette.colors["orange_dark"],
                "yellow": color_palette.colors["yellow_dark"],
                "green": color_palette.colors["green_dark"],
                "cyan": color_palette.colors["cyan_dark"],
                "blue": color_palette.colors["blue_dark"],
                "purple": color_palette.colors["purple_dark"],
                "magenta": color_palette.colors["magenta_dark"],
            }
            if high_contrast:
                base_tones = {
                    "bg": base_palette.colors["base_99"],
                    "surface": base_palette.colors["base_95"],
                    "overlay": base_palette.colors["base_85"],
                    "hilite_lo": base_palette.colors["base_90"],
                    "hilite_mid": base_palette.colors["base_80"],
                    "hilite_hi": base_palette.colors["base_70"],
                    "muted": base_palette.colors["base_45"],
                    "subtle": base_palette.colors["base_35"],
                    "tx": base_palette.colors["base_05"],
                    "black": base_palette.colors["base_05"],
                    "dark_grey": base_palette.colors["base_15"],
                    "lite_grey": base_palette.colors["base_85"],
                    "white": base_palette.colors["base_95"],
                }
            else:
                base_tones = {
                    "bg": base_palette.colors["base_99"],
                    "surface": base_palette.colors["base_96"],
                    "overlay": base_palette.colors["base_92"],
                    "hilite_lo": base_palette.colors["base_94"],
                    "hilite_mid": base_palette.colors["base_85"],
                    "hilite_hi": base_palette.colors["base_75"],
                    "muted": base_palette.colors["base_55"],
                    "subtle": base_palette.colors["base_45"],
                    "tx": base_palette.colors["base_30"],
                    "black": base_palette.colors["base_30"],
                    "dark_grey": base_palette.colors["base_40"],
                    "lite_grey": base_palette.colors["base_85"],
                    "white": base_palette.colors["base_95"],
                }
    name = color_palette.name.split()[0] + " " + kind.title()
    pal = ColorPalette(colors=base_tones | accent_colors, name=name)
    return pal
