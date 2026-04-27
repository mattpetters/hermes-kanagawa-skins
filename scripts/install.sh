#!/usr/bin/env bash
# Install the kanagawa-canvas and kanagawa-ink skins/themes into your Hermes profile.
# Idempotent: re-running just refreshes the YAML files.
#
# What gets installed:
#   - CLI skins   -> $HERMES_HOME/skins/         (terminal banner, prompt, status bar)
#   - Web themes  -> $HERMES_HOME/dashboard-themes/  (web UI palette + fonts)
#
# Usage:
#   ./scripts/install.sh            # installs into $HERMES_HOME (or ~/.hermes)
#   HERMES_HOME=/path ./scripts/install.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOME_DIR="${HERMES_HOME:-$HOME/.hermes}"
SKINS_DEST="$HOME_DIR/skins"
THEMES_DEST="$HOME_DIR/dashboard-themes"

mkdir -p "$SKINS_DEST" "$THEMES_DEST"

echo "Installing CLI skins -> $SKINS_DEST"
for skin in kanagawa-canvas kanagawa-ink; do
  src="$ROOT/skins/$skin.yaml"
  dst="$SKINS_DEST/$skin.yaml"
  # `cat > dst` instead of `cp` — cp on macOS exits 1 when source and dest
  # are the same file (e.g. when HERMES_HOME is symlinked into this repo,
  # or when re-running after a no-op install). With `set -e` that aborts
  # the whole script. cat handles identical-file case gracefully.
  cat "$src" > "$dst"
  echo "  $skin"
done

echo "Installing dashboard themes -> $THEMES_DEST"
for theme in kanagawa-canvas kanagawa-ink; do
  src="$ROOT/dashboard-themes/$theme.yaml"
  dst="$THEMES_DEST/$theme.yaml"
  cat "$src" > "$dst"
  echo "  $theme"
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
EOF
