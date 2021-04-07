import os
import time
import send_mail
from BinanceAnnouncementScrape import BinanceAnnouncementScrape

if __name__ == '__main__':
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(THIS_FOLDER, "mailing_list.txt"), 'r') as file:
        emails = [email.strip() for email in file.readlines()]

    scraper = BinanceAnnouncementScrape()

    last_announcement = scraper.get_announcement()

    while True:
        scraper.refresh()
        current_announcement = scraper.get_announcement()
        announcement_is_new = current_announcement != last_announcement
        if announcement_is_new:
            coins = scraper.get_coin_names()
            if coins:
                time_str = scraper.get_listing_date()
                message = "Subject: " + f"Binance will list {coins[0]} on {time_str}\n"
                message += '\n' + current_announcement
                message += "\nhttps://www.binance.com/en/support/announcement/c-48"
                for email in emails:
                    send_mail.send(email, message)
        time.sleep(60)
        last_announcement = current_announcement
