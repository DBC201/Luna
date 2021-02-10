import os
from dotenv import load_dotenv
from binance.client import Client
from binance.websockets import BinanceSocketManager
from luna_modules.kline_patterns import kline_helpers
from luna_modules.kline_patterns.patterns import pattern_matches

load_dotenv(dotenv_path="../.env.local")
client = Client(os.environ["api_key"], os.environ["api_secret"])

symbols = {
    "BTCUSDT": [],
    "DOGEUSDT": []
}

sock_manager = BinanceSocketManager(client)


def callback(data):  # function call for each socket data
    symbol = data['s']
    if data['k']['x']:
        symbols[symbol][1].append(kline_helpers.convert_socket_kline(data['k']))
        klines = symbols[symbol][1]
        print(symbol, pattern_matches(klines))


count = 1
for symbol in symbols:
    print(f"Loading symbol {symbol}, {round((count / len(symbols) * 100), 2)}% done")
    curr_key = sock_manager.start_kline_socket(symbol, callback, interval=client.KLINE_INTERVAL_15MINUTE)
    kline_history = client.get_historical_klines(symbol, client.KLINE_INTERVAL_15MINUTE, "1 hour ago UTC")
    symbols[symbol] = [curr_key, [list(map(float, x)) for x in kline_history]]
    print(symbol, pattern_matches(symbols[symbol][1]))
    count += 1
sock_manager.start()  # initate connection
