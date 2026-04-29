#!/usr/bin/env bash
# Install the kanagawa-canvas and kanagawa-ink skins/themes into your Hermes profile
# and matching Warp custom themes into ~/.warp/themes.
# Idempotent: re-running just refreshes the YAML files.
#
# What gets installed:
#   - CLI skins   -> $HERMES_HOME/skins/         (terminal banner, prompt, status bar)
#   - Web themes  -> $HERMES_HOME/dashboard-themes/  (web UI palette + fonts)
#   - Warp themes -> $WARP_HOME/themes/          (Warp custom themes)
#
# Usage:
#   ./scripts/install.sh            # installs into $HERMES_HOME (or ~/.hermes)
#   HERMES_HOME=/path ./scripts/install.sh
#   WARP_HOME=/path ./scripts/install.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOME_DIR="${HERMES_HOME:-$HOME/.hermes}"
WARP_HOME_DIR="${WARP_HOME:-$HOME/.warp}"
SKINS_DEST="$HOME_DIR/skins"
THEMES_DEST="$HOME_DIR/dashboard-themes"
WARP_THEMES_DEST="$WARP_HOME_DIR/themes"

mkdir -p "$SKINS_DEST" "$THEMES_DEST" "$WARP_THEMES_DEST"

copy_theme_file() {
  local src="$1"
  local dst="$2"
  local name="$3"

  if [[ -e "$dst" && "$src" -ef "$dst" ]]; then
    echo "  $name (already in place)"
    return
  fi

  cat "$src" > "$dst"
  echo "  $name"
}

echo "Installing CLI skins -> $SKINS_DEST"
for skin in kanagawa-canvas kanagawa-ink; do
  src="$ROOT/skins/$skin.yaml"
  dst="$SKINS_DEST/$skin.yaml"
  copy_theme_file "$src" "$dst" "$skin"
done

echo "Installing dashboard themes -> $THEMES_DEST"
for theme in kanagawa-canvas kanagawa-ink; do
  src="$ROOT/dashboard-themes/$theme.yaml"
  dst="$THEMES_DEST/$theme.yaml"
  copy_theme_file "$src" "$dst" "$theme"
done

echo "Installing Warp themes -> $WARP_THEMES_DEST"
for theme in kanagawa-canvas kanagawa-canvas-lighter kanagawa-canvas-bright kanagawa-ink; do
  src="$ROOT/warp-themes/$theme.yaml"
  dst="$WARP_THEMES_DEST/$theme.yaml"
  copy_theme_file "$src" "$dst" "$theme"
done

cat <<'EOF'

Installed.

CLI:
  /skin kanagawa-canvas      # light · canvas variant
  /skin kanagawa-ink         # dark  · ink variant

  Or set as default in ~/.hermes/config.yaml:
    display:
      skin: kanagawa-ink

Web dashboard:
  Open the theme picker in the dashboard UI and pick "Kanagawa Canvas"
  (light) or "Kanagawa Ink" (dark).

  Or set as default in ~/.hermes/config.yaml:
    dashboard:
      theme: kanagawa-ink

Warp:
  Open Settings > Appearance > Themes and pick "Kanagawa Canvas",
  "Kanagawa Canvas Lighter", "Kanagawa Canvas Bright", or "Kanagawa Ink".

  If Sync with OS is enabled:
    light mode -> pick your preferred Canvas variant
    dark mode  -> Kanagawa Ink
EOF
