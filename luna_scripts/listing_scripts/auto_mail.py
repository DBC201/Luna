import os
import time
import send_mail
import scrape_functions

if __name__ == '__main__':
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, "last-new-listing.txt")
    scrape_functions.write_to_file(my_file, scrape_functions.scrape_titles()[0]["title"])
    with open(os.path.join(THIS_FOLDER, "mailing_list.txt"), 'r') as file:
        emails = [email.strip() for email in file.readlines()]

    listing_time = None

    while True:
        current_listing = scrape_functions.scrape_titles()[0]
        announcement_is_new = current_listing["title"] != scrape_functions.read_last_listing(my_file)
        coin_name = scrape_functions.get_coin_name(current_listing["title"])
        if announcement_is_new and coin_name:
            time_str = scrape_functions.get_listing_time(current_listing["code"])
            message = "Subject: " + f"Binance will list {coin_name} on {time_str}\n"
            message += '\n' + current_listing["title"]
            message += "\nhttps://www.binance.com/en/support/announcement/c-48"
            for email in emails:
                send_mail.send(email, message)
            scrape_functions.write_to_file(my_file, current_listing["title"])
        time.sleep(60)
