import sys, argparse
import os
from binance import ThreadedWebsocketManager
import time, datetime
import json


def return_parser():
    parser = argparse.ArgumentParser(description="Log minute trades in binance")
    parser.add_argument("symbol", type=str, help="trades to log (ex:BTCUSDT)")
    parser.add_argument("dump_path", type=str, help="directory to dump trades")
    parser.add_argument("-d", "--duration", type=int, dest="duration", help="time in seconds")
    return parser


args = return_parser().parse_args(sys.argv[1:])
SYMBOL = args.symbol.upper()
DURATION = 60 # in seconds
DUMP_PATH = args.dump_path
if args.duration:
    DURATION = args.duration
sock_manager = ThreadedWebsocketManager()
sock_manager.start()
TRADES = []
TRADE_INIT = False
START = sys.maxsize


def write_data():
    time_str = datetime.datetime.utcfromtimestamp(START).strftime('%Y-%m-%d_%H.%M.%S')
    path = os.path.join(DUMP_PATH, SYMBOL + '_' + time_str + ".json")
    with open(path, 'w') as file:
        json.dump(TRADES, file)


def shutdown():
    sock_manager.stop()
    sys.exit()


def trade_callback(data):
    global START, TRADES, TRADE_INIT
    print(data)
    if data:
        if not TRADE_INIT:
            TRADE_INIT = True
            START = time.time()
        else:
            TRADES.append(data)
            if time.time() - START >= DURATION:
                write_data()
                shutdown()


sock_manager.start_trade_socket(callback=trade_callback, symbol=SYMBOL)
