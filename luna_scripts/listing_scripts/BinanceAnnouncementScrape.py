import requests
import re
import json


class BinanceAnnouncementScrape:
    def __init__(self, link="https://www.binance.com/en/support/announcement/c-48"):
        self.link = link
        self.__last_title = self.__scrape_titles()[0]
        self.__symbol_info = self.__get_symbol_info()

    def __scrape_titles(self):
        decoded_page = requests.get(self.link).content.decode()
        regex_str = r"<script id=\"__APP_DATA\" type=\"application\/json\">.*?<\/script>"
        raw_json = re.findall(regex_str, decoded_page)[0][
                   len("<script id=\"__APP_DATA\" type=\"application/json\">"):len("</script>") * -1]
        j = json.loads(raw_json)
        return j["routeProps"]['b723']["navDataResource"][0]['articles']

    def __get_symbol_info(self):
        html = requests.get('https://www.binance.com/en/support/announcement/' + self.__last_title["code"]).content.decode()
        regex_str = r"and will open trading for (\w+\/\w+,?\s?)+(and\s\w+\/\w+\s)?trading pairs at \d+-\d+-\d+ \d+:\d+:?\d* AM \(.*?\)"
        search_result = re.search(regex_str, html)
        if search_result:
            return search_result.group(0)
        else:
            return None

    def get_symbols(self):
        if self.__symbol_info is None:
            return None
        regex_str = r"(\w+\/\w+,?\s?)+(and\s\w+\/\w+\s)?"
        search_result = re.search(regex_str, self.__symbol_info)
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
        if self.__symbol_info is None:
            return None
        regex_str = r"\d+-\d+-\d+ \d+:\d+:?\d* AM \(.*?\)"
        search_result = re.search(regex_str, self.__symbol_info)
        if search_result:
            return search_result.group(0)
        else:
            return None

    def refresh(self):
        self.__last_title = self.__scrape_titles()[0]
        self.__symbol_info = self.__get_symbol_info()

    def get_announcement(self):
        return self.__last_title["title"]

    def get_coin_names(self):
        if "Binance Will List" in self.__last_title:
            names = re.findall(r"\(\w+\)", self.__last_title["title"])
            names = [n[1:-1] for n in names]
            return names
        else:
            return None
