from binance.client import Client
import json
import datetime
import os
from dotenv import load_dotenv

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")


load_dotenv(dotenv_path=os.path.join(ROOT, ".env.local"))
client = Client(api_key=os.environ["api_key"], api_secret=os.environ["api_secret"])
DUMP_FOLDER = os.path.join(ROOT, "historical_trades")


def dump_minute_trades(symbol):
    """Dump minute trades for a symbol

    A single trade representation:

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
    trades = client.get_historical_trades(symbol=symbol, fromId=id)
    start_time = trades[0]["time"]/1000
    while True:
        seconds = trades[-1]["time"]/1000 - start_time
        if seconds >= 60:
            break
        id = len(trades)
        trades += client.get_historical_trades(symbol=symbol, fromId=id)
    time_str = datetime.datetime.utcfromtimestamp(trades[0]["time"]/1000).strftime('%Y-%m-%d_%H.%M.%S')
    file_path = os.path.join(DUMP_FOLDER, symbol + '_' + time_str + ".json")
    with open(file_path, 'w') as file:
        json.dump(trades, file)


if __name__ == '__main__':
    if not os.path.isdir(DUMP_FOLDER):
        os.makedirs(DUMP_FOLDER)
    tickers = client.get_all_tickers()
    existing_files = os.listdir(DUMP_FOLDER)
    existing_trades = {}
    for filename in existing_files:
        symbol = filename.split('_')[0]
        existing_trades.update({symbol: True})
    i = 0
    for ticker in tickers:
        print("{}% done".format((i/len(tickers)*100)))
        symbol = ticker["symbol"]
        if symbol not in existing_trades:
            dump_minute_trades(symbol)
            existing_trades.update({symbol: True})
        i += 1
