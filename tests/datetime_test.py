import requests
import dateparser
import json
import re
import time
import calendar


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
    raw_time = "2021-28-3 11:46:31 UTC"
    parsed_time = dateparser.parse(raw_time)
    epoch_time = calendar.timegm(parsed_time.timetuple())
    while True:
        current_time = time.time()
        print(current_time, epoch_time)
        if current_time >= epoch_time:
            print(time.localtime())
            break
        time.sleep(1)
