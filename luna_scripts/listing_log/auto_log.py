import os, sys
import shlex, subprocess
import time
import dateparser
import calendar

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
from luna_modules.binance.BinanceAnnouncementScrape import BinanceAnnouncementScrape

if __name__ == '__main__':
    scraper = BinanceAnnouncementScrape()
    last_announcement = scraper.get_announcement()
    listing_time = None
    save_folder = os.path.join(ROOT, "trades")
    symbols = {}
    active_processes = []
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    listing_time = calendar.timegm(dateparser.parse("4 am UTC"))
    symbols = scraper.get_symbols()

    while True:
        scraper.refresh()
        current_announcement = scraper.get_announcement()
        announcement_is_new = current_announcement != last_announcement
        if announcement_is_new:
            temp_symbols = scraper.get_symbols()
            if temp_symbols:
                symbols.update(temp_symbols)
                time_str = scraper.get_listing_date()
                listing_time = calendar.timegm(dateparser.parse(time_str).timetuple())
        if listing_time is not None and time.time() + 60 >= listing_time:
            for symbol in symbols:
                for quote in symbols[symbol]:
                    bot = subprocess.Popen(
                        shlex.split(f"python3 log_listing.py {symbol + quote} {save_folder}"),
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    gate = subprocess.Popen(
                        shlex.split(f"python3 gateio_log.py {symbol + '_' + quote} {save_folder} -d 60"),
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    active_processes.append(bot)
                    active_processes.append(gate)
            listing_time = None
            symbols.clear()
        last_announcement = current_announcement
        time.sleep(60)
        for p in active_processes:
            stdout, stderr = p.communicate()
            if stdout:
                print(stdout)
            if stderr:
                print(stderr)
            del p
        active_processes.clear()
