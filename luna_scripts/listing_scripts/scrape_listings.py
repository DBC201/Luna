import requests
import os
import time
import send_mail
import re
import json
import dateparser


def write_to_file(file_name, content):
    f = open(file_name, "w")
    f.write(content)
    f.close()


def read_last_listing(file_name):
    with open(file_name, 'r') as f:
        return f.read()


def scrape_titles():
    decoded_page = requests.get('https://www.binance.com/en/support/announcement/c-48').content.decode()
    regex_str = r"<script id=\"__APP_DATA\" type=\"application\/json\">.*?<\/script>"
    raw_json = re.findall(regex_str, decoded_page)[0][
               len("<script id=\"__APP_DATA\" type=\"application/json\">"):len("</script>")*-1]
    j = json.loads(raw_json)
    return j["routeProps"]['b723']["navDataResource"][0]['articles']


def get_listing_time(code):
    html = requests.get('https://www.binance.com/en/support/announcement/'+code).content.decode()
    regex_str = r"Binance will list .*? in the Innovation Zone and will open trading for .*? trading pairs at (.*?) \((.*?)\)"
    return ' '.join(re.search(regex_str, html).groups())


if __name__ == '__main__':
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, "last-new-listing.txt")
    write_to_file(my_file, scrape_titles()[0]["title"])
    with open("./mailing_list.txt", 'r') as file:
        emails = [email.strip() for email in file.readlines()]

    listing_time = None

    while True:
        current_listing = scrape_titles()[0]
        if current_listing["title"] != read_last_listing(my_file):
            message = "Subject: " + current_listing + '\n'
            message += "\nhttps://www.binance.com/en/support/announcement/c-48"
            for email in emails:
                send_mail.send(email, message)
            if "Innovation Zone" in current_listing["title"]:
                ticker = re.search(r"\(.*?\)", current_listing).group(0)[1:-1]
                listing_time = time.mktime(dateparser.parse(get_listing_time(current_listing["code"])).timetuple())
            write_to_file(my_file, current_listing)
        if listing_time is not None and time.time() + 60 > listing_time:
            # run the program here
            pass
        time.sleep(60)
