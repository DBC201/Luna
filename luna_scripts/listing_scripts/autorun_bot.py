import os
import time
import dateparser
import calendar
import send_mail
import shlex, subprocess
from binance.client import Client
from dotenv import load_dotenv

ENV_PATH = "../../.env.local"
load_dotenv(dotenv_path=ENV_PATH)
client = Client(os.environ["api_key"], os.environ["api_secret"])

if __name__ == '__main__':
    # TODO
    pass
