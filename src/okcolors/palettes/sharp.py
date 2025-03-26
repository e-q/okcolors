from okcolors.color import ColorPalette, OkLCh


def get_colors() -> ColorPalette:
    L_dark = 0.6
    L_light = 0.78

    palette = ColorPalette(
        name="OkColors-Sharp Accent Colors",
        colors=dict(
            magenta_dark=OkLCh(L_dark, 0.2, 342),
            red_dark=OkLCh(L_dark, 0.2, 18),
            orange_dark=OkLCh(L_dark, 0.15, 54),
            yellow_dark=OkLCh(L_dark, 0.12, 90),
            green_dark=OkLCh(L_dark, 0.16, 150),
            cyan_dark=OkLCh(L_dark, 0.1, 210),
            blue_dark=OkLCh(L_dark, 0.15, 270),
            purple_dark=OkLCh(L_dark, 0.21, 306),
            magenta_light=OkLCh(L_light, 0.17, 342),
            red_light=OkLCh(L_light, 0.12, 18),
            orange_light=OkLCh(L_light, 0.14, 54),
            yellow_light=OkLCh(L_light, 0.15, 90),
            green_light=OkLCh(L_light, 0.21, 150),
            cyan_light=OkLCh(L_light, 0.13, 210),
            blue_light=OkLCh(L_light, 0.11, 270),
            purple_light=OkLCh(L_light, 0.14, 306),
        ),
    )

    return palette
