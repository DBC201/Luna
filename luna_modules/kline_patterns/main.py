from binance.client import Client
from binance.websockets import BinanceSocketManager
from luna_modules.kline_patterns.Kline import Kline
from luna_modules.kline_patterns.KlinePatterns import KlinePatterns

client = Client()

symbols = {
    "BTCUSDT": KlinePatterns([])
}

sock_manager = BinanceSocketManager(client)


def callback(data):  # function call for each socket data
    current_kline = Kline(Kline.convert_socket_kline(data['k']))
    klinePatterns = symbols[data['s']]
    klinePatterns.add_new_kline(current_kline)
    print(klinePatterns.get_patterns())
    klinePatterns.pop_kline(-1)
    if data['k']['x']:
        symbols[data['s']].add_new_kline(current_kline)
        symbols[data['s']].pop_kline(0)
        print("kline timeframe finished")


count = 1
for symbol in symbols:
    print(f"Loading symbol {symbol}, {round((count / len(symbols) * 100), 2)}% done")
    curr_key = sock_manager.start_kline_socket(symbol, callback, interval=client.KLINE_INTERVAL_1MINUTE)
    kline_data = client.get_historical_klines(symbol, client.KLINE_INTERVAL_1MINUTE, "3 minutes ago UTC")
    kline_data = [list(map(float, x)) for x in kline_data] # convert strings to float
    klinePatterns = symbols[symbol]
    for data in kline_data:
        klinePatterns.add_new_kline(Kline(data))
    print(klinePatterns.get_patterns())
    count += 1
sock_manager.start()  # initate connection
