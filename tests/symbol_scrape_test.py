from luna_modules.binance.BinanceAnnouncementScrape import BinanceAnnouncementScrape

if __name__ == '__main__':
    scrape = BinanceAnnouncementScrape()
    print(scrape.get_announcement())
    print(scrape.get_listing_date())
    print(scrape.get_symbols())
