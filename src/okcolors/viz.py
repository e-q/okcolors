import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.patches import Circle, Rectangle

from okcolors.color import ColorPalette


def palplot(pal: ColorPalette, bg: str = "#FFFFFF") -> tuple[Figure, Axes]:
    hex_d = {}
    for cname, c in pal.colors.items():
        hex_d[cname] = c.to_hex()

    n = len(hex_d)
    fig, ax = plt.subplots(
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
    return fig, ax


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


def schemeplot(colorscheme: ColorPalette) -> tuple[Figure, Axes]:
    if not all(c in colorscheme.colors for c in ["bg", "tx", *FOREGROUND_ROLES]):
        raise ValueError("Incomplete Colorscheme")

    hex_d = {cname: c.to_hex() for cname, c in colorscheme.colors.items()}

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
    return fig, ax


BACKGROUND_ROLES = ["bg", "surface", "overlay", "hilite_lo", "hilite_mid", "hilite_hi"]
TEXT_ROLES = ["tx", "subtle", "muted"]


def contrast_grid(colorscheme: ColorPalette) -> tuple[Figure, Axes]:
    fg_roles = TEXT_ROLES + FOREGROUND_ROLES
    bg_roles = BACKGROUND_ROLES

    hex_d = {cname: c.to_hex() for cname, c in colorscheme.colors.items()}

    n_rows = len(fg_roles)
    n_cols = len(bg_roles)
    cell_w, cell_h = 1.8, 0.5

    with mpl.rc_context(
        {
            "axes.spines.left": False,
            "axes.spines.bottom": False,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    ):
        fig, ax = plt.subplots(
            figsize=(n_cols * cell_w, n_rows * cell_h + 0.6), layout="constrained"
        )

    fig.set_facecolor(hex_d["bg"])
    ax.set_facecolor(hex_d["bg"])

    for row, fg_name in enumerate(fg_roles):
        y = n_rows - 1 - row
        for col, bg_name in enumerate(bg_roles):
            x = col * cell_w
            ax.add_patch(
                Rectangle(
                    (x, y * cell_h),
                    cell_w,
                    cell_h,
                    facecolor=hex_d[bg_name],
                    edgecolor="none",
                )
            )
            ax.text(
                x + cell_w / 2,
                y * cell_h + cell_h / 2,
                f"{fg_name} on {bg_name}",
                color=hex_d[fg_name],
                ha="center",
                va="center",
                fontsize=7,
                fontweight="bold",
            )

    ax.set_xlim(0, n_cols * cell_w)
    ax.set_ylim(0, n_rows * cell_h)
    ax.xaxis.set_major_locator(ticker.NullLocator())
    ax.yaxis.set_major_locator(ticker.NullLocator())

    if colorscheme.name is not None:
        ax.set_title(colorscheme.name, color=hex_d["tx"])

    return fig, ax
