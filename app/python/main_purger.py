import discord
import logging
import re
import os
import json
from datetime import datetime, timedelta
import asyncio

app_config = json.load(open('app_settings_purger.json'))

log_path = app_config.get('app_config').get('log').get('path')
print_command_prefix = app_config.get('app_config').get('print_command_prefix')
purge_command_prefix = app_config.get('app_config').get('purge_command_prefix')
member_to_delete = app_config.get('app_config').get('member_to_delete')
who_can_run_commands = app_config.get('app_config').get('who_can_run_commands')

log_path=os.path.join(os.getcwd(),log_path)

jailor_log_path = os.path.join(log_path,'jailor.log')
count_log_path = os.path.join(log_path,'count.log')

logging.basicConfig(filename=jailor_log_path, filemode='a', level=logging.INFO,
                    format='%(asctime)s %(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')

# Setup Discord client with intents
intents = discord.Intents.default()
intents.message_content = True
intents.guild_messages = True
intents.guild_messages = True
client = discord.Client(intents=intents)


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
    if message.author.name not in who_can_run_commands:
        return
    # Check if the message is a command
    if message.content.startswith(print_command_prefix):
        message_to_print = 'jailor says :{0}'.format(message.content.split(print_command_prefix)[1])
        write_to_file(jailor_log_path,'{0} by user id {1} with userName {2}'.format(
            message_to_print,message.author.id, message.author.name))
        await message.channel.send('jailor says :{0}'.format(message.content.split(print_command_prefix)[1]))

    if message.content.startswith(purge_command_prefix):
        await purge_messages(message, config)

async def purge_messages(message, config):
    app_config = json.load(open('app_settings_purger.json'))
    member_to_delete = app_config.get('app_config').get('member_to_delete')
    bulk_message_limit = app_config.get('app_config').get('bulk_message_limit') 
    
    #Get the name of the user for whom 
    user = member_to_delete 
    
    # Get all channels in the server
    channels = message.guild.text_channels

    # loop through channels
    for channel in channels:
        await purge(app_config, channel, bulk_message_limit, user, skip_threads=False)

    vchannels = message.guild.voice_channels

    for channel in vchannels:
        await purge(app_config, channel, bulk_message_limit, user,skip_threads=True)

async def purge(app_config, channel, bulk_message_limit, user, skip_threads=False):
    purge_search_period = app_config.get('app_config').get('purge_search_period')
    purge_channels = app_config.get('app_config').get('purge_channels')
    skip_purge_channels = app_config.get('app_config').get('skip_purge_channels')
    oldest_first = app_config.get('app_config').get('oldest_first') == "True"
    
    if (purge_channels!=[] and channel.name not in purge_channels) or (channel.name in skip_purge_channels):
        print('channel name {0} not checked'.format(channel.name))
        return
    
    print('channel name {0}'.format(channel.name))
    print('user name {0}'.format(user))
    
    start_date_str = app_config.get('app_config').get('start_date')
    end_date_str = app_config.get('app_config').get('end_date')
    
    
    # find threads
    threads_deleted_count = 0
    if not skip_threads and len(channel.threads) > 0:
        for thread in channel.threads:
            threads_deleted = await thread.purge(limit=bulk_message_limit, check=lambda msg: msg.author.name == user,bulk=True)
            threads_deleted_count = len(threads_deleted)
            msg_log = 'In channel {0}, deleted thread from {1} , delete count {2}'.format(channel.name, user, threads_deleted_count)
            print(msg_log)
    
    # find all messages by a user in a channel
    start_date_str = app_config.get('app_config').get('start_date')
    end_date_str = app_config.get('app_config').get('end_date')
    
    end = datetime.strptime(end_date_str, "%d/%m/%Y")
    lastSearchDate = datetime.strptime(start_date_str, "%d/%m/%Y")
    while end >=  lastSearchDate:
        await asyncio.sleep(2)
        start = end - timedelta(days=purge_search_period)
        msg_log = '[{0}] In channel {1}, for user {2} , search period between {3} and {4}'.format(datetime.now(),channel.name, user, end, start)
        print(msg_log)
        write_to_file(jailor_log_path,msg_log)
        
        deleted = await channel.purge(limit=bulk_message_limit, check=lambda msg: msg.author.name == user,bulk=True,oldest_first=oldest_first,before=end,after=start)
        deleted_count  = len(deleted)
        msg_log = '[{0}] In channel {1}, deleted messages from {2} , delete count {3} between {4} and {5}'.format(datetime.now(), channel.name, user, deleted_count, end, start)
        print(msg_log)
        write_to_file(jailor_log_path,msg_log)
        end = start

def write_to_file(file, msg):
    # Open a file with access mode 'a'
    file_object = open(file, 'a')
    logging.info('opened {0} file for writing message {1}\n'.format(file, msg))
    # Append 'hello' at the end of file
    file_object.write('{0}\n'.format(msg))
    # Close the file
    file_object.close()
    logging.info('closed {0} file after writing message\n'.format(file))

discord_bot_token = os.getenv('DISCORD_BOT_JAILOR_TOKEN')
client.run(discord_bot_token)
