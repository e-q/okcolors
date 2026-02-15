import pytest
from pytest import approx

from okcolors.color import OkLCh, sRGB
from okcolors.contrast import adjust_foreground_for_contrast, apca_contrast


def _hex(h: str) -> sRGB:
    return sRGB.from_hex(h)


def test_black_on_white():
    """Black text on white bg: maximum positive polarity (~106 Lc)."""
    lc = apca_contrast(_hex("#000000"), _hex("#ffffff"))
    assert lc == approx(106.0, abs=1.0)


def test_white_on_black():
    """White text on black bg: maximum negative polarity (~-108 Lc)."""
    lc = apca_contrast(_hex("#ffffff"), _hex("#000000"))
    assert lc == approx(-107.9, abs=1.0)


def test_same_color_returns_zero():
    assert apca_contrast(_hex("#ffffff"), _hex("#ffffff")) == 0.0
    assert apca_contrast(_hex("#000000"), _hex("#000000")) == 0.0
    assert apca_contrast(_hex("#888888"), _hex("#888888")) == 0.0


def test_polarity_sign():
    """Dark text on light bg is positive; light text on dark bg is negative."""
    white = _hex("#ffffff")
    dark = _hex("#222222")
    assert apca_contrast(dark, white) > 0  # dark fg, light bg → positive
    assert apca_contrast(white, dark) < 0  # light fg, dark bg → negative


def test_gray_on_white():
    """Mid-gray on white should give moderate positive contrast."""
    lc = apca_contrast(_hex("#888888"), _hex("#ffffff"))
    assert 50 < lc < 70


def test_symmetry_is_broken():
    """APCA is polarity-aware: swapping fg/bg does NOT just negate the value."""
    lc_forward = apca_contrast(_hex("#000000"), _hex("#ffffff"))
    lc_reverse = apca_contrast(_hex("#ffffff"), _hex("#000000"))
    assert abs(lc_forward) != approx(abs(lc_reverse), abs=0.5)


def test_accepts_non_srgb_input():
    """Should accept OkLCh (or any Color type) as input."""
    fg = OkLCh(0.0, 0.0, 0.0)  # black
    bg = OkLCh(1.0, 0.0, 0.0)  # white
    lc = apca_contrast(fg, bg)
    assert lc == approx(106.0, abs=1.0)


def test_low_contrast_clipped_to_zero():
    """Nearly identical colors should return 0 due to low-clip threshold."""
    a = _hex("#808080")
    b = _hex("#818181")
    assert apca_contrast(a, b) == 0.0


# --- adjust_foreground_for_contrast ---


def test_adjust_hits_target_on_light_bg():
    """Adjust achromatic fg to Lc 75 on white bg."""
    gray = _hex("#888888")
    white = _hex("#ffffff")
    result = adjust_foreground_for_contrast(gray, white, 75.0)
    assert apca_contrast(result, white) == approx(75.0, abs=0.5)


def test_adjust_hits_target_on_dark_bg():
    """Adjust achromatic fg to Lc -75 on black bg."""
    gray = _hex("#888888")
    black = _hex("#000000")
    result = adjust_foreground_for_contrast(gray, black, -75.0)
    assert apca_contrast(result, black) == approx(-75.0, abs=0.5)


def test_adjust_preserves_hue_and_chroma():
    """Only lightness should change; hue and chroma are preserved."""
    red = OkLCh(0.5, 0.15, 30.0)
    white = _hex("#ffffff")
    result = adjust_foreground_for_contrast(red, white, 60.0)
    assert result.C == red.C
    assert result.h == red.h
    assert result.L != red.L


def test_adjust_unreachable_raises():
    """Requesting an impossible Lc target should raise ValueError."""
    gray = _hex("#888888")
    white = _hex("#ffffff")
    with pytest.raises(ValueError, match="unreachable"):
        adjust_foreground_for_contrast(gray, white, -120.0)
