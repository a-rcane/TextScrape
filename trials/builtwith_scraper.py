import re
import time
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from selenium import webdriver


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


def scrape_site(url):
    driver = get_webdriver()
    driver.get(url)

    page_source = driver.execute_script('return document.documentElement.outerHTML')

    soup = BeautifulSoup(page_source, 'html.parser')
    # print(soup)

    # using specific class here
    relevant_companies = soup.find_all(
        'td',
        # {'class': 'pl-0 text-primary'}
        )

    # print(relevant_companies)
    res = []

    for company in relevant_companies:
        r = re.sub(r'(\n\s*)+', ' ', company.text)
        res.append(r)

    return res


if __name__ == '__main__':
    company_list = ['Razorpay', 'MangoPay']
    base_url = 'https://trends.builtwith.com/websitelist/'
    start = time.time()

    # for name in company_list:
    #     print(name)
    #     print(scrape_site(base_url + name))

    print(scrape_site('https://www.appsruntheworld.com/Apps-top-500-applications-vendors/'))

    end = time.time()
    print(str(end - start) + " seconds")
