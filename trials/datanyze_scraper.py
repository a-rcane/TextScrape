import re
import time
from base_scraper import BaseScraper


class BuiltWithSiteScraper:
    def __int__(self):
        BaseScraper.__init__(self)

    @staticmethod
    def scrape_site(url):
        scraper = BaseScraper()
        scrape_data = scraper.scrape_site(url, 'div', 'trending-companies-cards-wrapper')

        return scrape_data


if __name__ == '__main__':
    start = time.time()
    # print('Software')
    # scrape_site('https://www.datanyze.com/industries/software')
    # print('\n')
    # print('Education')
    # res = re.sub(r'(\d)([AC-LN-Z])|(\d) (M)|(\d) (B)', r'\1\n\2', company.text, flags=re.MULTILINE)

    base_url = 'https://www.datanyze.com/industries/education'
    new_scraper = BuiltWithSiteScraper.scrape_site(base_url)

    # scrape_site('https://www.datanyze.com/industries/education')
    end = time.time()
    print(str(end - start) + "s")
