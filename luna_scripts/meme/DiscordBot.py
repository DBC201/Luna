import discord
import sqlite3
import re

import os, sys
from dotenv import load_dotenv

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
ENV_PATH = os.path.join(ROOT, ".env.local")
load_dotenv(dotenv_path=ENV_PATH)

discord_token = os.environ["discord_token"]

client = discord.Client()
database = sqlite3.connect(os.path.join(os.path.dirname(__file__), "database.db"))
cursor = database.cursor()


def get_channels():
    """get channel ids from database

    :return: a list of ints consisting of ids
    :rtype: list
    """
    cursor.execute("SELECT id FROM channels WHERE valid = ?", [1])
    return [int(r[0]) for r in cursor.fetchall()]


def dump_eet():
    channels = get_channels()
    for channel in channels:
        send_message(channel, "dump eet")


def pump_eet():
    channels = get_channels()
    for channel in channels:
        send_message(channel, "pump eet")


def call_vitalik():
    channels = get_channels()
    for channel in channels:
        send_message(channel, "put vitalik on zhe line")


async def send_message(channel_id, message):
    channel = client.get_channel(int(channel_id))
    await channel.send(message)


@client.event
async def on_ready():
    print('Bot logged in as {0.user}'.format(client))
    print("In guilds:\n", "\n".join([guild.name for guild in client.guilds]))
    '''channels = get_channels()
    for channel in channels:
        await send_message(channel, "load ze fud")'''


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    reg_group = re.match(r"bogdanoff:\s*(\w+)((\s\w+)*)", message.content)
    if reg_group is None:
        return
    command = reg_group.group(1)
    params = reg_group.group(2)[1:].split(' ')

    async def add_channel():
        cursor.execute("SELECT * FROM channels WHERE id = ?", [message.channel.id])
        channels = cursor.fetchall()
        if channels:
            await message.channel.send("already added")
        else:
            cursor.execute("INSERT INTO channels(id, valid) VALUES(?,?)", [message.channel.id, 1])
            database.commit()

    async def remove_channel():
        cursor.execute("SELECT * FROM channels WHERE id = ?", [message.channel.id])
        channels = cursor.fetchall()
        if not channels:
            await message.channel.send("this channel doesn't exist in the database")
        else:
            cursor.execute("DELETE FROM channels where id = ?", [message.channel.id])
            database.commit()

    async def help_command():
        await message.channel.send("Type bogdanoff:add to add this channel, bogdanoff:remove to remove")

    commands = {
        "add": add_channel,
        "remove": remove_channel,
        "help": help_command
    }

    if command in commands:
        await commands[command]()
    else:
        await message.channel.send("Unrecognized command.")


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'\nUnhandled message: {args[0]}')
        else:
            raise

client.run(discord_token)
