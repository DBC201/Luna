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
    def __init__(self, identifier, price):
        self.identifier = identifier
        self.price = price
        self.reset()

    def reset(self):
        self.dumped = False
        self.pumped = False
        self.called_vitalik = False


if __name__ == '__main__':
    initial_prices = apiWrapper.get_price_dict()
    tickers = dict()
    # TODO
    for p in initial_prices:
        ticker = Ticker(p, initial_prices[p])
        tickers[p] = ticker
    minutes = 0
    while True:
        price = float(client.get_symbol_ticker(symbol=TICKER)["price"])
        if (price < initial_price * 0.9) and not dumped:
            send_bogdanoff(TICKER)
            dumped = True
        if (price > initial_price * 1.1) and not pumped:
            send_jesse(TICKER)
            pumped = True
        if (price > initial_price * 1.5) and not called_vitalik:
            get_vitalik_on_the_line(TICKER)
            called_vitalik = True
        # update old price every hour
        minutes += 1
        if minutes % 60 == 0:
            initial_price = price
            dumped = False
            pumped = False
            called_vitalik = False
        time.sleep(60)
