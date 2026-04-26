"""Generate palette-quantized colored braille ASCII of Hokusai's wave for both
kanagawa-paper skins (canvas + ink). Outputs Rich markup files into
assets/previews/.

Tunables: COLS, ROWS, THRESHOLD, palettes.
"""
from PIL import Image, ImageOps
from pathlib import Path
import re

ROOT   = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "assets" / "source" / "hokusai_great_wave.jpg"
OUTDIR = ROOT / "assets" / "previews"
OUTDIR.mkdir(parents=True, exist_ok=True)

SRC = Image.open(SOURCE).convert("RGB")

# Crop to focus on the wave + Fuji
W, H = SRC.size
SRC = SRC.crop((int(W*0.02), int(H*0.05), int(W*0.99), int(H*0.95)))

COLS = 50
ROWS = 14
PIX_W = COLS * 2
PIX_H = ROWS * 4

img  = SRC.resize((PIX_W, PIX_H), Image.LANCZOS)
gray = ImageOps.autocontrast(img.convert("L"), cutoff=2)

CANVAS_PALETTE = [
    "#E1E1DE", "#D1CFC5", "#AEAEA6", "#8E8A80", "#73787D",
    "#516E7D", "#6B8998", "#7E8FAF", "#7B958E", "#C27672",
]
INK_PALETTE = [
    "#1F1F28", "#2A2A37", "#363646", "#54546D", "#727169",
    "#658594", "#8EA49E", "#6A9589", "#C8C093", "#DCD7BA",
]

DOT_BITS = {
    (0,0): 0x01, (0,1): 0x02, (0,2): 0x04, (0,3): 0x40,
    (1,0): 0x08, (1,1): 0x10, (1,2): 0x20, (1,3): 0x80,
}

def hex_rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2],16), int(h[2:4],16), int(h[4:6],16))

def closest(rgb, palette_rgb):
    best, bd = 0, 1e18
    for i,(r,g,b) in enumerate(palette_rgb):
        d = (r-rgb[0])**2 + (g-rgb[1])**2 + (b-rgb[2])**2
        if d < bd:
            bd, best = d, i
    return best

def render(palette_hex, dark_on_light=True, threshold=128, invert_color=False):
    palette_rgb = [hex_rgb(h) for h in palette_hex]
    gray_px = gray.load()
    rgb_px  = img.load()

    lines = []
    for ry in range(ROWS):
        run_color = None
        run_chars = []
        out = []
        def flush():
            if run_chars:
                out.append(f"[{run_color}]{''.join(run_chars)}[/]")
        for cx in range(COLS):
            cell_gray = [[0]*4 for _ in range(2)]
            r_sum=g_sum=b_sum=lit_count=0
            for x in range(2):
                for y in range(4):
                    px = cx*2 + x
                    py = ry*4 + y
                    gv = gray_px[px, py]
                    cell_gray[x][y] = gv
                    is_lit = (gv < threshold) if dark_on_light else (gv >= threshold)
                    if is_lit:
                        rr,gg,bb = rgb_px[px, py]
                        r_sum+=rr; g_sum+=gg; b_sum+=bb
                        lit_count+=1
            bits = 0
            for x in range(2):
                for y in range(4):
                    gv = cell_gray[x][y]
                    is_lit = (gv < threshold) if dark_on_light else (gv >= threshold)
                    if is_lit:
                        bits |= DOT_BITS[(x,y)]
            ch = chr(0x2800 + bits)
            if lit_count == 0:
                color = palette_hex[0]
                ch = "\u2800"
            else:
                avg = (r_sum//lit_count, g_sum//lit_count, b_sum//lit_count)
                if invert_color:
                    avg = (255-avg[0], 255-avg[1], 255-avg[2])
                color = palette_hex[closest(avg, palette_rgb)]
            if color != run_color:
                flush()
                run_color = color
                run_chars = [ch]
            else:
                run_chars.append(ch)
        flush()
        lines.append("".join(out))
    return lines

paper_lines = render(CANVAS_PALETTE, dark_on_light=True, threshold=130)
ink_lines   = render(INK_PALETTE,    dark_on_light=True, threshold=130, invert_color=True)

PAPER_CAPTION = [
    "[bold #73787D]                  神 奈 川 沖 浪 裏[/]",
    "[dim #8E8A80]                  The Great Wave · 葛飾北斎[/]",
]
INK_CAPTION = [
    "[bold #DCD7BA]                  神 奈 川 沖 浪 裏[/]",
    "[dim #54546D]                  The Great Wave · 葛飾北斎[/]",
]

paper_block = "\n".join(paper_lines + PAPER_CAPTION)
ink_block   = "\n".join(ink_lines   + INK_CAPTION)

(OUTDIR / "paper_hero.txt").write_text(paper_block)
(OUTDIR / "ink_hero.txt").write_text(ink_block)

def strip_markup(s):
    return re.sub(r"\[/?[^\]]*\]", "", s)

(OUTDIR / "paper_hero.plain.txt").write_text(strip_markup(paper_block))
(OUTDIR / "ink_hero.plain.txt").write_text(strip_markup(ink_block))

print(f"wrote {OUTDIR/'paper_hero.txt'} ({len(paper_lines)+2} lines)")
print(f"wrote {OUTDIR/'ink_hero.txt'} ({len(ink_lines)+2} lines)")
