#!/bin/bash

# ToDo - Probably too verbose, need to refactor the deployment of files bit.

source /etc/profile

timestamp=$(date +"%d%m%Y_%H%M%S");
echo "$timestamp"
# echo "$DISCORD_BOT_JAILOR_TOKEN"  
supervisorctl stop all
echo "stopped supervisorctl"

# Update discord-bot-jailor.conf
echo "replaced secret token in supervisord config"
sed -e "s/\${DISCORD_BOT_JAILOR_TOKEN}/$DISCORD_BOT_JAILOR_TOKEN/" "/staging/discord-bot-jailor.conf" > "/staging/discord-bot-jailor-withsecret.conf"

echo "copied the current supervisord conf to backup with timestamp"
mv "/etc/supervisor/conf.d/discord-bot-jailor.conf" "/staging/backup/discord-bot-jailor_$timestamp.conf"

echo "updated the supervisor conf location with new supervisor config"
cp "/staging/discord-bot-jailor-withsecret.conf" "/etc/supervisor/conf.d/discord-bot-jailor.conf"

mv "/app/main.py" "/staging/backup/main_$timestamp.py"
echo "moved /app/main.py to /staging/backup/main_$timestamp.py"

mv "/app/app_settings.json" "/staging/backup/app_settings_$timestamp.json"
echo "moved /app/app_settings.json to /staging/backup/app_settings_$timestamp.json"

mv "/staging/main.py" "/app/main.py"
echo "copied /staging/main.py to /app/main.py"

mv "/staging/app_settings.json" "/app/app_settings.json"
echo "copied /staging/app_settings.json to /app/app_settings.json"

supervisorctl reload
echo "reloaded supervisor config"
