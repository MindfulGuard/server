#!/bin/bash

# Name of your service
SERVICE_NAME="mindfulguard.routines"

# Full path to your Python script
SCRIPT_PATH="/home/runner/work/server/server/routines/__main__.py"

# Full path to the working directory of your script
WORKING_DIR="/home/runner/work/server/server"

# Creating a service file
cat <<EOF > "/etc/systemd/system/$SERVICE_NAME.service"
[Unit]
Description=Routines for "mindfulguard"
After=network.target

[Service]
WorkingDirectory=$WORKING_DIR
ExecStart=/usr/bin/python $SCRIPT_PATH

[Install]
WantedBy=multi-user.target
EOF

# Updating systemd and enabling the service
systemctl daemon-reload
systemctl enable "$SERVICE_NAME.service"

echo "The $SERVICE_NAME service has been created and enabled."

# Starting the service
systemctl start "$SERVICE_NAME"
echo "The $SERVICE_NAME service is running."

# Checking the service status
systemctl status "$SERVICE_NAME"