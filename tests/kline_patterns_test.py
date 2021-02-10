import os
from dotenv import load_dotenv
from binance.client import Client
from binance.websockets import BinanceSocketManager
from luna_modules.kline_patterns import kline_helpers
from luna_modules.kline_patterns import patterns

load_dotenv(dotenv_path="../.env.local")
client = Client(os.environ["api_key"], os.environ["api_secret"])

symbols = {
    "BTCUSDT": [],
    "DOGEUSDT": []
}

sock_manager = BinanceSocketManager(client)
def callback(data): # function call for each socket data
    symbol = data['s']
    if data['k']['x']:
        symbols[symbol][1].append(kline_helpers.convert_socket_kline(data['k']))
        if patterns.is_hammer(symbols[symbol][1]):
            print(symbol, "is hammer")
        if patterns.is_hanging_man(symbols[symbol][1]):
            print(symbol, "is hanging man")


count = 1
for symbol in symbols:
    print(f"Loading symbol {symbol}, {round((count/len(symbols)*100), 2)}% done")
    curr_key = sock_manager.start_kline_socket(symbol, callback, interval=client.KLINE_INTERVAL_15MINUTE)
    kline_history = client.get_historical_klines(symbol, client.KLINE_INTERVAL_15MINUTE, "4 hours ago")
    symbols[symbol] = [curr_key, kline_history]
    count += 1
sock_manager.start() # initate connection