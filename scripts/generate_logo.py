"""Render Japanese block-letter banners using half-block characters with a
3-stop vertical gradient that mirrors the wave hero. Outputs to assets/previews/.

Variants:
  A_kanji_en  神奈川-AGENT     (kanji + ASCII block "AGENT")
  B_full_jp   神奈川エージェント (all Japanese: kanji + katakana)
  C_hermes    ヘルメス-神奈川   (Hermes in katakana + Kanagawa)

Currently the active skins use variant A. To swap in B or C, change
INJECT_VARIANT in scripts/inject_art.py.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import re

ROOT   = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "assets" / "previews"
OUTDIR.mkdir(parents=True, exist_ok=True)

# macOS bundled bold Japanese font; fall back to Arial Unicode.
FONT_CANDIDATES = [
    "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]
FONT_PATH = next((p for p in FONT_CANDIDATES if Path(p).exists()), None)
if FONT_PATH is None:
    raise SystemExit("No Japanese-capable font found. Install a CJK TTF and update FONT_CANDIDATES.")

VARIANTS = {
    "A_kanji_en":   "神奈川-AGENT",
    "B_full_jp":    "神奈川エージェント",
    "C_hermes":     "ヘルメス-神奈川",
}

FONT_SIZE = 18
THRESHOLD = 130

# Gradient stops mirror the wave hero's color flow per palette
PALETTES = {
    "canvas": [   # foam → wave teal → deep blue
        "#7E8FAF",  # canvasTeal1 (crest highlight)
        "#6B8998",  # canvasBlue2 (wave body)
        "#516E7D",  # canvasBlue4 (deep water)
    ],
    "ink": [     # fuji white foam → dragon aqua → deep dragon blue
        "#DCD7BA",  # fujiWhite (crest)
        "#8EA49E",  # dragonAqua (mid wave)
        "#658594",  # dragonBlue (deep)
    ],
}

def render_text_to_pixels(text: str, font_path: str, font_size: int):
    font = ImageFont.truetype(font_path, font_size)
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0] + 4
    h = bbox[3] - bbox[1] + 4
    img = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(img)
    draw.text((-bbox[0]+2, -bbox[1]+2), text, fill=255, font=font)
    return img

def to_halfblock(img: Image.Image, threshold=THRESHOLD):
    px = img.load()
    w, h = img.size
    if h % 2:
        new = Image.new("L", (w, h+1), 0)
        new.paste(img, (0,0))
        img = new
        px = img.load()
        h = h+1
    rows_out = []
    for y in range(0, h, 2):
        line = []
        for x in range(w):
            top = px[x, y] >= threshold
            bot = px[x, y+1] >= threshold
            if top and bot: line.append("█")
            elif top:       line.append("▀")
            elif bot:       line.append("▄")
            else:           line.append(" ")
        rows_out.append("".join(line).rstrip())
    return rows_out

def colorize(rows, palette):
    n = len(rows)
    out = []
    for i, row in enumerate(rows):
        if not row.strip():
            out.append(row)
            continue
        if   i < n * 0.34: c = palette[0]
        elif i < n * 0.67: c = palette[1]
        else:              c = palette[2]
        out.append(f"[bold {c}]{row}[/]")
    return out

def render_variant(text: str, palette_name: str):
    img = render_text_to_pixels(text, FONT_PATH, FONT_SIZE)
    rows = to_halfblock(img)
    while rows and not rows[0].strip(): rows.pop(0)
    while rows and not rows[-1].strip(): rows.pop()
    return colorize(rows, PALETTES[palette_name])

def strip_markup(s): return re.sub(r"\[/?[^\]]*\]", "", s)

for vname, vtext in VARIANTS.items():
    for palette_name in ("canvas","ink"):
        rows = render_variant(vtext, palette_name)
        body = "\n".join(rows)
        (OUTDIR / f"banner_{vname}_{palette_name}.txt").write_text(body)
        (OUTDIR / f"banner_{vname}_{palette_name}.plain.txt").write_text(strip_markup(body))
        print(f"wrote banner_{vname}_{palette_name}.txt ({len(rows)} lines)")
