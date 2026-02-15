"""Compute OkLCh lightness values for semantic colorscheme roles.

Background roles are spaced by equal ΔL steps (perceptually uniform).
Text roles are placed by APCA contrast targets against the background.
"""

from __future__ import annotations

from collections.abc import Callable

from okcolors.color import OkLab, OkLCh
from okcolors.contrast import adjust_foreground_for_contrast

type TintFn = Callable[[float], OkLab]

_BG_ROLES = ("bg", "surface", "hilite_lo", "overlay", "hilite_mid", "hilite_hi")


def background_lightnesses(
    bg_L: float, step: float, dark: bool, *, surface_L: float | None = None
) -> dict[str, float]:
    """Return OkLab L values for background roles.

    Dark mode steps increase from *bg_L*; light mode steps decrease.
    If *surface_L* is given, surface jumps to that value and subsequent
    roles step from there (useful when bg sits in a range where screens
    can't show discernible differences).
    """
    sign = 1 if dark else -1
    result: dict[str, float] = {}
    L = bg_L
    for i, role in enumerate(_BG_ROLES):
        if i == 0:
            L = bg_L
        elif i == 1 and surface_L is not None:
            L = surface_L
        else:
            L += step * sign
        result[role] = L
    return result


def text_lightnesses(
    bg_L: float, tx_lc: float, subtle_lc: float, muted_lc: float, dark: bool
) -> dict[str, float]:
    """Return OkLab L values for text roles via APCA bisection.

    Targets are given as positive magnitudes.  In dark mode text is lighter
    than bg (negative APCA Lc); in light mode text is darker (positive Lc).
    """
    bg_color = OkLCh(bg_L, 0, 0)
    sign = -1 if dark else 1
    result: dict[str, float] = {}
    for role, target in (("tx", tx_lc), ("subtle", subtle_lc), ("muted", muted_lc)):
        adjusted = adjust_foreground_for_contrast(
            OkLCh(0.5, 0, 0), bg_color, sign * target
        )
        result[role] = adjusted.L
    return result


def ansi_lightnesses() -> dict[str, float]:
    """Return fixed OkLab L values for the four ANSI grey roles."""
    return {"black": 0.25, "dark_grey": 0.35, "lite_grey": 0.80, "white": 0.90}
