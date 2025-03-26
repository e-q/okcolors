from attrs import astuple
from hypothesis import given
from hypothesis import strategies as st
from pytest import approx

from okcolors import color


@given(r=st.floats(0, 1), g=st.floats(0, 1), b=st.floats(0, 1))
def test_rgb_float_roundtrip(r, g, b):
    c_in = color.sRGB(r, g, b)
    c_oklch = c_in.to_oklch()
    c_out = c_oklch.to_srgb()
    # RGB precision, 1/255 ~ 4e-3
    assert astuple(c_out) == approx(astuple(c_in), abs=1e-4, rel=1e-3)


@given(r=st.integers(0, 255), g=st.integers(0, 255), b=st.integers(0, 255))
def test_rgb_hex_roundtrip(r, g, b):
    hex = f"#{r:02x}{g:02x}{b:02x}"
    c_in = color.sRGB.from_hex(hex)
    c_oklch = c_in.to_oklch()
    c_out = c_oklch.to_srgb()
    assert c_out.to_hex() == hex
