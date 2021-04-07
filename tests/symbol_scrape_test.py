from luna_scripts.listing_scripts.BinanceAnnouncementScrape import BinanceAnnouncementScrape

if __name__ == '__main__':
    scrape = BinanceAnnouncementScrape()
    print(scrape.get_announcement())
    print(scrape.get_coin_names())
    print(scrape.get_listing_date())
    print(scrape.get_symbols())
