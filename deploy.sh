#!/bin/bash
set -e

export XDG_RUNTIME_DIR=/run/user/$(id -u)
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus

cd /home/ringdingdonghu/projects/pythonEmailService

git pull origin main
.venv/bin/pip install flask pymysql redis gunicorn -q

systemctl --user restart travelplanner-email
echo "pythonEmailService deployed"
