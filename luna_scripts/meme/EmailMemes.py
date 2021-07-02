import os, sys
from dotenv import load_dotenv
import random

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
from luna_modules.email.EmailWrapper import EmailWrapper


ENV_PATH = os.path.join(ROOT, ".env.local")
load_dotenv(dotenv_path=ENV_PATH)

emailWrapper = EmailWrapper(
    port=int(os.environ["ssl_port"]),
    smtp_server=os.environ["smtp_server"],
    sender_email=os.environ["email"],
    password=os.environ["email_password"],
    signature_text="https://bogdanoff.pw"
)


class EmailMemes:
    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
