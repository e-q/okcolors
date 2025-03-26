"""Convenience classes for working with colors in different spaces."""

from __future__ import annotations

import math
from typing import Literal

from attrs import astuple, define, field, validators


def float_repr(n):
    return f"{n:.3f}"


def angle_repr(h):
    return f"{h:.0f}°"


type Color = sRGB | OkLab | OkLCh
type ColorDict = dict[str, Color]


@define
class sRGB:
    r: float = field(
        repr=float_repr, validator=[validators.ge(0.0), validators.le(1.0)]
    )
    g: float = field(
        repr=float_repr, validator=[validators.ge(0.0), validators.le(1.0)]
    )
    b: float = field(
        repr=float_repr, validator=[validators.ge(0.0), validators.le(1.0)]
    )

    @classmethod
    def from_hex(cls, hex_color: str) -> sRGB:
        if hex_color.startswith("#"):
            hex_color = hex_color[1:]

        # Handle both 3-digit and 6-digit hex codes
        if len(hex_color) == 3:
            # Expand 3-digit hex to 6-digit
            hex_color = "".join([c * 2 for c in hex_color])
        elif len(hex_color) != 6:
            raise ValueError(f"Invalid hex color format: {hex_color}")

        r = int(hex_color[0:2], 16) / 255.0
        g = int(hex_color[2:4], 16) / 255.0
        b = int(hex_color[4:6], 16) / 255.0
        return cls(r, g, b)

    def to_hex(self) -> str:
        r_int = round(self.r * 255)
        g_int = round(self.g * 255)
        b_int = round(self.b * 255)
        return f"#{r_int:02x}{g_int:02x}{b_int:02x}"

    def to_oklab(self) -> OkLab:
        Lab = srgb_to_oklab(*astuple(self))
        return OkLab(*Lab)

    def to_oklch(self) -> OkLCh:
        return self.to_oklab().to_oklch()


@define
class OkLab:
    L: float = field(
        repr=float_repr, validator=[validators.ge(0.0), validators.le(1.0)]
    )
    a: float = field(repr=float_repr)
    b: float = field(repr=float_repr)

    def to_oklch(self) -> OkLCh:
        C = math.sqrt(self.a**2 + self.b**2)
        h = math.atan2(self.b, self.a) / math.pi * 180
        return OkLCh(self.L, C, h)

    def to_srgb(self) -> sRGB:
        # Special case absolute white/black
        if self.L <= 0:
            rgb = (0, 0, 0)
        elif self.L >= 1.0:
            rgb = (1, 1, 1)
        else:
            rgb = oklab_to_srgb(*astuple(self))
        return sRGB(*rgb)

    def to_hex(self) -> str:
        return self.to_srgb().to_hex()


def wrap_degrees(a):
    return a - 360 * math.floor(a / 360)


@define
class OkLCh:
    L: float = field(
        repr=float_repr, validator=[validators.ge(0.0), validators.le(1.0)]
    )
    C: float = field(repr=float_repr, validator=validators.ge(0.0))
    h: float = field(repr=angle_repr, converter=wrap_degrees)

    def to_oklab(self) -> OkLab:
        h_rad = self.h / 180 * math.pi
        a = self.C * math.cos(h_rad)
        b = self.C * math.sin(h_rad)
        return OkLab(self.L, a, b)

    def to_srgb(self) -> sRGB:
        return self.to_oklab().to_srgb()

    def to_hex(self) -> str:
        return self.to_srgb().to_hex()


@define
class ColorPalette:
    colors: dict[str, Color]
    name: str

    def get_hex_colors(self) -> dict[str, str]:
        return {cname: c.to_hex() for cname, c in self.colors.items()}


Variant = Literal["dark", "light"]


# Following functions adapted from https://bottosson.github.io/posts/oklab/
# MIT License - Copyright (c) 2020 Björn Ottosson
def linear_to_srgb(c: float) -> float:
    if c <= 0.0031308:
        return 12.92 * c
    else:
        return 1.055 * c ** (1 / 2.4) - 0.055


def srgb_to_linear(c: float) -> float:
    if c <= 0.04045:
        return c / 12.92
    else:
        return ((c + 0.055) / 1.055) ** 2.4


def oklab_to_srgb(L: float, a: float, b: float) -> tuple[float, float, float]:
    # Convert from OkLab to linear RGB
    long_rt = L + 0.3963377774 * a + 0.2158037573 * b
    med_rt = L - 0.1055613458 * a - 0.0638541728 * b
    short_rt = L - 0.0894841775 * a - 1.2914855480 * b

    long = long_rt**3
    med = med_rt**3
    short = short_rt**3

    # Convert to linear RGB
    r_linear = +4.0767416621 * long - 3.3077115913 * med + 0.2309699292 * short
    g_linear = -1.2684380046 * long + 2.6097574011 * med - 0.3413193965 * short
    b_linear = -0.0041960863 * long - 0.7034186147 * med + 1.7076147010 * short

    # Apply gamma correction to get sRGB
    r_srgb = linear_to_srgb(r_linear)
    g_srgb = linear_to_srgb(g_linear)
    b_srgb = linear_to_srgb(b_linear)

    # Clamp values to [0, 1] range
    r_srgb = max(0, min(1, r_srgb))
    g_srgb = max(0, min(1, g_srgb))
    b_srgb = max(0, min(1, b_srgb))

    return (r_srgb, g_srgb, b_srgb)


def srgb_to_oklab(r: float, g: float, b: float) -> tuple[float, float, float]:
    # Convert from sRGB to linear RGB
    r_linear = srgb_to_linear(r)
    g_linear = srgb_to_linear(g)
    b_linear = srgb_to_linear(b)

    # Convert to LMS
    long = 0.4122214708 * r_linear + 0.5363325363 * g_linear + 0.0514459929 * b_linear
    med = 0.2119034982 * r_linear + 0.6806995451 * g_linear + 0.1073969566 * b_linear
    short = 0.0883024619 * r_linear + 0.2817188376 * g_linear + 0.6299787005 * b_linear

    # Non-linear transformation
    long_rt = long ** (1 / 3)
    med_rt = med ** (1 / 3)
    short_rt = short ** (1 / 3)

    # Convert to OkLab
    L = 0.2104542553 * long_rt + 0.7936177850 * med_rt - 0.0040720468 * short_rt
    a = 1.9779984951 * long_rt - 2.4285922050 * med_rt + 0.4505937099 * short_rt
    b = 0.0259040371 * long_rt + 0.7827717662 * med_rt - 0.8086757660 * short_rt

    return (L, a, b)
