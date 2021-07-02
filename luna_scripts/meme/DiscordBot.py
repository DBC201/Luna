import discord
import sqlite3
import re
import random
from dotenv import load_dotenv
import time
from discord.ext import tasks

import os, sys

CURRENT = os.path.dirname(__file__)
ROOT = os.path.join(CURRENT, "..", "..")
sys.path.append(ROOT)

from luna_modules.binance.BinanceApiWrapper import BinanceApiWrapper
# from EmailMemes import EmailMemes
from Ticker import Ticker

apiWrapper = BinanceApiWrapper()

ENV_PATH = os.path.join(ROOT, ".env.local")
load_dotenv(dotenv_path=ENV_PATH)

discord_token = os.environ["discord_token"]

client = discord.Client()
database = sqlite3.connect(os.path.join(os.path.dirname(__file__), "database.db"))
cursor = database.cursor()

initial_prices = apiWrapper.get_price_dict()
tickers = dict()
for p in initial_prices:
    tickers[p] = Ticker(p, initial_prices[p])
# Check every minute for price fluctuations
minutes = 0


@tasks.loop(minutes=1)
async def check_prices():
    global minutes
    # Update current prices of all tickers
    current_prices = apiWrapper.get_price_dict()
    for name in tickers:
        tickers[name].current_price = current_prices[name]
    # Check prices for all tickers
    for name in tickers:
        t = tickers[name]
        # Check USDT parities only
        if t.identifier[-4:] != "USDT":
            continue
        if (t.current_price < t.initial_price * 0.9) and not t.dumped:
            # EmailMemes.send_bogdanoff(t.identifier)
            await dump_eet(t.identifier)
            t.dumped = True
        if (t.current_price > t.initial_price * 1.1) and not t.pumped:
            # EmailMemes.send_jesse(t.identifier)
            await pump_eet(t.identifier)
            t.pumped = True
        if (t.current_price > t.initial_price * 1.5) and not t.called_vitalik:
            # EmailMemes.get_vitalik_on_the_line(t.identifier)
            await call_vitalik(t.identifier)
            t.called_vitalik = True
    # update old price every hour
    minutes += 1
    if minutes % 60 == 0:
        for name in tickers:
            tickers[name].reset()


def get_channels():
    """get channel ids from database

    :return: a list of ints consisting of ids
    :rtype: list
    """
    cursor.execute("SELECT id FROM channels WHERE valid = ?", [1])
    return [int(r[0]) for r in cursor.fetchall()]


def load_meme(condition):
    meme = random.choice(os.listdir(os.path.join(CURRENT, condition)))
    meme = os.path.join(CURRENT, condition, meme)
    with open(meme, 'rb') as file:
        return discord.File(file)


async def dump_eet(ticker):
    link = "https://www.binance.com/en/trade/" + ticker
    channels = get_channels()
    for channel in channels:
        await send_message(channel, f"dump eet: {link}", file=load_meme("dump"))


async def pump_eet(ticker):
    link = "https://www.binance.com/en/trade/" + ticker
    channels = get_channels()
    for channel in channels:
        await send_message(channel, f"pump eet: {link}", file=load_meme("pump"))


async def call_vitalik(ticker):
    link = "https://www.binance.com/en/trade/" + ticker
    channels = get_channels()
    for channel in channels:
        await send_message(channel, f"put vitalik on zhe line: {link}", file=load_meme("vitalik"))


async def send_message(channel_id, message, file=None):
    channel = client.get_channel(int(channel_id))
    if channel:
        await channel.send(message, file=file)


@client.event
async def on_ready():
    print('Bot logged in as {0.user}'.format(client))
    print("In guilds:\n", "\n".join([guild.name for guild in client.guilds]))
    channels = get_channels()
    for channel in channels:
        await send_message(channel, "load ze fud", file=load_meme("wojak"))
    check_prices.start()


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
            await message.channel.send("added this channel to notification list")

    async def remove_channel():
        cursor.execute("SELECT * FROM channels WHERE id = ?", [message.channel.id])
        channels = cursor.fetchall()
        if not channels:
            await message.channel.send("this channel doesn't exist in the database")
        else:
            cursor.execute("DELETE FROM channels where id = ?", [message.channel.id])
            database.commit()
            await message.channel.send("removed this channel from notification list")

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
