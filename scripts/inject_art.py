"""Inject regenerated banner_logo + banner_hero into the skin YAMLs under skins/.

Idempotent — replaces the existing block-scalar values for both keys.
Uses ruamel-style block scalars by hand to keep formatting predictable
without adding a YAML library dependency at write time.
"""
from pathlib import Path
import re

ROOT     = Path(__file__).resolve().parent.parent
SKINS    = ROOT / "skins"
PREVIEWS = ROOT / "assets" / "previews"

# Variant of the kanji block-letter logo to inject (A | B | C)
INJECT_VARIANT = "A_kanji_en"

PAIRS = (
    # (skin_filename, logo_preview, hero_preview)
    ("kanagawa-canvas.yaml", f"banner_{INJECT_VARIANT}_canvas.txt", "canvas_hero.txt"),
    ("kanagawa-ink.yaml",   f"banner_{INJECT_VARIANT}_ink.txt",   "ink_hero.txt"),
)

LOGO_HEADER = "# Block-letter banner — 神奈川-AGENT (Kanagawa Agent)"
HERO_HEADER = (
    "# Hokusai's Great Wave off Kanagawa — palette-quantized braille.\n"
    "# Replace freely; kanji caption is 神奈川沖浪裏 (Under the Wave off Kanagawa)."
)

def replace_block(text: str, key: str, header: str, body: str) -> str:
    """Replace the entire `key: |` block (including header comments above it).

    Strategy: find the block anchor (`{key}: |`), then walk backward over
    consecutive comment lines that immediately precede it (those are the
    "header" comments we own). Forward, consume all subsequent indented
    lines until we hit a non-indented non-blank line or EOF.
    """
    indented_body = "\n".join("  " + ln for ln in body.splitlines())
    new_block = f"{header}\n{key}: |\n{indented_body}\n"

    # Locate the key anchor
    anchor_re = re.compile(rf"^{re.escape(key)}: \|\s*$", re.MULTILINE)
    m = anchor_re.search(text)
    if m is None:
        # Append at end with a blank-line separator
        sep = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
        return text.rstrip() + "\n\n" + new_block

    # Walk backward over comment / header lines we own
    start = m.start()
    pre = text[:start].rstrip("\n")
    pre_lines = pre.split("\n") if pre else []
    drop_from = len(pre_lines)
    while drop_from > 0:
        line = pre_lines[drop_from - 1]
        # Stop on first non-comment, non-blank line above the block
        if line.strip().startswith("#") or line.strip() == "":
            drop_from -= 1
            # Don't consume comments separated from our key by a blank-then-other-content;
            # we only walk contiguous blank/comment lines.
            continue
        break
    pre_lines = pre_lines[:drop_from]
    head = "\n".join(pre_lines).rstrip("\n")

    # Walk forward over the block body (indented lines)
    rest = text[m.end():].lstrip("\n").splitlines(keepends=True)
    consumed = 0
    while consumed < len(rest):
        ln = rest[consumed]
        if ln.startswith("  ") or ln.strip() == "":
            consumed += 1
            continue
        break
    tail = "".join(rest[consumed:])

    # Reassemble — single blank line between sections
    parts = []
    if head:
        parts.append(head)
        parts.append("")
    parts.append(new_block.rstrip())
    if tail:
        parts.append("")
        parts.append(tail.rstrip())
    return "\n".join(parts) + "\n"

for skin_file, logo_preview, hero_preview in PAIRS:
    skin_path = SKINS / skin_file
    text = skin_path.read_text()
    logo = (PREVIEWS / logo_preview).read_text().rstrip("\n")
    hero = (PREVIEWS / hero_preview).read_text().rstrip("\n")
    text = replace_block(text, "banner_logo", LOGO_HEADER, logo)
    text = replace_block(text, "banner_hero", HERO_HEADER, hero)
    skin_path.write_text(text)
    print(f"updated {skin_path}")

# Sanity: re-parse with PyYAML if available
try:
    import yaml
    for skin_file, *_ in PAIRS:
        d = yaml.safe_load((SKINS / skin_file).read_text())
        print(
            f"  {skin_file}: logo={len(d.get('banner_logo','').splitlines())} lines · "
            f"hero={len(d.get('banner_hero','').splitlines())} lines"
        )
except ImportError:
    print("  (install PyYAML to verify YAML structure)")
