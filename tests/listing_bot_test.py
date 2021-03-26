import os
import sys
import argparse
from dotenv import load_dotenv
from binance.client import Client
from binance.websockets import BinanceSocketManager
import time
import math


def return_parser():
    parser = argparse.ArgumentParser(description="Auto buy listing")
    parser.add_argument("buy_type", type=str, help="Coin to buy (ex:BTC)")
    parser.add_argument("sell_type", type=str, help="Coin to pay with (ex:USDT)")
    parser.add_argument("spending_amount", type=float, help="Amount to pay")
    parser.add_argument("env_path", type=str, help="file path for env variables")
    return parser


#args = return_parser().parse_args(sys.argv[1:])
BUY_TYPE = "ETH" # args.buy_type.upper()
SELL_TYPE = "USDT" # args.sell_type.upper()
SPENDING_AMOUNT = 100 # args.spending_amount
env_path = "../.env.local" # args.env_path
SYMBOL = BUY_TYPE + SELL_TYPE

load_dotenv(dotenv_path=env_path)
client = Client(os.environ["api_key"], os.environ["api_secret"])
sock_manager = BinanceSocketManager(client)

client.API_URL = 'https://testnet.binance.vision/api'  # Test url, delete for real life usage

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
symbol_info = client.get_symbol_info(SYMBOL)
BASE_PRECISION = symbol_info["baseAssetPrecision"]


def round_down(number, decimals):
    factor = 10 ** decimals
    return math.floor(number * factor) / factor


SPENDING_AMOUNT = round_down(SPENDING_AMOUNT, symbol_info["quoteAssetPrecision"])
print(client.get_asset_balance(BUY_TYPE)["free"], client.get_asset_balance(SELL_TYPE)["free"])
order = client.order_market_sell(symbol=SYMBOL, quantity=1)
print(order)
print(client.get_asset_balance(BUY_TYPE)["free"], client.get_asset_balance(SELL_TYPE)["free"])
exit()

def trade_callback(data):
    if data['p']:
        global IN, IN_PRICE, MAX_PRICE, DOUBLE_OUT, TRIPLE_OUT, DOUBLE_VAL, TRIPLE_VAL, BOTTOM_VAL
        global BUY_TYPE, SELL_TYPE, SPENDING_AMOUNT, BALANCE, BASE_PRECISION
        global START_TIME
        print(client.get_open_orders(symbol=SYMBOL))
        print(client.get_asset_balance(BUY_TYPE)["free"], client.get_asset_balance(SELL_TYPE)["free"], data['p'])
        current_price = float(data['p'])
        MAX_PRICE = max(current_price, MAX_PRICE)
        if not IN:
            IN_PRICE = float(data['p'])
            client.order_market_buy(symbol=SYMBOL, quoteOrderQty=SPENDING_AMOUNT)
            DOUBLE_VAL = IN_PRICE * 1.00001
            TRIPLE_VAL = IN_PRICE * 1.00002
            BOTTOM_VAL = IN_PRICE * 0.99999
            BALANCE = round_down(float(client.get_asset_balance(asset=BUY_TYPE)["free"]), BASE_PRECISION)
            IN = True
            START_TIME = time.time()
        else:
            if current_price <= BOTTOM_VAL:
                print("selling")
                client.order_market_sell(symbol=SYMBOL, quantity=BALANCE)
                sys.exit()
            elif not DOUBLE_OUT and current_price >= DOUBLE_VAL:
                BALANCE = round_down(BALANCE*0.5, BASE_PRECISION)
                client.order_market_sell(symbol=SYMBOL, quantity=BALANCE)
                print("two")
                DOUBLE_OUT = True
            elif not TRIPLE_OUT and current_price >= TRIPLE_VAL:
                to_sell = round_down(BALANCE*0.75, BASE_PRECISION)
                client.order_market_sell(symbol=SYMBOL, quantity=to_sell)
                print("tri")
                BALANCE -= to_sell
                BALANCE = round_down(BALANCE, BASE_PRECISION)
                TRIPLE_OUT = True
            elif DOUBLE_OUT and TRIPLE_OUT and current_price <= MAX_PRICE * 0.95: # i don't like this multiplication here slows down?
                print("trail selling")
                client.order_market_sell(symbol=SYMBOL, quantity=BALANCE)
                sys.exit()
            elif time.time() - START_TIME >= 58:
                client.order_market_sell(symbol=SYMBOL, quantity=BALANCE)
                sys.exit()
    else:
        print("no trades")


trade_sock = sock_manager.start_trade_socket(symbol=SYMBOL, callback=trade_callback)
sock_manager.run()
