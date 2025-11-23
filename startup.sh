#!/bin/bash

# Set executable and change directory
set -e
cd /home/zoot/Project/OLED

# Update Project from git
#   Initialisation commands for reference:
#   git init
#   git remote add origin https://github.com/ZephCreations/Remote_OLED_control.git

git fetch origin
git reset --hard origin/master
git pull origin master

# Activate venv
source venv/bin/activate

# Start file
while true; do
    python src/main.py
    echo "main.py exited with code $? — restarting in 2 seconds"
    sleep 2
done

# Deactivate venv
deactivate

exit

# Additional commands for auto-running
# sudo nano /etc/systemd/system/oled.service

#  SCRIPT:
#    [Unit]
#    Description=OLED Startup Script
#    After=network-online.target
#
#    [Service]
#    Type=simple
#    User=zoot
#    WorkingDirectory=/home/zoot/Project/OLED
#    ExecStart=/home/zoot/Project/OLED/startup.sh
#    Restart=always
#
#    [Install]
#    WantedBy=multi-user.target

# Make sure script has permissions after editing:
# chmod +x /home/zoot/Project/OLED/startup.sh
# sudo systemctl daemon-reload
# sudo systemctl start/restart oled.service
# sudo systemctl status oled.service

