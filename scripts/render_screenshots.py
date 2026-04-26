"""Render banner_logo + banner_hero from each skin into an SVG screenshot
using Rich's terminal_renderer (preserves all colors as inline CSS).
Outputs to assets/screenshots/{kanagawa-canvas,kanagawa-ink}.svg.
"""
from pathlib import Path
import sys
import yaml

ROOT     = Path(__file__).resolve().parent.parent
SKINS    = ROOT / "skins"
OUTDIR   = ROOT / "assets" / "screenshots"
OUTDIR.mkdir(parents=True, exist_ok=True)

# Use Rich from the Hermes venv if available; otherwise system rich.
sys.path.insert(0, "/Users/mpetters/.hermes/hermes-agent")
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.terminal_theme import TerminalTheme

# Build per-skin TerminalThemes so save_svg paints the proper canvas/ink bg
def make_theme(bg_hex: str, fg_hex: str) -> TerminalTheme:
    bg = tuple(int(bg_hex[i:i+2], 16) for i in (1, 3, 5))
    fg = tuple(int(fg_hex[i:i+2], 16) for i in (1, 3, 5))
    # 16 ANSI slots — values don't matter much because every glyph already
    # carries an explicit truecolor markup tag; just provide reasonable fills.
    palette = [bg, (0xc2,0x76,0x72), (0x7a,0x8c,0x6a), (0xa7,0x95,0x6a),
               (0x7e,0x8f,0xaf), (0x7b,0x95,0x8e), (0x9e,0x7e,0x98), fg,
               bg, (0xc2,0x76,0x72), (0x7a,0x8c,0x6a), (0xa7,0x95,0x6a),
               (0x7e,0x8f,0xaf), (0x7b,0x95,0x8e), (0x9e,0x7e,0x98), fg]
    return TerminalTheme(bg, fg, palette[:8], palette[8:])

THEMES = {
    "kanagawa-canvas": make_theme("#E1E1DE", "#73787D"),
    "kanagawa-ink":    make_theme("#1F1F28", "#DCD7BA"),
}

def render_skin(skin_name: str):
    data = yaml.safe_load((SKINS / f"{skin_name}.yaml").read_text())
    logo = data["banner_logo"].rstrip("\n")
    hero = data["banner_hero"].rstrip("\n")
    border = data["colors"]["banner_border"]
    title  = data["branding"]["agent_name"]
    welcome = data["branding"]["welcome"]

    console = Console(record=True, width=120, force_terminal=True, color_system="truecolor")
    console.print()
    console.print(Text.from_markup(logo))
    console.print()
    console.print(Text.from_markup(hero))
    console.print()
    console.print(Panel.fit(
        f"[bold]{title}[/]  ·  [{border}]{skin_name}[/]\n[dim]{welcome}[/]",
        border_style=border, padding=(0,2),
    ))

    out = OUTDIR / f"{skin_name}.svg"
    console.save_svg(
        str(out),
        title=f"Hermes Agent · {skin_name}",
        theme=THEMES[skin_name],
    )
    print(f"wrote {out}")

for name in ("kanagawa-canvas", "kanagawa-ink"):
    render_skin(name)
