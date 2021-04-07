from luna_scripts.listing_scripts import BinanceAnnouncementScrape

if __name__ == '__main__':
    time_str = BinanceAnnouncementScrape.get_listing_time("1bd8869e95ec4bf9b01b6b31361d7f84")
    print(time_str)