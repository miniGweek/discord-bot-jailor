import discord
import logging
import re
import os
import json
from datetime import datetime

app_config = json.load(open('app_settings.json'))

log_path = app_config.get('app_config').get('log').get('path')
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
client = discord.Client(intents=intents)

patterns = [
            'Guild Saves: \*\*(\d+)/(\d+)\*\*',
            'for a total of `([\d.]+)/(\d+)` guild saves'
            ]




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
    if message.author.bot == False and message.content.startswith('j!'):
        logging.info(
            'jailor debug mode invoked, content passed={0.content}'.format(message))

        await check_send_hello(debug, message)

    if debug or (message.author.bot == True and message.author.display_name == 'counting'):

        if message.embeds != None and hasattr(message.embeds, '__len__') and len(message.embeds) > 0:
            counting_message = message.embeds[0].description
            logging.info(
                'counting bot posted embedded message with: {0}'.format(counting_message))
            await check_saves_and_lock_channel(message, counting_message, config)
            logging.info('jailor done checking if guildsaves are there')
            return
        else:
            counting_message = message.content
            logging.info(
                'counting bot posted regular message with: {0}'.format(counting_message))
            await check_saves_and_lock_channel(message, counting_message, config)
            logging.info('jailor done checking if guildsaves are there')
            return

    await log_messages_in_counting_channel(message, config)


async def check_saves_and_lock_channel(message, counting_message, config):

    logging.info('jailor initiating check if guildsaves are there')
    check_saves = get_saves(counting_message)
    counting_channel = get_counting_channel(message, config['channelId'])
    logging.info(
        'jailor result of check if guildsaves are there={0}'.format(check_saves))
    current_send_message_permission = can_send_messages(
        counting_channel, config['role'])
    logging.info('jailor result of check the current permission for sending_messages={0}'.format(
        current_send_message_permission))

    if check_saves == False and str(current_send_message_permission) in config['sendmessage_permission']:
        logging.info(
            'jailor checked guild saves are not >=1, locking channel'.format(check_saves))
        await lock_channel(counting_channel, config)
        logging.info('jailor locking channel done')
    elif check_saves == True and str(current_send_message_permission) in config['denymessage_permission']:
        logging.info(
            'jailor checked guild saves are >=1, un-locking channel'.format(check_saves))
        await unlock_channel(counting_channel, config)
        logging.info('jailor un-locking channel done')
    elif check_saves == None:
        logging.info(
            "jailor didn't evaluate guild saves, won't change anything")


def get_role(roles, name):
    for role in roles:
        if role.name == name:
            return role


async def lock_channel(channel, config):
    lock_permission = convert_string_permissions(
        config['denymessage_permission'])

    await channel.send('Guild saves are less than 1. Locking the channel.')
    await channel.set_permissions(get_role(channel.guild.roles,
                                           config['role']),
                                  send_messages=lock_permission)


async def unlock_channel(channel, config):
    unlock_permission = convert_string_permissions(
        config['sendmessage_permission'])

    await channel.send('Guild saves are at-least 1. Unlocking the channel.')
    await channel.set_permissions(get_role(channel.guild.roles,
                                           config['role']),
                                  send_messages=unlock_permission)


def get_saves(message):
    all_none = True
    for pattern in patterns:
        search_pattern = re.search(pattern, message)
        saves_atleast_one = is_saves_atleast_one(search_pattern)

        if saves_atleast_one == False:
            return False
        if search_pattern != None:
            all_none = False

    if all_none == True:
        return None

    return True


def is_saves_atleast_one(pattern):
    if pattern:
        savesString = pattern.group(1)
        saves = float(savesString)
        if saves >= 1:
            return True
        else:
            return False


def get_counting_channel(message, channel_to_check):
    # channel_to_check = '💴-♧-counting'
    # channel_to_check='😇-♤-chat'
    # channel_to_check = 'counting'

    channels = message.guild.channels
    for channel in channels:
        if channel.id == channel_to_check:
            return channel


def get_channel_permission_overwrites(channel, role):
    role = get_role(channel.guild.roles, role)
    permission_overwrites = channel.overwrites_for(role)
    return permission_overwrites


def can_send_messages(channel, role):
    current_permissions = get_channel_permission_overwrites(
        channel, role)
    send_messages_permission = current_permissions.send_messages
    return send_messages_permission


async def check_send_hello(debug, message):
    if debug and message.content.startswith('j!debug print '):
        printcontent = message.content.split('j!debug print ')[1]
        await message.channel.send('Good bot jailor says :{0}'.format(printcontent))


def convert_string_permissions(permission):
    if permission == 'True':
        return True
    elif permission == 'False':
        return False
    elif permission == 'None':
        return None


async def log_messages_in_counting_channel(message, config):
    counting_channel = get_counting_channel(message, config['channelId'])
    if counting_channel != None and message.channel.id == counting_channel.id and message.author.bot != True:
        currentDateTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        logMessage = '{} GuildName={}#|#GuildId={}#|#Name={}#|#Id={}#|#Nick={}#|#CountMessage={}\n'.format(
            currentDateTime, message.guild.name, message.guild.id, message.author.name, message.author.id, message.author.nick, message.content)
        write_to_file(count_log_path, logMessage)


def write_to_file(file, msg):
    # Open a file with access mode 'a'
    file_object = open(file, 'a')
    logging.info('opened {0} file for writing message {1}'.format(file, msg))
    # Append 'hello' at the end of file
    file_object.write(msg)
    # Close the file
    file_object.close()
    logging.info('closed {0} file after writing message'.format(file))


discord_bot_token = os.getenv('DISCORD_BOT_JAILOR_TOKEN')
client.run(discord_bot_token)
