import requests
import os
import time
import send_mail
import re
import json


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


def get_last_listing():
    return scrape_titles()[0]["title"]


def get_listing_time(code):
    html = requests.get('https://www.binance.com/en/support/announcement/'+code).content.decode()
    regex_str = r"Binance will list .*? in the Innovation Zone and will open trading for .*? trading pairs at (.*?)\(UTC\)"
    return re.search(regex_str, html).group(1).strip()


if __name__ == '__main__':
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, "last-new-listing.txt")
    write_to_file(my_file, get_last_listing())
    with open("./mailing_list.txt", 'r') as file:
        emails = [email.strip() for email in file.readlines()]

    while True:
        current_listing = get_last_listing()
        if current_listing != read_last_listing(my_file):
            message = "Subject: " + current_listing + '\n'
            message += "\nhttps://www.binance.com/en/support/announcement/c-48"
            for email in emails:
                send_mail.send(email, message)
            if "Innovation Zone" in current_listing:
                ticker = re.search(r"\(.*?\)", current_listing).group(0)[1:-1]
                t = get_listing_time(scrape_titles()[0]["code"])
                # Then run the script
            write_to_file(my_file, current_listing)
        time.sleep(60)
