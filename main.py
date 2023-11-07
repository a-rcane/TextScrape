from base_scraper import BaseScraper

if __name__ == '__main__':
    datanyze = ['https://www.datanyze.com/industries/software', 'div', 'trending-companies-cards-wrapper']
    scraper = BaseScraper()
    datanyze_data = scraper.scrape_site(datanyze[0], datanyze[1])

