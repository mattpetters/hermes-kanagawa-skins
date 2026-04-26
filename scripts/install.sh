#!/usr/bin/env bash
# Install the kanagawa-paper and kanagawa-ink skins into your Hermes profile.
# Idempotent: re-running just refreshes the YAML files.
#
# Usage:
#   ./scripts/install.sh            # installs into $HERMES_HOME/skins (or ~/.hermes/skins)
#   HERMES_HOME=/path ./scripts/install.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${HERMES_HOME:-$HOME/.hermes}/skins"

mkdir -p "$DEST"

for skin in kanagawa-paper kanagawa-ink; do
  src="$ROOT/skins/$skin.yaml"
  dst="$DEST/$skin.yaml"
  cp "$src" "$dst"
  echo "installed $skin -> $dst"
done

cat <<'EOF'

Installed. To activate:

  /skin kanagawa-paper      # light · canvas variant
  /skin kanagawa-ink        # dark  · ink variant

Or set as default in ~/.hermes/config.yaml:

  display:
    skin: kanagawa-ink
EOF
