import os, sys
import time
import dateparser
import calendar
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
from luna_modules.binance.BinanceAnnouncementScrape import BinanceAnnouncementScrape
from luna_modules.binance.BinanceLog import BinanceLog

if __name__ == '__main__':
    scraper = BinanceAnnouncementScrape()
    last_announcement = ''
    listing_time = None
    save_folder = os.path.join(ROOT, "trades")
    symbols = {}
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
            full_symbols = [] # btc+usdt is a full symbol, symbols is a dict
            for symbol in symbols:
                for quote in symbols[symbol]:
                    full_symbols.append(symbol+quote)
            binanceLog = BinanceLog(full_symbols)
            binanceLog.log(60)
            binanceLog.dump(save_folder)
            listing_time = None
            symbols.clear()
        last_announcement = current_announcement
        time.sleep(60)
