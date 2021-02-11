import os
from dotenv import load_dotenv
from binance.client import Client
from luna_modules.indicators.fib import fib_breaking_points

load_dotenv(dotenv_path="../.env.local")
client = Client(os.environ["api_key"], os.environ["api_secret"])

exchange_info = client.get_exchange_info()
#symbols = {s["symbol"]: [] for s in exchange_info["symbols"]} # symbol: [min, max]
symbols = {
    "BTCUSDT":[]
}

for symbol in symbols:
    raw_klines = client.get_historical_klines(symbol, client.KLINE_INTERVAL_1DAY, "100 days ago UTC")
    history = [list(map(float, l)) for l in raw_klines]
    max_val = max(history, key=lambda l: l[2])[2]
    min_val = min(history, key=lambda l: l[3])[3]
    print(symbol, fib_breaking_points(min_val, max_val))
