import os
import sys
import datetime
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException

# Read api key and connect to binance client
load_dotenv(dotenv_path="./.env.local")
client = Client(os.environ["api_key"], os.environ["api_secret"])

client.API_URL = 'https://testnet.binance.vision/api'  # Test url, delete for real life usage


def new_listing(old, new, percent):
    # Check if coin is listed
    price = ""
    while True:
        try:
            price = float(client.get_symbol_ticker(symbol=new+old)["price"])
            break
        except BinanceAPIException as e:
            print("Coin not yet listed.")
    print("Coin listed!")

    # Buy new listed coin here
    # I couldn't do it

    in_price = client.get_symbol_ticker(symbol=new_ticker)["price"]  # price we paid
    print(in_price + " at " + str(datetime.datetime.now()))
    in_price = float(in_price)
    last_price = in_price
    max_price = in_price

    while True:
        current_price = client.get_symbol_ticker(symbol=new_ticker)["price"]
        now = str(datetime.datetime.now())
        print(current_price + " at ")
        current_price = float(current_price)
        if current_price > max_price:
            print("All time high at " + now)
            max_price = current_price
        if current_price > in_price * 3 / 2:
            print("up 50% at " + now)
            # Sell some
        if current_price > in_price * 2:
            print("up 100% at " + now)
            # Sell some more
        if current_price > in_price * 3:
            print("up 200% at " + now)
            # Sell all
        if current_price < max_price * 95 / 100:
            print("down 5% from max at " + now)
            print("sold all from" + str(current_price))
            break
            # Sell all
        last_price = current_price


# Check and read for amount and new ticker
if len(sys.argv) != 4:
    print("Give ticker to buy, ticker to sell and yolo percentage respectively")
    exit()
else:
    new_ticker = sys.argv[1]
    old_ticker = sys.argv[2]
    percentage = sys.argv[3]
    new_listing(old_ticker, new_ticker, percentage)
