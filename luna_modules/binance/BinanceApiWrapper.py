from binance.client import Client
import math

class BinanceApiWrapper:
    def __init__(self, key, secret, url=None):
        self.client = Client(key, secret)
        if url:
            self.client.API_URL = url

    def __round_down(self, number, decimals):
        factor = 10 ** decimals
        return math.floor(number * factor) / factor

    def get_balance(self, coin):
        return float(self.client.get_asset_balance(coin.upper())["free"])

    def market_buy(self, to_buy, to_sell, sell_amount):
        symbol = to_buy.upper()+to_sell.upper()
        base_precision = self.client.get_symbol_info(symbol)["baseAssetPrecision"]
        return self.client.order_market_buy(symbol=symbol, quoteOrderQty=self.__round_down(sell_amount, base_precision))

    def market_sell(self, to_sell, to_buy, sell_amount):
        symbol = to_buy.upper() + to_sell.upper()
        base_precision = self.client.get_symbol_info(symbol)["baseAssetPrecision"]
        return self.client.order_market_buy(symbol=symbol, quantity=self.__round_down(sell_amount, base_precision))
