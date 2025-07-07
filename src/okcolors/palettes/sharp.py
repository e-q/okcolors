from okcolors.color import ColorPalette, OkLCh


def get_colors() -> ColorPalette:
    L_dark = 0.53
    L_light = 0.85

    palette = ColorPalette(
        name="OkColors-Sharp Accent Colors",
        colors={
            "magenta_dark": OkLCh(L_dark, 0.2, 342),
            "red_dark": OkLCh(L_dark, 0.2, 18),
            "orange_dark": OkLCh(L_dark, 0.13, 54),
            "yellow_dark": OkLCh(L_dark, 0.1, 90),
            "green_dark": OkLCh(L_dark, 0.14, 150),
            "cyan_dark": OkLCh(L_dark, 0.09, 210),
            "blue_dark": OkLCh(L_dark, 0.2, 270),
            "purple_dark": OkLCh(L_dark, 0.2, 306),
            "magenta_light": OkLCh(L_light, 0.1, 342),
            "red_light": OkLCh(L_light, 0.08, 18),
            "orange_light": OkLCh(L_light, 0.09, 54),
            "yellow_light": OkLCh(L_light, 0.15, 90),
            "green_light": OkLCh(L_light, 0.15, 150),
            "cyan_light": OkLCh(L_light, 0.13, 210),
            "blue_light": OkLCh(L_light, 0.07, 270),
            "purple_light": OkLCh(L_light, 0.09, 306),
        },
    )

    return palette
