#!/bin/bash

# Define the udev rules directory
UDEV_RULES_DIR="/etc/udev/rules.d"

# Create the udev rules directory if it doesn't exist
sudo mkdir -p "$UDEV_RULES_DIR"

# Get the absolute path of the current script's directory
SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")

# Define the Python script path relative to the Bash script
PYTHON_SCRIPT="$SCRIPT_DIR/main.py"

# Define the path to the Python interpreter from the virtual environment
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"

# Check if the Python interpreter exists
if [[ -x "$VENV_PYTHON" ]]; then
    PYTHON_BIN="$VENV_PYTHON"
else
    echo "Virtual environment Python not found at $VENV_PYTHON"
    exit 1
fi

# Define the rule content
RULE_CONTENT='ACTION=="add", SUBSYSTEM=="usb", RUN+="/usr/bin/systemd-run --no-block '$VENV_PYTHON' '$PYTHON_SCRIPT'"'

# Create the 99-usb.rules file with the rule content
echo "$RULE_CONTENT" | sudo tee "$UDEV_RULES_DIR/99-usb.rules" > /dev/null

# Set appropriate permissions (optional, if needed)
sudo chmod 644 "$UDEV_RULES_DIR/99-usb.rules"

echo "Udev rule created successfully at $UDEV_RULES_DIR/99-usb.rules"

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm control --reload

echo "Udev rules reloaded"
