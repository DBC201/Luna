import os
from dotenv import load_dotenv
from binance.client import Client
from binance.websockets import BinanceSocketManager

load_dotenv(dotenv_path="./.env.local")
client = Client(os.environ["api_key"], os.environ["api_secret"])


def callback(data): # function call for each socket data
    pass


exchange_info = client.get_exchange_info()
symbols = {s["symbol"]: [] for s in exchange_info["symbols"]} # symbol: [identifier, kline_history]
if len(symbols) > 1024:
    raise RuntimeError("More symbols than the allowed maximum")
sock_manager = BinanceSocketManager(client)
for symbol in symbols:
    curr_key = sock_manager.start_kline_socket(symbol, callback, interval=client.KLINE_INTERVAL_15MINUTE)
    kline_history = client.get_historical_klines(symbol, client.KLINE_INTERVAL_15MINUTE, "1 hour ago")
    symbols[symbol] = [curr_key, [list(map(float, x)) for x in kline_history]]
sock_manager.start() # initate connection