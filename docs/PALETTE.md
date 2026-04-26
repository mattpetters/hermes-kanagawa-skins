# Palette reference

Both skins are direct ports of the [`kanagawa-paper.nvim`](https://github.com/thesimonho/kanagawa-paper.nvim)
canvas (light) and ink (dark) themes. Sources:

- `lua/kanagawa-paper/colors.lua` — full palette
- `lua/kanagawa-paper/themes/canvas.lua` — light theme bindings
- `lua/kanagawa-paper/themes/ink.lua`    — dark theme bindings

## Canvas (light) — used by `kanagawa-paper`

| Role                | Hex       | Palette name      |
|---------------------|-----------|-------------------|
| canvas bg           | `#E1E1DE` | canvasWhite4      |
| bg_dim              | `#D8D8D2` | canvasWhite3      |
| bg_p1 / bg_p2       | `#E6E6E3` / `#ECECE8` | canvasWhite5/6 |
| bg_statusline       | `#D1CFC5` | canvasWhite2      |
| bg_visual           | `#D4CDD4` | canvasPink3       |
| fg                  | `#73787D` | canvasGray3       |
| fg_dim              | `#8E8A80` | canvasGray2       |
| fg_dimmer           | `#AEAEA6` | canvasGray1       |
| primary accent      | `#7E8FAF` | canvasTeal1       |
| accent2 (orange)    | `#B28D77` | canvasOrange1     |
| accent3 (aqua)      | `#7B958E` | canvasAqua1       |
| accent5 (red)       | `#C27672` | canvasRed1        |
| diff add            | `#7A8C6A` | canvasGreen2      |
| info / docstring    | `#9BA98E` | canvasGreen3      |
| violet              | `#7880A5` | canvasViolet1     |
| deep wave (border)  | `#516E7D` | canvasBlue4       |
| wave body           | `#6B8998` | canvasBlue2       |

## Ink (dark) — used by `kanagawa-ink`

| Role                | Hex       | Palette name      |
|---------------------|-----------|-------------------|
| sumi bg             | `#1F1F28` | sumiInk3          |
| sumi panel          | `#2A2A37` | sumiInk4          |
| sumi panel +1       | `#363646` | sumiInk5          |
| sumi divider        | `#54546D` | sumiInk6          |
| fuji white (text)   | `#DCD7BA` | fujiWhite         |
| old white           | `#C8C093` | oldWhite          |
| fuji gray           | `#727169` | fujiGray          |
| primary accent      | `#C4B28A` | dragonYellow      |
| dragon orange       | `#B6927B` | dragonOrange      |
| dragon red (errors) | `#C4746E` | dragonRed         |
| dragon green (ok)   | `#699469` | dragonGreen       |
| dragon aqua         | `#8EA49E` | dragonAqua        |
| wave aqua           | `#6A9589` | waveAqua1         |
| dragon blue (border)| `#658594` | dragonBlue        |
| dragon violet       | `#8992A7` | dragonViolet      |

## ASCII art gradient stops

Both `banner_logo` and `banner_hero` use the same 3-stop gradient per theme so
the two pieces feel unified. Top → bottom (foam → mid wave → deep water):

| Theme   | Top crest  | Mid body  | Deep water |
|---------|-----------:|----------:|-----------:|
| canvas  | `#7E8FAF`  | `#6B8998` | `#516E7D`  |
| ink     | `#DCD7BA`  | `#8EA49E` | `#658594`  |

Plus per-theme accent injections in the wave hero where Hokusai's source has
warm hints (`canvasRed1` for paper, `oldWhite/fujiWhite` foam highlights for ink).
