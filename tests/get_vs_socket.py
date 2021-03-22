import time
import os
from dotenv import load_dotenv
from binance.client import Client
from binance.websockets import BinanceSocketManager

load_dotenv(dotenv_path="../.env.local")
client = Client(os.environ["api_key"], os.environ["api_secret"])

client.API_URL = 'https://testnet.binance.vision/api'
symbol = "BTCUSDT"

start = time.time()
client.get_symbol_ticker(symbol=symbol)
end = time.time()
print("Get request time:", end-start)


def trade_callback(data):
    global trade_start
    print("trade_time", time.time()-trade_start)
    trade_start = time.time()


def agg_trade_callback(data):
    global agg_start
    print("agg_trade time", time.time()-agg_start)
    agg_start = time.time()


sock_manager = BinanceSocketManager(client)
trade_key = sock_manager.start_trade_socket(symbol=symbol, callback=trade_callback)
agg_trade_key = sock_manager.start_aggtrade_socket(symbol=symbol, callback=agg_trade_callback)

agg_start = time.time()
trade_start = time.time()
sock_manager.start()

