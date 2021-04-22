import requests
import re
import json


class BinanceAnnouncementScrape:
    def __init__(self, link="https://www.binance.com/en/support/announcement/c-48"):
        self.link = link
        self.__last_title = self.__scrape_titles()[0]
        self.__last_link = 'https://www.binance.com/en/support/announcement/' + self.__last_title["code"]
        self.__symbols_date = self.__get_symbols_date()

    def __scrape_titles(self):
        decoded_page = requests.get(self.link).content.decode()
        regex_str = r"<script id=\"__APP_DATA\" type=\"application\/json\">.*?<\/script>"
        raw_json = re.findall(regex_str, decoded_page)[0][
                   len("<script id=\"__APP_DATA\" type=\"application/json\">"):len("</script>") * -1]
        j = json.loads(raw_json)
        return j["routeProps"]['b723']["navDataResource"][0]['articles']

    def __get_symbols_date(self):
        html = requests.get(self.__last_link).content.decode()
        regex_str = r"open trading for (\w+\/\w+,?\s?)+(and\s\w+\/\w+\s)?trading pairs at \d+-\d+-\d+ \d+:\d+:?\d* \w\w \(.*?\)"
        search_result = re.search(regex_str, html)
        if search_result:
            return search_result.group(0)
        else:
            return None

    def get_symbols(self):
        if self.__symbols_date is None:
            return None
        regex_str = r"(\w+\/\w+,?\s?)+(and\s\w+\/\w+\s)?"
        search_result = re.search(regex_str, self.__symbols_date)
        if not search_result:
            return None
        symbols = {}
        regex_str = r"(\w+\/\w+)"
        found_symbols = re.findall(regex_str, search_result.group(0))
        for s in found_symbols:
            coin, to_pay = s.split('/')
            if coin in symbols:
                symbols[coin].append(to_pay)
            else:
                symbols.update({coin: [to_pay]})
        return symbols

    def get_listing_date(self):
        if self.__symbols_date is None:
            return None
        regex_str = r"\d+-\d+-\d+ \d+:\d+:?\d* \w\w \(.*?\)"
        search_result = re.search(regex_str, self.__symbols_date)
        if search_result:
            return search_result.group(0)
        else:
            return None

    def refresh(self, prev_index=0):
        self.__last_title = self.__scrape_titles()[prev_index]
        self.__last_link = 'https://www.binance.com/en/support/announcement/' + self.__last_title["code"]
        self.__symbols_date = self.__get_symbols_date()

    def get_announcement(self):
        return self.__last_title["title"]

    def get_announcement_link(self):
        return self.__last_link
