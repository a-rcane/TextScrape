import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium_stealth import stealth
from market_info import MarketInfo


class BaseScraper:

    @staticmethod
    def get_webdriver():
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--enable-javascript")
        options.add_argument("--headless")
        driver = webdriver.Chrome(options)

        # Selenium Stealth settings
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

        return driver

    def scrape_site_for_specific_tag(self, url, tag, **kwargs):
        # kwargs are the tag and class for that tag
        driver = self.get_webdriver()
        driver.get(url)

        page_source = driver.execute_script('return document.documentElement.outerHTML')

        soup = BeautifulSoup(page_source, 'html.parser')

        # using specific class here
        if 'classname' in kwargs.keys():
            relevant_companies = soup.find_all(tag, {'class': f"{kwargs['classname']}"})
        else:
            relevant_companies = soup.find_all(tag)
        # print(relevant_companies)

        scrape_data = []

        for company in relevant_companies:
            scrape_data.append(company.text)

        return scrape_data

    def get_specifics(self, url, values_to_scrape):
        driver = self.get_webdriver()
        driver.get(url)

        page_source = driver.execute_script('return document.documentElement.outerHTML')

        soup = BeautifulSoup(page_source, 'html.parser')

        # using specific class here
        for k in values_to_scrape:
            relevant_values = soup.find_all(values_to_scrape[k], {'class': f"{k}"})
            print(relevant_values)


if __name__ == '__main__':
    start = time.time()
    scraper = BaseScraper()
    market_info = MarketInfo()
    urls = ['payment-processing--26/razorpay-market-share', 'other-accounting-and-finance-software--256/mangopay'
                                                            '-market-share']

    for specific_url in urls:
        company_name = re.search(r'\/(.*?)-', specific_url).group(1)
        market_share = scraper.scrape_site_for_specific_tag(f'https://www.datanyze.com/market-share/{specific_url}',
                                                            'h4', classname='ms-description')
        market_info.get_market_share(market_share, company_name)

    end = time.time()
    print(str(end - start) + " s")
