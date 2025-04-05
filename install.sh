#!/bin/bash

# Define the path to the service file
SERVICE_FILE="/etc/systemd/system/my_daemon.service"

# Define the script path and username (you can change these variables if needed)
SCRIPT_PATH="main.py"
USERNAME="your_username"

# Create or overwrite the service file with the desired configuration
echo "[Unit]
Description=My Python Daemon

[Service]
ExecStart=/usr/bin/python3 $SCRIPT_PATH
Restart=always
User=$USERNAME

[Install]
WantedBy=default.target" | sudo tee $SERVICE_FILE > /dev/null

# Reload systemd to apply the changes
sudo systemctl daemon-reload

# Enable the service to start automatically on boot
sudo systemctl enable my_daemon.service

# Optionally, start the service immediately
sudo systemctl start my_daemon.service

# Check the status of the service
sudo systemctl status my_daemon.service
