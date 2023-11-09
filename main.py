import time
from base_scraper import BaseScraper
from market_info import MarketInfo

if __name__ == '__main__':
    start = time.time()

    market_info = MarketInfo()
    scraper = BaseScraper()

    scrape_value = {
        'pic-table': 'table',
        'overview-container': 'div',
        'person-row': 'tr',
        'scrollable-cards': 'app - scrollable - cards',
        'products-row': 'tr',
        'cards-wrapper': 'div',
    }

    base_url = 'https://www.datanyze.com/companies/razorpay/416311031'

    scraper.get_specifics(base_url, scrape_value)

