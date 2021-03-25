import os
import sys
import argparse
from dotenv import load_dotenv
from binance.client import Client
from binance.websockets import BinanceSocketManager
import time


def return_parser():
    parser = argparse.ArgumentParser(description="Auto buy listing")
    parser.add_argument("buy_type", type=str, help="Coin to buy (ex:BTC)")
    parser.add_argument("sell_type", type=str, help="Coin to pay with (ex:USDT)")
    parser.add_argument("spending_amount", type=float, help="Amount to pay")
    parser.add_argument("env_path", type=str, help="env file path")
    return parser


args = return_parser().parse_args(sys.argv[1:])
BUY_TYPE = args.buy_type.upper()
SELL_TYPE = args.sell_type.upper()
SPENDING_AMOUNT = args.spending_amount
env_path = args.env_path
SYMBOL = BUY_TYPE + SELL_TYPE

load_dotenv(dotenv_path=env_path)
client = Client(os.environ["api_key"], os.environ["api_secret"])
sock_manager = BinanceSocketManager(client)

client.API_URL = 'https://testnet.binance.vision/api'  # Test url, delete for real life usage


def trade_callback(data):
    if data['p']:
        global IN, IN_PRICE, MAX_PRICE, DOUBLE_OUT, TRIPLE_OUT, DOUBLE_VAL, TRIPLE_VAL, BOTTOM_VAL
        global BUY_TYPE, SELL_TYPE, SPENDING_AMOUNT, BALANCE
        global START_TIME
        current_price = data['p']
        MAX_PRICE = max(current_price, MAX_PRICE)
        if not IN:
            IN_PRICE = data['p']
            client.order_market_buy(symbol=SYMBOL, quoteOrderQty=SPENDING_AMOUNT)
            DOUBLE_VAL = IN_PRICE * 2
            TRIPLE_VAL = IN_PRICE * 3
            BOTTOM_VAL = IN_PRICE * 0.95
            BALANCE = client.get_asset_balance(asset=BUY_TYPE)["free"]
            IN = True
            START_TIME = time.time()
        else:
            if current_price <= BOTTOM_VAL:
                client.order_market_sell(symbol=SYMBOL, quantity=BALANCE)
                sys.exit()
            elif not DOUBLE_OUT and current_price >= DOUBLE_VAL:
                client.order_market_sell(symbol=SYMBOL, quantity=BALANCE*0.5)
                BALANCE *= 0.5
                DOUBLE_OUT = True
            elif not TRIPLE_OUT and current_price >= TRIPLE_VAL:
                client.order_market_sell(symbol=SYMBOL, quantity=BALANCE*0.75)
                BALANCE *= 0.25
                TRIPLE_OUT = True
            elif DOUBLE_OUT and TRIPLE_OUT and current_price <= MAX_PRICE * 0.95: # i don't like this multiplication here slows down?
                client.order_market_sell(symbol=SYMBOL, quantity=BALANCE)
                sys.exit()
            elif time.time() - START_TIME >= 58:
                client.order_market_sell(symbol=SYMBOL, quantity=BALANCE)
                sys.exit()
    else:
        print("no trades")


trade_sock = sock_manager.start_trade_socket(symbol=SYMBOL, callback=trade_callback)

IN = False
IN_PRICE = sys.maxsize
MAX_PRICE = 0
DOUBLE_OUT = False
TRIPLE_OUT = False
DOUBLE_VAL = 0
TRIPLE_VAL = 0
BOTTOM_VAL = sys.maxsize
BALANCE = 0
START_TIME = 0
sock_manager.run()
