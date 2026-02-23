from itertools import product

from okcolors.contrast import apca_contrast
from okcolors.palettes import get_color_palette
from okcolors.schemes import get_colorscheme

SCHEME_NAMES = ["smooth", "sharp"]
EXPECTED_VARIANTS = ["dark", "light"]
ACCENT_ROLES = ["red", "orange", "yellow", "green", "cyan", "blue", "purple", "magenta"]


def test_get_color_palette():
    for name in SCHEME_NAMES:
        _ = get_color_palette(name)  # type: ignore[reportArgumentType]


def test_get_colorscheme():
    for name, var in product(SCHEME_NAMES, EXPECTED_VARIANTS):
        _ = get_colorscheme(name, var)


def test_contrast_floor_against_hilite_hi():
    """All foreground roles (accents and muted) must achieve |Lc| >= 45 against hilite_hi."""
    fg_roles = [*ACCENT_ROLES, "muted"]
    for name, var in product(SCHEME_NAMES, EXPECTED_VARIANTS):
        cs = get_colorscheme(name, var)
        hilite_hi = cs.colors["hilite_hi"]
        for role in fg_roles:
            lc = apca_contrast(cs.colors[role], hilite_hi)
            assert abs(lc) >= 45, (
                f"{name} {var}: |Lc| of {role} vs hilite_hi is {abs(lc):.1f}, expected >= 45"
            )
