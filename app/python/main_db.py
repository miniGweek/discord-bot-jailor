import discord
import logging
import re
import os
import json
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app_config = json.load(open('app_settings.json'))

log_path = app_config.get('app_config').get('log').get('path')
log_path=os.path.join(os.getcwd(),log_path)

jailor_log_path = os.path.join(log_path,'jailor.log')

# Create the directory if it doesn't exist
os.makedirs(log_path, exist_ok=True)

jailor_log_path = os.path.join(log_path, 'jailor.log')

# Create the file if it doesn't exist
if not os.path.isfile(jailor_log_path):
    open(jailor_log_path, 'w').close()
    
# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler(jailor_log_path), logging.StreamHandler()])

logging.info('This will get logged to a file')

# Setup Discord client with intents
intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
client = discord.Client(intents=intents)


mydb = mysql.connector.connect(
  host=os.getenv("DB_HOST"),
  user=os.getenv("DB_USER"),
  password=os.getenv("DB_PASSWORD"),
  database=os.getenv("DB_NAME")
)

@client.event
async def on_ready():
    print('we have logged in as {0.user}'
          .format(client))
    logging.info('we have logged in as {0.user}'
                 .format(client))


@client.event
async def on_message(message):
    guild = str(message.guild.id)
    config_available = guild in app_config
    if config_available == True:
        config = app_config[guild]
        if message.author == client.user:  # If the message is posted by jailor bot, don't do anything
            return
        return await process_message(message, config)
    return


async def process_message(message, config):
    debug = message.content.startswith('j!debug')
    return


discord_bot_token = os.getenv('DISCORD_BOT_JAILOR_TOKEN')
client.run(discord_bot_token)
