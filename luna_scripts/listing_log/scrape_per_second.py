import os
import sys
import shlex
import subprocess
import time

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
from luna_modules.binance.BinanceAnnouncementScrape import BinanceAnnouncementScrape
from dotenv import load_dotenv
load_dotenv(os.path.join(ROOT, ".env.local"))

if __name__ == '__main__':
    scraper = BinanceAnnouncementScrape()

    last_announcement = scraper.get_announcement()

    active_processes = []

    save_folder = os.path.join(ROOT, "trades")
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    while True:
        scraper.refresh()
        current_announcement = scraper.get_announcement()
        announcement_is_new = current_announcement != last_announcement
        if announcement_is_new:
            coins = scraper.get_symbols()
            if coins:
                time_str = scraper.get_listing_date()
                for symbol in coins:
                    for quote in coins[symbol]:
                        gate = subprocess.Popen(
                            shlex.split(f"python3 gateio_log.py {symbol + '_' + quote} {save_folder}"),
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
                        active_processes.append(gate)
                listing_time = None
                coins.clear()
        last_announcement = current_announcement
        time.sleep(1)
        for p in active_processes:
            if p.poll() is None:
                del p
