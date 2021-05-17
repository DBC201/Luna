import sys, os
CURR = os.path.dirname(__file__)
ROOT = os.path.join(CURR, "..")
sys.path.append(ROOT)
from luna_modules.binance.BinanceLog import BinanceLog

if __name__ == '__main__':
    binanceLog = BinanceLog(symbols=["btcusdt", "ethusdt"])
    binanceLog.log(3)
    binanceLog.dump(os.path.join(ROOT, "trades"))
    binanceLog.clear_logs()
