import os, sys
import time
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
from luna_scripts.listing_mail import send_mail
from luna_modules.binance.BinanceAnnouncementScrape import BinanceAnnouncementScrape

if __name__ == '__main__':
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    emails = []
    with open(os.path.join(THIS_FOLDER, "mailing_list.txt"), 'r') as file:
        for email in file.readlines():
            email = email.strip()
            if email:
                emails.append(email)
    scraper = BinanceAnnouncementScrape()

    last_announcement = scraper.get_announcement()

    while True:
        scraper.refresh()
        current_announcement = scraper.get_announcement()
        announcement_is_new = current_announcement != last_announcement
        if announcement_is_new:
            coins = scraper.get_symbols()
            if coins:
                time_str = scraper.get_listing_date()
                message = "Subject: " + f"{current_announcement} on {time_str}\n"
                message += "\nhttps://www.binance.com/en/support/announcement/c-48"
                for email in emails:
                    try:
                        send_mail.send(email, message)
                    except Exception as e:
                        print(e)
        time.sleep(60)
        last_announcement = current_announcement
