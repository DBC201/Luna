# LUNA
Luna is a program consisting of different modules and scripts for binance using python-binance library. However
the modules should work with the right input format which have been documented in their relative folder. 
- [Github repo](https://github.com/DBC201/Luna)
- [demo website](https://rocketdodgegame.com:41373)
- ~~[Try out the discord bot](https://discord.com/api/oauth2/authorize?client_id=859857639255834644&permissions=52224&scope=bot)~~
  The binance api doesn't work in the US, and our servers are located in the US.

## Discord Bot
Currently, the bot sends messages about market change to the added channels. It will message in 10% price increase,
10% decrease, 50% increase in the past 60 minutes for a given coin. 
### Discord Bot Commands
- bogdanoff: add
  - adds the channel the message has been sent from to the database
- bogdanoff: remove
  - removes that channel
- bogdanoff: help
  - displays a help prompt

## Dependencies
- [python-binance](https://github.com/sammchardy/python-binance)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [discord.py](https://pypi.org/project/discord.py/)  
- [websocket-client](https://pypi.org/project/websocket-client/)
- [mathplotlib](https://pypi.org/project/matplotlib/) 
  (for graphing trade data, not essential if you won't use [Luna to graph](luna_modules/trade_analysis))

## Installation
- You can use pipenv, if not you can install all dependencies one by one with pip. However if a dependency gets a breaking update,
  program might not work as intended. One can look at [Pipfile.lock](Pipfile.lock) to see latest version specifics.
- Run 'pipenv install' in root folder. This should install the required dependencies.
- In case of time sync error, sync your os time with internet time.
    - Screenshot for windows:
    
    ![windows time sync](./docs/pictures/sync%20internet%20time.png)

## Scripts
### listing_buy
This is a bot that listens for trades, and will automatically buy when it gets a trade. It will sell if certain conditions
are met.
### listing_log
This used to scrape the binance website for listings and set an autologger to the listing date to log the first minute of trades. 
It also allows for past minute trades to be downloaded via download_binance.py and download_gateio.py.
### listing_mail
This sends emails when there is going to be a new listing.
### meme
A discord bot that sends notification when there is a pump and dump for a given coin.

## Modules
TODO

## Tests
These are just random scripts I have written while testing functionality and pieces of code. They aren't much organized
and are a pain to look at.

## Creators
- [Atilla Turkmen](https://github.com/atillaturkmen)
- [Deniz Cakiroglu](https://github.com/DBC201)
