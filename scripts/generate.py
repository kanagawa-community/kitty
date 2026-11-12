#!/usr/bin/env python3
"""Write themes/kanagawa-<variant>.conf from the shared palette.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]
ANSI = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]

# kitty color -> palette role.
SIMPLE = {
    "background": "ui.bg",
    "foreground": "ui.fg",
    "selection_background": "ui.bg_visual",
    "selection_foreground": "ui.fg",
    "cursor": "ui.fg_dim",
    "cursor_text_color": "ui.bg",
    "url_color": "syn.fun",
    "active_border_color": "ui.fg_dim",
    "inactive_border_color": "ui.nontext",
    "tab_bar_background": "ui.bg_m3",
    "active_tab_background": "ui.bg_p2",
    "active_tab_foreground": "ui.fg",
    "inactive_tab_background": "ui.bg_m3",
    "inactive_tab_foreground": "ui.fg_dim",
}
# color0-15 are the ANSI colors, color16-17 the two extended colors.
COLORS = [f"term.{c}" for c in ANSI] + [f"term.bright_{c}" for c in ANSI]
COLORS += ["term.extended_1", "term.extended_2"]


def roles(variant):
    """Map each role to its hex color; a role missing from the palette raises KeyError later."""
    return {role: c["hex"] for c in variant["colors"].values() for role in c["usage"]}


def theme(variant, appearance, colors):
    out = [
        "# vim:ft=kitty",
        "",
        f"## name: Kanagawa {variant.capitalize()}",
        "## author: Kanagawa Community",
        "## license: MIT",
        "## upstream: https://github.com/kanagawa-community/kitty",
        f"## blurb: Kanagawa {variant.capitalize()}, a {appearance} theme from the shared Kanagawa palette.",
        "",
    ]
    out += [f"{k} {colors[role]}" for k, role in SIMPLE.items()]
    out += [f"color{i} {colors[role]}" for i, role in enumerate(COLORS)]
    return "\n".join(out) + "\n"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        out = ROOT / "themes" / f"kanagawa-{v}.conf"
        out.parent.mkdir(exist_ok=True)
        out.write_text(theme(v, variants[v]["appearance"], roles(variants[v])))
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
