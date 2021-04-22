import os, sys
import time
ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
sys.path.append(ROOT)
from luna_scripts.listing_mail import send_mail
from luna_modules.binance.BinanceAnnouncementScrape import BinanceAnnouncementScrape
import sqlite3

if __name__ == '__main__':
    THIS_FOLDER = os.path.dirname(__file__)
    DATABASE_PATH = os.path.join(THIS_FOLDER, "mailing_list.db")
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
                message += f"\n{scraper.get_announcement_link()}"
                db = sqlite3.connect(DATABASE_PATH)
                cursor = db.cursor()
                cursor.execute('''SELECT email FROM emails WHERE valid = 1''')
                rows = cursor.fetchall()
                for row in rows:
                    email = row[0]
                    try:
                        send_mail.send(email, message)
                    except Exception as e:
                        cursor.execute('''UPDATE emails SET valid = ? WHERE email = ?''', [0, email])
                        db.commit()
                cursor.close()
                db.close()
        time.sleep(60)
        last_announcement = current_announcement
