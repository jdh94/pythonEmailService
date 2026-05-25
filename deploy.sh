#!/bin/bash
set -e

cd /home/ringdingdonghu/projects/pythonEmailService

git pull origin main
.venv/bin/pip install flask pymysql redis gunicorn -q

systemctl --user restart travelplanner-email
echo "pythonEmailService deployed"
