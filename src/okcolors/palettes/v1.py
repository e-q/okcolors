from okcolors.color import ColorPalette, OkLCh


def get_colors() -> ColorPalette:
    L_dark = 0.55  # dL = +.44, hits Lc60
    L_light = 0.78  # dL = -.58, slight boost for light-on_dark
    C_base = 0.1

    palette = ColorPalette(
        name="OkColors-v1 Accent Colors",
        colors=dict(
            magenta_dark=OkLCh(L_dark, 0.2, 342),
            red_dark=OkLCh(L_dark, 0.2, 18),
            orange_dark=OkLCh(L_dark, C_base, 54),
            yellow_dark=OkLCh(L_dark, C_base, 90),
            green_dark=OkLCh(L_dark, C_base, 162),
            cyan_dark=OkLCh(L_dark, C_base, 198),
            blue_dark=OkLCh(L_dark, C_base, 234),
            purple_dark=OkLCh(L_dark, C_base, 306),
            magenta_light=OkLCh(L_light, 0.17, 342),
            red_light=OkLCh(L_light, 0.125, 18),
            orange_light=OkLCh(L_light, C_base, 54),
            yellow_light=OkLCh(L_light, C_base, 90),
            green_light=OkLCh(L_light, C_base, 162),
            cyan_light=OkLCh(L_light, C_base, 198),
            blue_light=OkLCh(L_light, C_base, 234),
            purple_light=OkLCh(L_light, C_base, 306),
        ),
    )
    return palette
