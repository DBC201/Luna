import os
import time
import dateparser
import calendar
import send_mail
import scrape_functions

if __name__ == '__main__':
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, "last-new-listing.txt")
    scrape_functions.write_to_file(my_file, scrape_functions.scrape_titles()[0]["title"])  # listing bot won't auto start if the listing has been alr made
    with open("./mailing_list.txt", 'r') as file:
        emails = [email.strip() for email in file.readlines()]

    listing_time = None

    while True:
        current_listing = scrape_functions.scrape_titles()[0]
        announcement_is_new = current_listing["title"] != scrape_functions.read_last_listing(my_file)
        if announcement_is_new:
            coin_name = scrape_functions.get_coin_name(current_listing["title"])
            if coin_name:
                message = "Subject: " + f"Binance will list {coin_name} on {time_str}\n"
                message += '\n' + current_listing["title"]
                message += "\nhttps://www.binance.com/en/support/announcement/c-48"
                for email in emails:
                    send_mail.send(email, message)
                ticker = scrape_functions.get_coin_name(current_listing)
                listing_time = calendar.timegm(dateparser.parse(scrape_functions.get_listing_time(current_listing["code"])).timetuple())
            scrape_functions.write_to_file(my_file, current_listing["title"])
        if listing_time is not None and time.time() + 60 >= listing_time:
            # run script here
            listing_time = None
        time.sleep(60)
