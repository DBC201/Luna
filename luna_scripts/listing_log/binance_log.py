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
START_TIME = None
STOPPED = False


def write_data():
    time_str = datetime.datetime.utcfromtimestamp(START_TIME).strftime('%Y-%m-%d_%H.%M.%S')
    path = os.path.join(DUMP_PATH, SYMBOL + '_' + time_str + ".json")
    with open(path, 'w') as file:
        json.dump(TRADES, file)


def trade_callback(data):
    global START_TIME, TRADES, STOPPED
    if STOPPED:
        return
    current_time = data['T']/1000
    if not START_TIME:
        START_TIME = current_time
    else:
        TRADES.append(data)
        if current_time - START_TIME >= DURATION:
            STOPPED = True


sock_manager.start_trade_socket(callback=trade_callback, symbol=SYMBOL)
while not STOPPED:
    time.sleep(1)
sock_manager.stop()
write_data()
