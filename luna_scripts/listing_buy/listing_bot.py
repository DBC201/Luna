import os
import sys
import argparse
from dotenv import load_dotenv
from binance.client import Client
from binance import ThreadedWebsocketManager
import time
import math


def return_parser():
    parser = argparse.ArgumentParser(description="Auto buy listing")
    parser.add_argument("buy_type", type=str, help="Coin to buy (ex:BTC)")
    parser.add_argument("sell_type", type=str, help="Coin to pay with (ex:USDT)")
    parser.add_argument("spending_amount", type=float, help="Amount to pay")
    parser.add_argument("env_path", type=str, help="file path for env variables")
    return parser


args = return_parser().parse_args(sys.argv[1:])
BUY_TYPE = args.buy_type.upper()
SELL_TYPE = args.sell_type.upper()
SPENDING_AMOUNT = args.spending_amount
env_path = args.env_path
SYMBOL = BUY_TYPE + SELL_TYPE

load_dotenv(dotenv_path=env_path)
client = Client(os.environ["api_key"], os.environ["api_secret"])
sock_manager = ThreadedWebsocketManager()
sock_manager.start()

IN_PRICE = sys.maxsize
MAX_PRICE = 0
DOUBLE_OUT = False
TRIPLE_OUT = False
DOUBLE_VAL = 0
TRIPLE_VAL = 0
BOTTOM_VAL = sys.maxsize
BALANCE = 0
START_TIME = None
BASE_PRECISION = 8
STOPPED = False


def round_down(number, decimals):
    factor = 10 ** decimals
    return math.floor(number * factor) / factor


def trade_callback(data):
    global IN_PRICE, MAX_PRICE, DOUBLE_OUT, TRIPLE_OUT, DOUBLE_VAL, TRIPLE_VAL, BOTTOM_VAL
    global BUY_TYPE, SELL_TYPE, SPENDING_AMOUNT, BALANCE, BASE_PRECISION
    global START_TIME, STOPPED
    if STOPPED:
        return
    current_price = float(data['p'])
    MAX_PRICE = max(current_price, MAX_PRICE)
    current_time = data['T']
    if current_time - START_TIME >= 58:
        client.order_market_sell(symbol=SYMBOL, quantity=BALANCE)
        STOPPED = True
        return
    try:
        if not START_TIME:
            IN_PRICE = current_price
            order = client.order_market_buy(symbol=SYMBOL, quoteOrderQty=SPENDING_AMOUNT)
            START_TIME = float(order["transactTime"]) / 1000
            DOUBLE_VAL = IN_PRICE * 2
            TRIPLE_VAL = IN_PRICE * 3
            BOTTOM_VAL = IN_PRICE * 0.87
            BASE_PRECISION = len(order["executedQty"]) - order["executedQty"].find('.') - 1
            BALANCE = round_down(float(order["executedQty"]),
                                 BASE_PRECISION)  # maybe remove round down for optimization?
        else:
            if not DOUBLE_OUT and current_price >= DOUBLE_VAL:
                to_sell = round_down(BALANCE * 0.5, BASE_PRECISION)
                client.order_market_sell(symbol=SYMBOL, quantity=to_sell)
                BALANCE = to_sell
                DOUBLE_OUT = True
            elif not TRIPLE_OUT and current_price >= TRIPLE_VAL:
                to_sell = round_down(BALANCE * 0.75, BASE_PRECISION)
                client.order_market_sell(symbol=SYMBOL, quantity=to_sell)
                BALANCE -= to_sell
                BALANCE = round_down(BALANCE, BASE_PRECISION)
                TRIPLE_OUT = True
            elif current_price <= MAX_PRICE * 0.87:
                client.order_market_sell(symbol=SYMBOL, quantity=BALANCE)
                STOPPED = True
    except Exception as e:
        print(e)
        BALANCE = round_down(float(client.get_asset_balance(asset=BUY_TYPE)["free"]), BASE_PRECISION)
        client.order_market_sell(symbol=SYMBOL, quantity=BALANCE)
        STOPPED = True


sock_manager.start_trade_socket(symbol=SYMBOL, callback=trade_callback)
while not STOPPED:
    time.sleep(1)
sock_manager.stop()
