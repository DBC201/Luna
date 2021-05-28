import os, sys
import time
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
from luna_modules.email.EmailWrapper import EmailWrapper
from luna_modules.binance.BinanceAnnouncementScrape import BinanceAnnouncementScrape
from dotenv import load_dotenv
load_dotenv(os.path.join(ROOT, ".env.local"))

if __name__ == '__main__':
    scraper = BinanceAnnouncementScrape()
    emailWrapper = EmailWrapper(
        port=int(os.environ["ssl_port"]),
        smtp_server=os.environ["smtp_server"],
        sender_email=os.environ["email"],
        password=os.environ["email_password"],
        signature_text="https://bogdanoff.pw"
    )

    last_announcement = scraper.get_announcement()

    while True:
        scraper.refresh()
        current_announcement = scraper.get_announcement()
        announcement_is_new = current_announcement != last_announcement
        if announcement_is_new:
            coins = scraper.get_symbols()
            if coins:
                time_str = scraper.get_listing_date()
                emailWrapper.database_send(
                    subject= f"{current_announcement} on {time_str}",
                    body=scraper.get_announcement_link()
                )
        time.sleep(60)
        last_announcement = current_announcement
