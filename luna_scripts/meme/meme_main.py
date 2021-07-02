import os
import sys
import time

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)

from luna_modules.binance.BinanceApiWrapper import BinanceApiWrapper
# from EmailMemes import EmailMemes
import DiscordBot

apiWrapper = BinanceApiWrapper()


class Ticker:
    """
    Contains data about ticker name, price at last hour and current price

    Ex: "BTCUSDT" 65000 66000

    :param identifier: ticker symbol (ex: "BTCUSDT")
    :type identifier: string
    :param initial_price: price of coin
    :type initial_price: float
    """

    def __init__(self, identifier, initial_price):
        self.identifier = identifier
        self.initial_price = initial_price
        self.current_price = self.initial_price
        self.reset()

    def reset(self):
        """
        Set all mail flags to false and reset the initial price

        :return: None
        """
        self.dumped = False
        self.pumped = False
        self.called_vitalik = False
        self.initial_price = self.current_price


if __name__ == '__main__':
    # Get prices for all tickers and initialize them
    initial_prices = apiWrapper.get_price_dict()
    tickers = dict()
    for p in initial_prices:
        tickers[p] = Ticker(p, initial_prices[p])
    # Check every minute for price fluctuations
    minutes = 0
    while True:
        # Update current prices of all tickers
        current_prices = apiWrapper.get_price_dict()
        for name in tickers:
            tickers[name].current_price = current_prices[name]
        # Check prices for all tickers
        for name in tickers:
            t = tickers[name]
            # Check USDT parities only
            if t.identifier[-4:] != "USDT":
                continue
            if (t.current_price < t.initial_price * 0.9) and not t.dumped:
                # EmailMemes.send_bogdanoff(t.identifier)
                DiscordBot.dump_eet(t.identifier)
                t.dumped = True
            if (t.current_price > t.initial_price * 1.1) and not t.pumped:
                # EmailMemes.send_jesse(t.identifier)
                DiscordBot.pump_eet(t.identifier)
                t.pumped = True
            if (t.current_price > t.initial_price * 1.5) and not t.called_vitalik:
                # EmailMemes.get_vitalik_on_the_line(t.identifier)
                DiscordBot.call_vitalik(t.identifier)
                t.called_vitalik = True
        # update old price every hour
        minutes += 1
        if minutes % 60 == 0:
            for name in tickers:
                tickers[name].reset()
        time.sleep(60)
