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
    name = color_palette.name.split()[0] + " " + kind.title()
    pal = ColorPalette(colors=base_tones | accent_colors, name=name)
    return pal
