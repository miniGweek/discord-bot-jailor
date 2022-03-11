$UserAndHost = "root@$($env:DISCORD_BOT_JAILOR_SERVERIP)"
scp main.py app_settings.json update_deployment.sh discord-bot-jailor.conf "$UserAndHost`:`/staging"
 
ssh $UserAndHost 'chmod +x /staging/update_deployment.sh && /staging/update_deployment.sh'
