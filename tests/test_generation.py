from itertools import product

from okcolors.palettes import get_color_palette
from okcolors.schemes import get_colorscheme

EXPECTED_NAMES = ["smooth", "sharp"]
EXPECTED_VARIANTS = ["dark", "light"]


def test_get_color_palette():
    for name in EXPECTED_NAMES:
        _ = get_color_palette(name)  # type: ignore


def test_get_colorscheme():
    for name, var in product(EXPECTED_NAMES, EXPECTED_VARIANTS):
        _ = get_colorscheme(name, var)  # type: ignore
