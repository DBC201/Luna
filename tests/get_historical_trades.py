from binance.client import Client
import json
import datetime
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env.local")
client = Client(api_key=os.environ["api_key"], api_secret=os.environ["api_secret"])


def get_trade_second(trade):
    return int(trade["time"])/1000


symbol = "BTCUSDT"
dump_folder = "../trades"

"""
[
  {
    "id": 28457,
    "price": "4.00000100",
    "qty": "12.00000000",
    "quoteQty": "48.000012",
    "time": 1499865549590, // Trade executed timestamp, as same as `T` in the stream
    "isBuyerMaker": true,
    "isBestMatch": true
  }
]
"""


id = 0
while True:
    trades = client.get_historical_trades(symbol=symbol, fromId=id)
    last_trade_time = get_trade_second(trades[-1])
    id = trades[-1]["id"] + 1
    if last_trade_time >= 60:
        break
time_str = datetime.datetime.utcfromtimestamp(get_trade_second(trades[0])).strftime('%Y-%m-%d_%H.%M.%S')
file_path = os.path.join(dump_folder, symbol + '_' + time_str + ".json")
with open(file_path, 'w') as file:
    json.dump(trades, file)
