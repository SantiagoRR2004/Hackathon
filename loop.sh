#!/bin/bash

# Get the number of connected USB devices
LISTDEVICES=""

# Get the absolute path of the current script's directory
SCRIPT_DIR=$(dirname "$(realpath "${BASH_SOURCE[0]}")")

# Define the Python script path
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

# Can add nohup if needed
# Run the Python script every 5 seconds
while true; do
    CURRENTLISTDEVICES=$(lsusb | sort | uniq)

    # Compare CURRENTLISTDEVICES with LISTDEVICES
    NEW_DEVICES=$(comm -13 <(echo "$LISTDEVICES") <(echo "$CURRENTLISTDEVICES"))

    # Check if new devices is not empty
    if [[ -n "$NEW_DEVICES"  ]]; then
        "$PYTHON_BIN" "$PYTHON_SCRIPT"
    fi

    sleep 5
    LISTDEVICES="$CURRENTLISTDEVICES"
done &
