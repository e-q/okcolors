from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from okcolors.color import Variant
from okcolors.schemes import OkColorscheme, get_colorscheme


def render(
    template_path: Path | str, name: OkColorscheme = "smooth", kind: Variant = "dark"
) -> str:
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
