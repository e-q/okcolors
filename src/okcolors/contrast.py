"""APCA-W3 contrast calculation (version 0.0.98G-4g).

Attempt at a faithful implementation of the APCA (Accessible Perceptual
Contrast Algorithm) by Andrew Somers / Myndex Research.

Reference: https://github.com/Myndex/SAPC-APCA
"""

from __future__ import annotations

from okcolors.color import Color, OkLCh, srgb_to_linear

# sRGB to Y (luminance) coefficients
_Y_R = 0.2126729
_Y_G = 0.7151522
_Y_B = 0.0721750

# Soft clamp for near-black
_SOFT_CLAMP = 0.022
_SOFT_EXP = 1.414

# Normal polarity: light text on dark background (bg darker)
_NTX = 0.57
_NBG = 0.56
_NOFF = 0.027

# Reverse polarity: dark text on light background (bg lighter)
_RTX = 0.62
_RBG = 0.65
_ROFF = 0.027

_SCALE = 1.14
_LOW_CLIP = 0.1
_DELTA_Y_MIN = 0.0005


def _srgb_to_y(r: float, g: float, b: float) -> float:
    """Convert sRGB [0,1] to APCA luminance Y."""
    return (
        _Y_R * srgb_to_linear(r) + _Y_G * srgb_to_linear(g) + _Y_B * srgb_to_linear(b)
    )


def _soft_clamp(y: float) -> float:
    if y < _SOFT_CLAMP:
        return y + (_SOFT_CLAMP - y) ** _SOFT_EXP
    return y


def apca_contrast(fg_color: Color, bg_color: Color) -> float:
    """
    Compute APCA Lc (lightness contrast) for text on background.

    Returns a signed float roughly in [-108, 106].
    Positive = dark text on light bg; Negative = light text on dark bg.
    """
    fg_srgb = fg_color.to_srgb()
    bg_srgb = bg_color.to_srgb()

    y_fg = _srgb_to_y(fg_srgb.r, fg_srgb.g, fg_srgb.b)
    y_bg = _srgb_to_y(bg_srgb.r, bg_srgb.g, bg_srgb.b)

    # Soft clamp near-black luminances
    y_fg = _soft_clamp(y_fg)
    y_bg = _soft_clamp(y_bg)

    # Bail out if luminances are too close
    if abs(y_bg - y_fg) < _DELTA_Y_MIN:
        return 0.0

    # Normal polarity: bg is lighter than fg
    if y_bg > y_fg:
        sapc = (y_bg**_NBG - y_fg**_NTX) * _SCALE
        if sapc < _LOW_CLIP:
            return 0.0
        return (sapc - _NOFF) * 100.0
    else:
        # Reverse polarity: fg is lighter than bg
        sapc = (y_bg**_RBG - y_fg**_RTX) * _SCALE
        if sapc > -_LOW_CLIP:
            return 0.0
        return (sapc + _ROFF) * 100.0


def adjust_foreground_for_contrast(
    fg_color: Color, bg_color: Color, target_lc: float, *, tol: float = 0.1
) -> OkLCh:
    """
    Return a new foreground color that achieves *target_lc* APCA contrast
    against *bg_color*, derived from *fg_color* by adjusting only its OkLCh
    lightness (preserving hue and chroma as much as gamut allows).

    Uses bisection on OkLCh L. The result is an OkLCh color within *tol* Lc
    of the target. Raises ValueError if the target is unreachable at any L.
    """
    fg_lch = fg_color.to_oklch()
    C, h = fg_lch.C, fg_lch.h

    # apca_contrast is monotonically decreasing in fg lightness:
    #   L=0 gives maximum positive Lc, L=1 gives maximum negative Lc.
    lc_at_zero = apca_contrast(OkLCh(0.0, C, h), bg_color)
    lc_at_one = apca_contrast(OkLCh(1.0, C, h), bg_color)

    # Check reachability
    lc_lo = min(lc_at_zero, lc_at_one)
    lc_hi = max(lc_at_zero, lc_at_one)
    if target_lc > lc_hi + tol or target_lc < lc_lo - tol:
        raise ValueError(
            f"Target Lc {target_lc} is unreachable; achievable range is "
            f"[{lc_lo:.1f}, {lc_hi:.1f}] for this fg/bg combination."
        )

    lo, hi = 0.0, 1.0
    for _ in range(64):
        mid = (lo + hi) / 2
        lc = apca_contrast(OkLCh(mid, C, h), bg_color)
        if abs(lc - target_lc) < tol:
            return OkLCh(mid, C, h)
        # Monotonically decreasing: if lc is too high, increase L
        if lc > target_lc:
            lo = mid
        else:
            hi = mid

    return OkLCh((lo + hi) / 2, C, h)
