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
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    gate = subprocess.Popen(
                        shlex.split(f"python3 gateio_log.py {symbol + '_' + quote} {save_folder}"),
                        shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    active_processes.append([symbol+quote, bot])
                    active_processes.append([symbol+'_'+quote, gate])
            listing_time = None
            symbols.clear()
        last_announcement = current_announcement
        time.sleep(60)
        for i in active_processes:
            name, p = i
            if p.poll() is None:
                stdout, stderr = p.communicate()
                if stdout:
                    print(name, "stdout:", stdout)

                if stderr:
                    print(name, "stderr:", stderr)
                del i
