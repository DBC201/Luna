import os
import random
import sys
import time
from dotenv import load_dotenv

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
from luna_modules.email.EmailWrapper import EmailWrapper
from luna_modules.binance.BinanceApiWrapper import BinanceApiWrapper

ENV_PATH = os.path.join(ROOT, ".env.local")
load_dotenv(dotenv_path=ENV_PATH)
apiWrapper = BinanceApiWrapper(os.environ["api_key"], os.environ["api_secret"])

emailWrapper = EmailWrapper(
    port=os.environ["ssl_port"],
    smtp_server=os.environ["smtp_server"],
    sender_email=os.environ["email"],
    password=os.environ["email_password"]
)


def send_bogdanoff(ticker):
    """
    Whales are out, inform everyone in mail list

    :param ticker: ticker that will be sent in mail
    :type ticker: string
    :return: None
    """
    subject = "Dump EET --- " + ticker
    body = "https://www.binance.com/en/trade/" + ticker
    img = "dump/" + random.choice(os.listdir(os.path.join(ROOT, "luna_scripts", "meme", "dump")))
    emailWrapper.database_send(subject, body, img)


def send_jesse(ticker):
    """
    Whales are in, inform everyone in mail list

    :param ticker: ticker that will be sent in mail
    :type ticker: string
    :return: None
    """
    subject = "Pump EET --- " + ticker
    body = "https://www.binance.com/en/trade/" + ticker
    img = "pump/" + random.choice(os.listdir((os.path.join(ROOT, "luna_scripts", "meme", "pump"))))
    emailWrapper.database_send(subject, body, img)


def get_vitalik_on_the_line(ticker):
    """
    Put Vitalik on zhe line

    :param ticker: ticker that will be sent in mail
    :type ticker: string
    :return: None
    """
    subject = "Get Vitalik On The Line --- " + ticker
    body = "https://www.binance.com/en/trade/" + ticker
    img = "vitalik/" + random.choice(os.listdir((os.path.join(ROOT, "luna_scripts", "meme", "vitalik"))))
    emailWrapper.database_send(subject, body, img)


class Ticker:
    """
    Contains data about ticker name, price at last hour and current price

    Ex: "BTCUSDT" 65000 66000
    """

    def __init__(self, identifier, initial_price, current_price):
        self.identifier = identifier
        self.initial_price = initial_price
        self.current_price = current_price
        self.reset()

    def reset(self):
        """
        Set all mail flags to false

        :return: None
        """
        self.dumped = False
        self.pumped = False
        self.called_vitalik = False


if __name__ == '__main__':
    # Get prices for all tickers and initialize them
    initial_prices = apiWrapper.get_price_dict()
    tickers = dict()
    for p in initial_prices:
        tickers[p] = Ticker(p, initial_prices[p], initial_prices[p])
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
            if (t.current_price < t.initial_price * 0.9) and not t.dumped:
                send_bogdanoff(t.identifier)
                t.dumped = True
            if (t.current_price > t.initial_price * 1.1) and not t.pumped:
                send_jesse(t.identifier)
                t.pumped = True
            if (t.current_price > t.initial_price * 1.5) and not t.called_vitalik:
                get_vitalik_on_the_line(t.identifier)
                t.called_vitalik = True
        # update old price every hour
        minutes += 1
        if minutes % 60 == 0:
            initial_prices = current_prices
            for name in tickers:
                tickers[name].reset()
        time.sleep(60)
