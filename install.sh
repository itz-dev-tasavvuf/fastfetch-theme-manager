#!/usr/bin/env bash
set -e

# ==========================================
# 🌈 FTM Installer (Universal)
# ==========================================

REPO_URL="https://raw.githubusercontent.com/itz-dev-tasavvuf/fastfetch-theme-manager/main/ftm.py"
INSTALL_DIR="$HOME/.local/bin"
EXECUTABLE="$INSTALL_DIR/ftm"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}
  _____ _______ __  __ 
 |  ___|__   __|  \/  |
 | |_     | |  | \  / |
 |  _|    | |  | |\/| |
 |_|      |_|  |_|  |_|  Installer
${NC}"

# 1. Prepare Directory
mkdir -p "$INSTALL_DIR"

# 2. Download
echo -e "⬇️  Downloading FTM..."
if command -v curl >/dev/null; then
    curl -fsSL "$REPO_URL" -o "$EXECUTABLE"
elif command -v wget >/dev/null; then
    wget -qO "$EXECUTABLE" "$REPO_URL"
else
    echo -e "${RED}❌ Error: curl or wget is required.${NC}"
    exit 1
fi

chmod +x "$EXECUTABLE"
echo -e "${GREEN}✔ Installed to $EXECUTABLE${NC}"

# 3. Dependency Check
echo -e "\n🔍 Checking dependencies..."
MISSING=0

if ! command -v fastfetch >/dev/null; then
    echo -e "${RED}✖ Fastfetch is missing.${NC}"
    MISSING=1
else
    echo -e "${GREEN}✔ Fastfetch found.${NC}"
fi

if ! command -v fzf >/dev/null; then
    echo -e "${RED}✖ fzf (fuzzy finder) is missing.${NC} (Recommended for 'ftm pick')"
    # We don't mark MISSING=1 strictly for fzf as it's optional for some features
fi

if [ $MISSING -eq 1 ]; then
    echo -e "\n${BLUE}ℹ Attempting to identify installation command...${NC}"
    if command -v pacman >/dev/null; then
        echo "  Run: sudo pacman -S fastfetch fzf"
    elif command -v apt >/dev/null; then
        echo "  Run: sudo apt install fastfetch fzf"
    elif command -v dnf >/dev/null; then
        echo "  Run: sudo dnf install fastfetch fzf"
    elif command -v zypper >/dev/null; then
        echo "  Run: sudo zypper install fastfetch fzf"
    elif command -v apk >/dev/null; then
        echo "  Run: sudo apk add fastfetch fzf"
    elif command -v xbps-install >/dev/null; then
        echo "  Run: sudo xbps-install -S fastfetch fzf"
    elif command -v brew >/dev/null; then
        echo "  Run: brew install fastfetch fzf"
    else
        echo "  Please install 'fastfetch' using your package manager."
    fi
fi

# 4. Path Check
case ":$PATH:" in
    *":$INSTALL_DIR:"*) ;;
    *)
        echo -e "\n${RED}⚠ Warning: $INSTALL_DIR is not in your PATH.${NC}"
        echo "  Add this to your shell config (~/.bashrc, ~/.zshrc, etc.):"
        echo -e "  ${BLUE}export PATH=\"$INSTALL_DIR:\$PATH\"${NC}"
        ;;
esac

echo -e "\n${GREEN}🚀 Installation Complete!${NC}"
echo -e "Try running: ${BLUE}ftm build${NC} to create your first theme."