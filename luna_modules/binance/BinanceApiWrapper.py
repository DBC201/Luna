from binance.client import Client
import math


class BinanceApiWrapper:
    """A simple Api Wrapper

    :param key: api key
    :type key: string
    :param secret: api secret
    :type secret: string
    :param url: change this if you want to use the test api
    :type url: string
    """
    def __init__(self, key=None, secret=None, url=None):
        if key and secret:
            self.client = Client(key, secret)
        else:
            self.client = Client()
        if url:
            self.client.API_URL = url

    @staticmethod
    def round_down(number, decimals):
        """Round down decimal points

        :param number: float to round down
        :type number: float
        :param decimals: amount of digits to round down to
        :type decimals: int
        :return: rounded number
        :rtype: float
        """
        factor = 10 ** decimals
        return math.floor(number * factor) / factor

    def get_balance(self, coin):
        """Get account balance for a given coin

        :param coin: coin type (Ex:"BTC")
        :type coin: string
        :return: balance
        :rtype: float
        """
        return float(self.client.get_asset_balance(coin.upper())["free"])

    def market_buy(self, to_buy, to_sell, sell_amount):
        """Buy a coin using another

        Ex: Buying BTC by spending USDT

        :param to_buy: coin to buy(ex: BTC)
        :type to_buy: string
        :param to_sell: coin to spend(ex: USDT)
        :type to_sell: string
        :param sell_amount: amount to spend (ex: how much usdt will be spent)
        :type sell_amount: float
        :return: transaction details
        :rtype: dict
        """
        symbol = to_buy.upper()+to_sell.upper()
        base_precision = self.client.get_symbol_info(symbol)["baseAssetPrecision"]
        return self.client.order_market_buy(symbol=symbol, quoteOrderQty=BinanceApiWrapper.round_down(sell_amount, base_precision))

    def market_sell(self, to_sell, to_buy, sell_amount):
        """Sell a coin

        Ex: sell BTC and get USDT

        :param to_sell: coin to sell (ex: BTC)
        :type to_sell: string
        :param to_buy: coin to get after transaction (ex: USDT)
        :type to_buy: string
        :param sell_amount: amount to sell (ex: how much BTC will be spent)
        :type sell_amount: float
        :return: transaction details
        :rtype: dict
        """
        symbol = to_buy.upper() + to_sell.upper()
        base_precision = self.client.get_symbol_info(symbol)["baseAssetPrecision"]
        return self.client.order_market_buy(symbol=symbol, quantity=BinanceApiWrapper.round_down(sell_amount, base_precision))

    def get_price_dict(self):
        """Returns all the prices as a dictionary.

        Ex: {"ETHBTC": 0.06}

        :return: prices
        :rtype: dict
        """
        raw = self.client.get_symbol_ticker()
        prices = dict()
        for r in raw:
            prices[r["symbol"]] = float(r["price"])
        return prices
