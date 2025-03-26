import json
import sys
from pathlib import Path
from typing import get_args

import click
from cattrs import unstructure
from jinja2 import Environment, FileSystemLoader

from okcolors.color import Variant
from okcolors.palettes import OkColorPalette, get_color_palette
from okcolors.schemes import OkColorscheme, get_colorscheme

# If we want to exclude a field from unstructuring, do this:
# c = cattrs.Converter()
# unst_hook = make_dict_unstructure_fn(ColorPalette, c, name=override(omit=True))
# c.register_unstructure_hook(ColorPalette, unst_hook)

palette_names = get_args(OkColorPalette)
scheme_names = get_args(OkColorscheme)
variant_names = get_args(Variant)


@click.command()
@click.argument("palette", type=click.Choice(palette_names), default="smooth")
@click.option("-f", "--format", type=click.Choice(["native", "hex"]), default="hex")
def export_palette(palette: OkColorPalette, format: str):
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
def export_colorscheme(colorscheme: OkColorscheme, variant: Variant, format: str):
    pal = get_colorscheme(name=colorscheme, kind=variant)
    if format == "hex":
        out = {"name": pal.name, "colors": pal.get_hex_colors()}
    else:
        out = unstructure(pal)
    pretty_out = json.dumps(out, indent=2)
    click.echo(pretty_out)


def render(
    template_path: Path | str, name: OkColorscheme = "smooth", kind: Variant = "dark"
):
    colorscheme = get_colorscheme(name=name, kind=kind)

    parsed_path = Path(template_path)
    if not parsed_path.is_file():
        raise FileNotFoundError(f"No such file: '{template_path}'")
    template_dir = parsed_path.parent
    template_name = parsed_path.name
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template(template_name)

    rendered = template.render(colors=colorscheme.get_hex_colors())
    return rendered


@click.command()
@click.argument("template_file", type=click.Path(exists=True, path_type=Path))
@click.option("-s", "--colorscheme", type=click.Choice(scheme_names), default="smooth")
@click.option("-v", "--variant", type=click.Choice(variant_names), default="dark")
def render_template(template_file: Path, colorscheme: OkColorscheme, variant: Variant):
    out = render(template_file, name=colorscheme, kind=variant)
    click.echo(out)


@click.command()
@click.argument("colorscheme", type=click.Choice(scheme_names), default="smooth")
@click.option("-v", "--variant", type=click.Choice(variant_names), default="dark")
def render_colorscheme_swatch(colorscheme: OkColorscheme, variant: Variant):
    try:
        from okcolors.viz import schemeplot
    except ImportError:
        raise RuntimeError("Visualization extras not present. Install `okcolors[viz]`")
    cs = get_colorscheme(name=colorscheme, kind=variant)
    fig = schemeplot(cs)
    outname = f"{cs.name.replace(' ', '_')}.png"
    fig.savefig(outname, dpi=200, bbox_inches="tight")
    print(f"Wrote {outname}", file=sys.stderr)
