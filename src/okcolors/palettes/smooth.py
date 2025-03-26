from okcolors.color import ColorPalette, OkLCh


def get_colors() -> ColorPalette:
    # Hits Lc60, and achieves consistent chroma
    L_dark = 0.58
    # Draft WCAG3 is stricter on light-on-dark legibility, so lightnesses aren't
    # symmetric around the base tones.
    L_light = 0.78
    C_base = 0.1  # limited by cyan_dark

    palette = ColorPalette(
        name="OkColors-Smooth Accent Colors",
        colors=dict(
            magenta_dark=OkLCh(L_dark, 0.2, 342),
            red_dark=OkLCh(L_dark, 0.2, 18),
            orange_dark=OkLCh(L_dark, C_base, 54),
            yellow_dark=OkLCh(L_dark, C_base, 90),
            green_dark=OkLCh(L_dark, C_base, 150),
            cyan_dark=OkLCh(L_dark, C_base, 210),
            blue_dark=OkLCh(L_dark, C_base, 270),
            purple_dark=OkLCh(L_dark, C_base, 306),
            magenta_light=OkLCh(L_light, 0.17, 342),
            red_light=OkLCh(L_light, 0.125, 18),
            orange_light=OkLCh(L_light, C_base, 54),
            yellow_light=OkLCh(L_light, C_base, 90),
            green_light=OkLCh(L_light, C_base, 150),
            cyan_light=OkLCh(L_light, C_base, 210),
            blue_light=OkLCh(L_light, C_base, 270),
            purple_light=OkLCh(L_light, C_base, 306),
        ),
    )

    return palette
