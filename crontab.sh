#!/usr/bin/env bash

# Ensure the log file exists
touch /app/logs/crontab.log

# Added a cronjob in a new crontab
echo "* * * * * /usr/bin/python3 /app/run.py --command=scan-index --index=alerting-external --project_path=$(pwd) >> /logs/crontab.log 2>&1" > /etc/crontab

# Registering the new crontab
crontab /etc/crontab

# Starting the cron
/usr/sbin/service cron start

# Displaying logs
# Useful when executing docker-compose logs mycron
tail -f /app/logs/crontab.log