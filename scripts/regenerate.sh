#!/usr/bin/env bash
# Regenerate hero (Hokusai wave) and logo (神奈川-AGENT) ASCII art and
# write them back into the skin YAMLs under skins/.
#
# Requires: python3 with Pillow + PyYAML
#   pip install --user Pillow PyYAML
#
# Usage:
#   ./scripts/regenerate.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PYTHON:-python3}"

cd "$ROOT"

# Make sure the source image exists (re-download from Wikimedia if missing)
if [[ ! -f assets/source/hokusai_great_wave.jpg ]]; then
  echo "downloading public-domain Hokusai source image..."
  mkdir -p assets/source
  curl -sL -o assets/source/hokusai_great_wave.jpg \
    "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/The_Great_Wave_off_Kanagawa.jpg/1280px-The_Great_Wave_off_Kanagawa.jpg"
fi

echo "1/2  generating wave hero ASCII..."
"$PY" scripts/generate_hero.py

echo "2/2  generating block-letter logo ASCII..."
"$PY" scripts/generate_logo.py

echo "3/3  injecting into skin YAMLs..."
"$PY" scripts/inject_art.py

echo "done. Re-run scripts/install.sh to push the updated skins to ~/.hermes/skins/."
