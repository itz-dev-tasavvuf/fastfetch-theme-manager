#!/usr/bin/env bash
set -euo pipefail

REPO="https://raw.githubusercontent.com/itz-dev-tasavvuf/fastfetch-theme-manager/main"
TARGET="${HOME}/.local/bin"
BIN="${TARGET}/ftm"

mkdir -p "${TARGET}"

echo "⬇️  Downloading ftm.py..."
curl -fsSL "${REPO}/ftm.py" -o "${BIN}"

chmod +x "${BIN}"

echo "✅ Installed: ${BIN}"
echo
if ! command -v fastfetch >/dev/null 2>&1; then
  echo "⚠️  fastfetch not found. Please install fastfetch."
fi

echo "\nℹ️  Add to your shell profile if ~/.local/bin is not in your PATH:"
echo "    export PATH=\"${TARGET}:\$PATH\""
echo "Then restart your shell."

echo "\nRun: ftm list"