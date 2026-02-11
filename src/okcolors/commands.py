import csv
import io
import json
import sys
from pathlib import Path
from typing import get_args

import click
from cattrs import unstructure

from okcolors.color import Variant
from okcolors.palettes import OkColorPalette, get_color_palette
from okcolors.schemes import OkColorscheme, colorscheme_report, get_colorscheme
from okcolors.template import render

# If we want to exclude a field from unstructuring, do this:
# c = cattrs.Converter()
# unst_hook = make_dict_unstructure_fn(ColorPalette, c, name=override(omit=True))
# c.register_unstructure_hook(ColorPalette, unst_hook)

palette_names: tuple[str] = get_args(OkColorPalette)
scheme_names: tuple[str] = get_args(OkColorscheme)
variant_names: tuple[str] = get_args(Variant)


@click.command()
@click.argument("palette", type=click.Choice(palette_names), default="smooth")
@click.option("-f", "--format", type=click.Choice(["native", "hex"]), default="hex")
def export_palette(palette: OkColorPalette, format: str) -> None:
    pal = get_color_palette(palette)
    if format == "hex":
        out = {"name": pal.name, "colors": pal.get_hex_colors()}
    else:
        out = unstructure(pal)
    pretty_out = json.dumps(out, indent=2)
    click.echo(pretty_out)


@click.command()
@click.argument("colorscheme", type=click.Choice(scheme_names), default="smooth")
@click.option("-v", "--variant", type=click.Choice(variant_names), default="dark")
@click.option("-f", "--format", type=click.Choice(["native", "hex"]), default="hex")
def export_colorscheme(
    colorscheme: OkColorscheme, variant: Variant, format: str
) -> None:
    pal = get_colorscheme(name=colorscheme, kind=variant)
    if format == "hex":
        out = {"name": pal.name, "colors": pal.get_hex_colors()}
    else:
        out = unstructure(pal)
    pretty_out = json.dumps(out, indent=2)
    click.echo(pretty_out)


@click.command()
@click.argument("template_file", type=click.Path(exists=True, path_type=Path))
@click.option("-s", "--colorscheme", type=click.Choice(scheme_names), default="smooth")
@click.option("-v", "--variant", type=click.Choice(variant_names), default="dark")
def render_template(
    template_file: Path, colorscheme: OkColorscheme, variant: Variant
) -> None:
    out = render(template_file, name=colorscheme, kind=variant)
    click.echo(out)


@click.command()
@click.argument("colorscheme", type=click.Choice(scheme_names), default="smooth")
@click.option("-v", "--variant", type=click.Choice(variant_names), default="dark")
def export_colorscheme_csv(colorscheme: OkColorscheme, variant: Variant) -> None:
    scheme = get_colorscheme(name=colorscheme, kind=variant)
    rows = colorscheme_report(scheme)
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    click.echo(buf.getvalue(), nl=False)


@click.command()
@click.argument("colorscheme", type=click.Choice(scheme_names), default="smooth")
@click.option("-v", "--variant", type=click.Choice(variant_names), default="dark")
def render_colorscheme_swatch(colorscheme: OkColorscheme, variant: Variant) -> None:
    try:
        from okcolors.viz import schemeplot
    except ImportError as e:
        raise RuntimeError(
            "Visualization extras not present. Install `okcolors[viz]`"
        ) from e
    cs = get_colorscheme(name=colorscheme, kind=variant)
    fig, _ = schemeplot(cs)
    outname = f"{cs.name.replace(' ', '_')}.png"
    fig.savefig(outname, dpi=200, bbox_inches="tight")
    print(f"Wrote {outname}", file=sys.stderr)


@click.command()
@click.argument("colorscheme", type=click.Choice(scheme_names), default="smooth")
@click.option("-v", "--variant", type=click.Choice(variant_names), default="dark")
def render_contrast_grid(colorscheme: OkColorscheme, variant: Variant) -> None:
    try:
        from okcolors.viz import contrast_grid
    except ImportError as e:
        raise RuntimeError(
            "Visualization extras not present. Install `okcolors[viz]`"
        ) from e
    cs = get_colorscheme(name=colorscheme, kind=variant)
    fig, _ = contrast_grid(cs)
    outname = f"{cs.name.replace(' ', '_')}_contrast_grid.png"
    fig.savefig(outname, dpi=200, bbox_inches="tight")
    print(f"Wrote {outname}", file=sys.stderr)
