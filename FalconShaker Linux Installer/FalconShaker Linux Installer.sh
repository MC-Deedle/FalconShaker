#!/usr/bin/env bash
set -euo pipefail

# 1. Automatically fetch the current username
USER_NAME=$(whoami)
HOME_DIR="/home/$USER_NAME"

echo "=================================================="
echo "   CachyOS Wine/Proton Shortcut Creator Tool"
echo "=================================================="
echo "Detected Current User: $USER_NAME"
echo "--------------------------------------------------"

# Check for zenity (visual file picker). Install if missing.
if ! command -v zenity &> /dev/null; then
    echo "Installing zenity for file selection dialogs..."
    sudo pacman -S --noconfirm zenity
fi

# Set base folder paths
BASE_BMS_DIR="$HOME_DIR/Games/falcon-bms"
DEFAULT_RUNNER="$BASE_BMS_DIR/runners/GE-Proton10-32/files/bin"

# Dynamically locate the FalconShaker <version number> directory
SHAKER_DIR=$(find "$BASE_BMS_DIR" -maxdepth 1 -type d -name "FalconShaker *" -print -quit 2>/dev/null || true)

# Fallback to the base directory if a FalconShaker folder isn't found
if [ -z "$SHAKER_DIR" ]; then
    SHAKER_DIR="$BASE_BMS_DIR"
fi

# 2. Prompt for the .exe file path
echo "Opening file picker for the Target .exe Application..."
EXE_PATH=$(zenity --file-selection \
    --title="Select the target .exe application (Default: FalconShaker)" \
    --file-filter="*.exe" \
    --filename="$SHAKER_DIR/")

# 3. Prompt for the Wine Prefix directory
echo "Opening folder picker for the WINEPREFIX..."
PREFIX_PATH=$(zenity --file-selection --directory \
    --title="Select the Wine Prefix directory" \
    --filename="$BASE_BMS_DIR/")

# 4. Prompt for the runner binary folder
echo "Opening folder picker for the Proton/Wine bin directory..."
RUNNER_BIN_DIR=$(zenity --file-selection --directory \
    --title="Select the Proton/Wine 'bin' directory" \
    --filename="$DEFAULT_RUNNER/")

# 5. Extract application name and directory for icon matching
EXE_FILENAME=$(basename "$EXE_PATH")
APP_NAME="${EXE_FILENAME%.*}"
EXE_DIR=$(dirname "$EXE_PATH")

# Find the first .ico file in the application directory (fallback to blank if none found)
ICON_PATH=$(find "$EXE_DIR" -maxdepth 1 -iname "*.ico" -print -quit 2>/dev/null || true)

# --- NEW: Check if the application is a terminal app ---
TERMINAL_SETTING="false"

# Check if "FalconShaker" is missing from the file path (case-insensitive)
if [[ ! "${EXE_PATH,,}" =~ "falconshaker" ]]; then
    echo "Non-FalconShaker application detected. Prompting for terminal setting..."
    if zenity --question \
        --title="Terminal Application Check" \
        --text="Is '$EXE_FILENAME' a terminal/command-line application?\n\nClick Yes to force the desktop icon to launch in a terminal window." \
        --ok-label="Yes" \
        --cancel-label="No" 2>/dev/null; then
        TERMINAL_SETTING="true"
        echo "➔ User selected: Launch in Terminal"
    else
        echo "➔ User selected: Launch standard GUI app"
    fi
fi
# -------------------------------------------------------

# Define desktop entry destination
SHORTCUT_PATH="$HOME_DIR/Desktop/$APP_NAME.desktop"

# 6. Build the .desktop file structure
cat << EOF > "$SHORTCUT_PATH"
[Desktop Entry]
Name=$APP_NAME
Exec=env WINEPREFIX="$PREFIX_PATH" "$RUNNER_BIN_DIR/wine" "$EXE_PATH"
Path=$EXE_DIR
Icon=${ICON_PATH:-}
Type=Application
Categories=Game;Utility;
Terminal=$TERMINAL_SETTING
StartupNotify=true
EOF

# 7. Make the shortcut executable
chmod +x "$SHORTCUT_PATH"

echo "--------------------------------------------------"
echo "Success! Shortcut created at:"
echo "👉 $SHORTCUT_PATH"
if [ -n "$ICON_PATH" ]; then
    echo "🎨 Automatically linked icon: $(basename "$ICON_PATH")"
else
    echo "⚠️  No .ico file found in the application directory. Using default system icon."
fi
echo "⚙️  Terminal launching set to: $TERMINAL_SETTING"
echo "=================================================="

