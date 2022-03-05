import discord
import logging
import re
import os

logging.basicConfig(filename='jailor.log', filemode='a', level=logging.INFO, format='%(asctime)s %(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')

client = discord.Client()

@client.event
async def on_ready():
    print('we have logged in as {0.user}'
    .format(client))
    logging.info('we have logged in as {0.user}'
    .format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    debug = message.content.startswith('j!debug')
    if message.author.bot == False and message.content.startswith('j!'):
        logging.info('jailor debug mode invoked, content passed={0.content}'.format(message))
        await message.channel.send('Jailor will be happy to do for you :{0.content}'.format(message))

    if debug or (message.author.bot == True and message.author.display_name == 'counting'):
        
        if message.embeds != None and hasattr(message.embeds,'__len__') and len(message.embeds) > 0:
            counting_message = message.embeds[0].description
            logging.info('counting bot posted embedded message with: {0}'.format(counting_message))
            await check_saves_and_lock_channel(message, counting_message)
            logging.info('jailor done checking if guildsaves are there')
            return
        else:
            counting_message = message.content
            logging.info('counting bot posted regular message with: {0}'.format(counting_message))
            await check_saves_and_lock_channel(message, counting_message)
            logging.info('jailor done checking if guildsaves are there')
            return


async def check_saves_and_lock_channel(message, counting_message):

    logging.info('jailor initiating check if guildsaves are there')
    check_saves = get_saves(counting_message)
    counting_channel=get_counting_channel(message)
    logging.info('jailor result of check if guildsaves are there={0}'.format(check_saves))
    if check_saves == False:
        logging.info('jailor checked guild saves are not >=1, locking channel'.format(check_saves))        
        await lock_channel(counting_channel)
        logging.info('jailor locking channel done')
    elif check_saves == True:
        logging.info('jailor checked guild saves are >=1, un-locking channel'.format(check_saves))
        await unlock_channel(counting_channel)
        logging.info('jailor un-locking channel done')        
            

def get_role(roles,name):
    for role in roles:
        if role.name == name:
            return role

async def lock_channel(channel):
    await channel.send('Guild saves are less than 1. Locking channel')
    await channel.set_permissions(get_role(channel.guild.roles, '@everyone'), send_messages=False)

async def unlock_channel(channel):
    await channel.send('Guild saves are at-least 1. Unlocking channel')
    await channel.set_permissions(get_role(channel.guild.roles, '@everyone'), send_messages=True)

def get_saves(message):
    pattern1=re.search('There are (.+?)/2 guild saves left.',message)
    pattern2=re.search('Guild Saves: \*\*(.+?)/2\*\*',message)

    return is_saves_atleast_one(pattern1) or is_saves_atleast_one(pattern2)

def is_saves_atleast_one(pattern):
    if pattern:
        savesString=pattern.group(1)
        saves=float(savesString)
        if saves >= 1:
            return True
        else:
            return False
    else:
        return False


def get_counting_channel(message):
    channel_to_check='💴-♧-counting'
    #channel_to_check='😇-♤-chat' #
    channels=message.guild.channels;
    for channel in channels:
        if channel.name == channel_to_check:
            return channel

discord_bot_token=os.getenv("DISCORD_BOT_JAILOR_TOKEN")
client.run(discord_bot_token)