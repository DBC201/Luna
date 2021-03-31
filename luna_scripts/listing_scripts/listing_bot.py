import os
import sys
import argparse
from dotenv import load_dotenv
from binance.client import Client
from binance.websockets import BinanceSocketManager
import time
import math
from twisted.internet import reactor

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
sock_manager = BinanceSocketManager(client)

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
min_amount = float(symbol_info["filters"][3]["minNotional"])
min_amount += min_amount*0.1 + min_amount*0.05  # trading fee and min exit margin for getting out of stop loss
# stop loss still might fail in case of drastic price drops if the value drops below min notional
if SPENDING_AMOUNT <= min_amount:
    raise RuntimeError("You must spend more than " + str(min_amount))


def shutdown(code=0):
    reactor.stop()
    sys.exit(code)


def trade_callback(data):
    if data['p']:
        global IN, IN_PRICE, MAX_PRICE, DOUBLE_OUT, TRIPLE_OUT, DOUBLE_VAL, TRIPLE_VAL, BOTTOM_VAL
        global BUY_TYPE, SELL_TYPE, SPENDING_AMOUNT, BALANCE, BASE_PRECISION
        global START_TIME
        current_price = float(data['p'])
        MAX_PRICE = max(current_price, MAX_PRICE)
        try:
            if not IN:
                IN_PRICE = current_price
                client.order_market_buy(symbol=SYMBOL, quoteOrderQty=SPENDING_AMOUNT)
                DOUBLE_VAL = IN_PRICE * 2
                TRIPLE_VAL = IN_PRICE * 3
                BOTTOM_VAL = IN_PRICE * 0.95
                BALANCE = round_down(float(client.get_asset_balance(asset=BUY_TYPE)["free"]), BASE_PRECISION)
                IN = True
                START_TIME = time.time()
            else:
                if current_price <= BOTTOM_VAL:
                    client.order_market_sell(symbol=SYMBOL, quantity=BALANCE)
                    shutdown()
                elif not DOUBLE_OUT and current_price >= DOUBLE_VAL:
                    to_sell = round_down(BALANCE*0.5, BASE_PRECISION)
                    client.order_market_sell(symbol=SYMBOL, quantity=to_sell)
                    BALANCE = to_sell
                    DOUBLE_OUT = True
                elif not TRIPLE_OUT and current_price >= TRIPLE_VAL:
                    to_sell = round_down(BALANCE*0.75, BASE_PRECISION)
                    client.order_market_sell(symbol=SYMBOL, quantity=to_sell)
                    BALANCE -= to_sell
                    BALANCE = round_down(BALANCE, BASE_PRECISION)
                    TRIPLE_OUT = True
                elif DOUBLE_OUT and TRIPLE_OUT and current_price <= MAX_PRICE * 0.95:
                    client.order_market_sell(symbol=SYMBOL, quantity=BALANCE)
                    shutdown()
                elif time.time() - START_TIME >= 58:
                    client.order_market_sell(symbol=SYMBOL, quantity=BALANCE)
                    shutdown()
        except Exception as e:
            print(e)
            BALANCE = round_down(float(client.get_asset_balance(asset=BUY_TYPE)["free"]), BASE_PRECISION)
            # getting balance this way is slow but safer since we have encountered an error
            client.order_market_sell(symbol=SYMBOL, quantity=BALANCE)
            # do something to confirm the sell order or notify the user
            shutdown(-1)
    else:
        print("no trades")


trade_sock = sock_manager.start_trade_socket(symbol=SYMBOL, callback=trade_callback)
sock_manager.run()
