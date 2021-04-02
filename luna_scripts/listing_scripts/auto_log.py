import os
import time
import dateparser
import calendar
import scrape_functions
import shlex, subprocess
from binance.client import Client
from dotenv import load_dotenv

ENV_PATH = "../../.env.local"
load_dotenv(dotenv_path=ENV_PATH)
client = Client(os.environ["api_key"], os.environ["api_secret"])

if __name__ == '__main__':
    last_listing = scrape_functions.scrape_titles()[0]
    listing_time = None
    symbol = None
    save_folder = "../../trades"
    coin_name = None

    while True:
        current_listing = scrape_functions.scrape_titles()[0]
        announcement_is_new = current_listing["title"] != last_listing["title"]
        if announcement_is_new:
            coin_name = scrape_functions.get_coin_name(current_listing["title"])
            if coin_name:
                time_str = scrape_functions.get_listing_time(current_listing["code"])
                ticker = scrape_functions.get_coin_name(current_listing)
                listing_time = calendar.timegm(dateparser.parse(time_str).timetuple())
        if listing_time is not None and time.time() + 60 >= listing_time:
            symbol = coin_name+"USDT"
            bot = subprocess.Popen(
                shlex.split(f"python log_listing.py {symbol} {save_folder} {ENV_PATH}"),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            listing_time = None
            coin_name = None
        last_listing = current_listing
        time.sleep(60)
