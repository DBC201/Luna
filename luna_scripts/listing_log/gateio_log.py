import json
import datetime
import os
import sys
from dotenv import load_dotenv
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
from luna_modules.gate_io.GateApiWrapper import get_first_thousand_orders, get_all_tickers

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")

load_dotenv(dotenv_path=os.path.join(ROOT, ".env.local"))
DUMP_FOLDER = os.path.join(ROOT, "historical_trades", "gate_io")


def main():
    # create dump folder if it doesn't exist
    if not os.path.isdir(DUMP_FOLDER):
        os.makedirs(DUMP_FOLDER)
    # don't take existing info again
    existing_files = os.listdir(DUMP_FOLDER)
    existing_trades = set()
    for filename in existing_files:
        symbol = filename.split('-')[0]
        existing_trades.add(symbol)
    # dump info for all non existing symbols
    tickers = get_all_tickers()
    i = 0
    for ticker in tickers:
        print("{}% done".format((i / len(tickers) * 100)))
        symbol = ticker["id"]
        if symbol not in existing_trades:
            dump_minute_trades(symbol)
            existing_trades.add(symbol)
        i += 1


def dump_minute_trades(symbol):
    """Dump minute trades for a symbol

    A single trade representation:
      {
        "id": "1232893232",
        "create_time": "1548000000",
        "create_time_ms": "1548000000123.456",
        "order_id": "4128442423",
        "side": "buy",
        "role": "maker",
        "amount": "0.15",
        "price": "0.03",
        "fee": "0.0005",
        "fee_currency": "ETH",
        "point_fee": "0",
        "gt_fee": "0"
      }
    """
    last_id = 1
    trades = get_first_thousand_orders(symbol, last_id)
    if len(trades) == 0:
        print(symbol + " is empty")
        return
    start_time = float(trades[-1]["create_time_ms"])
    while True:
        milliseconds = float(trades[0]["create_time_ms"]) - start_time
        if milliseconds >= 60_000:
            break
        last_id = trades[0]["id"]
        trades = get_first_thousand_orders(symbol, last_id) + trades
    time_str = datetime.datetime.utcfromtimestamp(start_time / 1000).strftime('%Y-%m-%d_%H.%M.%S')
    file_path = os.path.join(DUMP_FOLDER, symbol + '-' + time_str + ".json")
    with open(file_path, 'w') as file:
        json.dump(trades, file)


if __name__ == '__main__':
    main()
