import requests
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
               len("<script id=\"__APP_DATA\" type=\"application/json\">"):len("</script>") * -1]
    j = json.loads(raw_json)
    return j["routeProps"]['b723']["navDataResource"][0]['articles']


def get_listing_time(code): # maybe have it return trading pairs as well in the future
    html = requests.get('https://www.binance.com/en/support/announcement/' + code).content.decode()
    regex_str = r"Binance will list .*? and will open trading for .*? trading pairs at (\d+-\d+-\d+ \d+:\d+:?\d* AM \(.*?\))"
    search_result = re.search(regex_str, html)
    if search_result:
        return re.search(regex_str, html).group(1)
    else:
        return None


def get_coin_name(title):
    search_result = re.search(r"\wist (.*?) \((\w+)\)", title)
    if search_result:
        return search_result.group(2)
    else:
        return None
