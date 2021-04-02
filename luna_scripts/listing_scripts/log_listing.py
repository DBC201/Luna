import sys, argparse
import os
from dotenv import load_dotenv
from binance.client import Client
from binance.websockets import BinanceSocketManager
import time, datetime
import json
from twisted.internet import reactor


def return_parser():
    parser = argparse.ArgumentParser(description="Log minute trades")
    parser.add_argument("symbol", type=str, help="trades to log (ex:BTCUSDT)")
    parser.add_argument("dump_path", type=str, help="directory to dump trades")
    parser.add_argument("env_path", type=str, help="file path for env variables")
    return parser


args = return_parser().parse_args(sys.argv[1:])
SYMBOL = args.symbol
env_path = args.env_path
load_dotenv(dotenv_path=env_path)
client = Client(os.environ["api_key"], os.environ["api_secret"])
TRADES = []


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
    global START, TRADES
    TRADES.append(data)
    if time.time() - START >= 60:
        shutdown()


sock_manager = BinanceSocketManager(client)
trade_sock = sock_manager.start_trade_socket(symbol=SYMBOL, callback=trade_callback)
START = time.time()
sock_manager.run()
