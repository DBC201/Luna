import os
import time
import send_mail
import scrape_functions

if __name__ == '__main__':
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(THIS_FOLDER, "mailing_list.txt"), 'r') as file:
        emails = [email.strip() for email in file.readlines()]

    last_listing = scrape_functions.scrape_titles()[0]

    while True:
        current_listing = scrape_functions.scrape_titles()[0]
        announcement_is_new = current_listing["title"] != last_listing["title"]
        if announcement_is_new:
            coin_name = scrape_functions.get_coin_name(current_listing["title"])
            if coin_name:
                time_str = scrape_functions.get_listing_time(current_listing["code"])
                message = "Subject: " + f"Binance will list {coin_name} on {time_str}\n"
                message += '\n' + current_listing["title"]
                message += "\nhttps://www.binance.com/en/support/announcement/c-48"
                for email in emails:
                    send_mail.send(email, message)
        time.sleep(60)
        last_listing = current_listing
