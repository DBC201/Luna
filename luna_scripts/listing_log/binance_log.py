import sys, argparse
import os
from binance.client import Client
from binance.websockets import BinanceSocketManager
import time, datetime
import json
from twisted.internet import reactor


def return_parser():
    parser = argparse.ArgumentParser(description="Log minute trades in binance")
    parser.add_argument("symbol", type=str, help="trades to log (ex:BTCUSDT)")
    parser.add_argument("dump_path", type=str, help="directory to dump trades")
    parser.add_argument("-d", "--duration", type=int, dest="duration", help="time in seconds")
    return parser


args = return_parser().parse_args(sys.argv[1:])
SYMBOL = args.symbol.upper()
client = Client()
DURATION = 60 # in seconds
if args.duration:
    DURATION = args.duration
TRADES = []
TRADE_INIT = False
START = sys.maxsize


def shutdown():
    try:
        reactor.stop()
    except:
        pass
    time_str = datetime.datetime.utcfromtimestamp(START).strftime('%Y-%m-%d_%H.%M.%S')
    path = os.path.join(args.dump_path, SYMBOL+'_'+time_str+".json")
    with open(path, 'w') as file:
        json.dump(TRADES, file)
    sys.exit()


def trade_callback(data):
    global START, TRADES, TRADE_INIT
    if data:
        if not TRADE_INIT:
            TRADE_INIT = True
            START = time.time()
        else:
            TRADES.append(data)
            if time.time() - START >= DURATION:
                shutdown()


sock_manager = BinanceSocketManager(client)
trade_sock = sock_manager.start_trade_socket(symbol=SYMBOL, callback=trade_callback)
sock_manager.run()
