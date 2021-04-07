import os
import time
import dateparser
import calendar
from BinanceAnnouncementScrape import BinanceAnnouncementScrape
import shlex, subprocess
from binance.client import Client
from dotenv import load_dotenv

ENV_PATH = "../../.env.local"
load_dotenv(dotenv_path=ENV_PATH)
client = Client(os.environ["api_key"], os.environ["api_secret"])

if __name__ == '__main__':
    scraper = BinanceAnnouncementScrape()
    last_announcement = scraper.get_announcement()
    listing_time = None
    symbol = None
    save_folder = "../../trades"
    coin_name = None

    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    while True:
        scraper.refresh()
        current_announcement = scraper.get_announcement()
        announcement_is_new = current_announcement != last_announcement
        if announcement_is_new:
            coins = scraper.get_coin_names()
            if coins:
                coin_name = coins[0]
                time_str = scraper.get_listing_date()
                listing_time = calendar.timegm(dateparser.parse(time_str).timetuple())
        if listing_time is not None and time.time() + 60 >= listing_time:
            symbol = coin_name+"USDT"
            bot = subprocess.Popen(
                shlex.split(f"python3 log_listing.py {symbol} {save_folder} {ENV_PATH}"),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            listing_time = None
            coin_name = None
        last_announcement = current_announcement
        time.sleep(60)
