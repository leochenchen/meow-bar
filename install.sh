#!/bin/bash
set -euo pipefail

echo "=== MeowBar Installer ==="
echo "A pixel cat companion for your Claude Code menu bar"
echo ""

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
MEOW_HOME="$HOME/.meow-bar"
FRAMES_DIR="$MEOW_HOME/frames"

# Check dependencies
if ! command -v jq &>/dev/null; then
    echo "[!] jq is required but not installed."
    echo "    Install with: brew install jq"
    exit 1
fi

if ! command -v swift &>/dev/null; then
    echo "[!] Swift is required but not installed."
    echo "    Install Xcode Command Line Tools: xcode-select --install"
    exit 1
fi

# Step 1: Generate pixel cat frames
echo "[1/4] Generating pixel cat frames..."
if command -v python3 &>/dev/null; then
    # Check if Pillow is available
    if python3 -c "from PIL import Image" 2>/dev/null; then
        python3 "$SCRIPT_DIR/resources/generate-frames.py"
    else
        echo "  Installing Pillow..."
        pip3 install Pillow --quiet
        python3 "$SCRIPT_DIR/resources/generate-frames.py"
    fi
else
    echo "[!] Python 3 is required to generate cat frames."
    exit 1
fi

# Step 2: Copy frames to ~/.meow-bar/frames/
echo "[2/4] Installing frames to $FRAMES_DIR..."
mkdir -p "$FRAMES_DIR"
cp "$SCRIPT_DIR/app/MeowBar/Resources/Frames/"*.png "$FRAMES_DIR/"
echo "  Copied $(ls "$FRAMES_DIR"/*.png 2>/dev/null | wc -l | tr -d ' ') frames"

# Step 3: Build Swift app
echo "[3/4] Building MeowBar.app..."
cd "$SCRIPT_DIR/app/MeowBar"
swift build --configuration release 2>&1 | tail -1

# Create .app bundle
APP_DIR="$MEOW_HOME/MeowBar.app"
CONTENTS_DIR="$APP_DIR/Contents"
MACOS_DIR="$CONTENTS_DIR/MacOS"

mkdir -p "$MACOS_DIR"

# Copy binary
BUILD_BIN="$(swift build --configuration release --show-bin-path)/MeowBar"
cp "$BUILD_BIN" "$MACOS_DIR/MeowBar"

# Create Info.plist
cat > "$CONTENTS_DIR/Info.plist" << 'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>MeowBar</string>
    <key>CFBundleIdentifier</key>
    <string>com.meowbar.app</string>
    <key>CFBundleName</key>
    <string>MeowBar</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>LSUIElement</key>
    <true/>
    <key>LSMinimumSystemVersion</key>
    <string>13.0</string>
</dict>
</plist>
PLIST

echo "  Built: $APP_DIR"

# Step 4: Initialize state file
echo "[4/4] Initializing..."
STATE_FILE="$HOME/.claude/meow-state.json"
mkdir -p "$HOME/.claude"
if [ ! -f "$STATE_FILE" ]; then
    echo '{"state":"idle","timestamp":"","session_id":"","events_log":[]}' > "$STATE_FILE"
fi

echo ""
echo "=== Installation Complete ==="
echo ""
echo "To use MeowBar:"
echo ""
echo "  1. Launch the menu bar app:"
echo "     open $APP_DIR"
echo ""
echo "  2. Install the Claude Code plugin:"
echo "     claude plugins add $SCRIPT_DIR"
echo "     claude plugins enable meow-bar"
echo ""
echo "  3. (Optional) Add to Login Items for auto-start:"
echo "     System Settings > General > Login Items > Add MeowBar.app"
echo ""
echo "  4. Start a Claude Code session and watch your cat!"
echo ""
