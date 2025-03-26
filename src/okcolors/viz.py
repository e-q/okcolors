import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.figure import Figure
from matplotlib.patches import Circle

from okcolors.color import ColorPalette, OkLab, OkLCh


def palplot(pal: ColorPalette, bg: str = "#FFFFFF"):
    hex_d = {}
    for cname, c in pal.colors.items():
        match c:
            case OkLCh() | OkLab():
                hex_d[cname] = c.to_srgb().to_hex()
            case _:
                hex_d[cname] = c.to_hex()

    n = len(hex_d)
    _, ax = plt.subplots(
        figsize=(n / 2, 1.2), layout="constrained", subplot_kw={"aspect": "equal"}
    )
    ax.set_facecolor(bg)
    for n, (cname, chex) in enumerate(hex_d.items()):
        ax.add_patch(Circle((n / 2, 0), radius=0.2, color=chex))
        ax.text(x=n / 2, y=-0.25, s=cname, va="top", ha="center", size="xx-small")

    if pal.name is not None:
        ax.set_title(pal.name)
    ax.set_xlim(-0.5, n / 2 + 0.5)
    ax.set_ylim(-0.5, 0.5)
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_major_locator(ticker.NullLocator())


FOREGROUND_ROLES = [
    "magenta",
    "red",
    "orange",
    "yellow",
    "green",
    "cyan",
    "blue",
    "purple",
]
N_COLORS = len(FOREGROUND_ROLES)


def schemeplot(colorscheme: ColorPalette) -> Figure:
    if not all(c in colorscheme.colors for c in ["bg", "tx", *FOREGROUND_ROLES]):
        raise ValueError("Incomplete Colorscheme")

    hex_d = {}
    for cname in colorscheme.colors:
        match c := colorscheme.colors[cname]:
            case OkLCh() | OkLab():
                hex_d[cname] = c.to_srgb().to_hex()
            case _:
                hex_d[cname] = c.to_hex()

    with mpl.rc_context(
        {
            "axes.spines.left": False,
            "axes.spines.bottom": False,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    ):
        fig, ax = plt.subplots(
            figsize=(N_COLORS / 2, 1.2),
            layout="constrained",
            subplot_kw={"aspect": "equal"},
        )
    fig.set_facecolor(hex_d["bg"])
    ax.set_facecolor(hex_d["bg"])
    for n, cname in enumerate(FOREGROUND_ROLES):
        ax.add_patch(Circle((n / 2, 0), radius=0.2, color=hex_d[cname]))

    if colorscheme.name is not None:
        ax.set_title(colorscheme.name, color=hex_d["tx"])
    ax.set_xlim(-0.25, (N_COLORS - 1) / 2 + 0.25)
    ax.set_ylim(-0.25, 0.25)
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_major_locator(ticker.NullLocator())
    return fig
