import os
from dotenv import load_dotenv
from binance.client import Client
from binance.websockets import BinanceSocketManager
from luna_modules.kline_patterns import kline_helpers
from luna_modules.kline_patterns.patterns import pattern_matches
from luna_modules.impulse_detector.detect_impulse import is_impulse_wave

load_dotenv(dotenv_path="../.env.local")
client = Client(os.environ["api_key"], os.environ["api_secret"])

symbols = {
    "BTCUSDT": []
}

sock_manager = BinanceSocketManager(client)


def callback(data):  # function call for each socket data
    symbol = data['s']
    klines = symbols[symbol][1]
    last_kline = kline_helpers.convert_socket_kline(data['k'])
    print(symbol, pattern_matches([*klines, last_kline]))
    if data['k']['x']:
        klines.append(last_kline)
        print("kline timeframe finished. Impulse:", is_impulse_wave(klines))
        klines.pop(0)


count = 1
for symbol in symbols:
    print(f"Loading symbol {symbol}, {round((count / len(symbols) * 100), 2)}% done")
    curr_key = sock_manager.start_kline_socket(symbol, callback, interval=client.KLINE_INTERVAL_1MINUTE)
    kline_history = client.get_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, "2 MINUTES AGO UTC")
    symbols[symbol] = [curr_key, [list(map(float, x)) for x in kline_history]]
    count += 1
sock_manager.start()  # initate connection
