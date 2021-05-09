import os, sys
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
from luna_modules.trade_analysis.TradeAnalyzer import TradeAnalyzer

if __name__ == '__main__':
    trades_path = os.path.join(ROOT, "trades")
    file_name = "ETHUSDT_2021-05-07_00.38.02.json"
    analyzer = TradeAnalyzer(os.path.join(trades_path, file_name))
    analyzer.draw(1000)
    analyzer.save_graph(os.path.join(trades_path, file_name.replace(".json", ".png")))
