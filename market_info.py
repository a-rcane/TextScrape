class MarketInfo:
    @staticmethod
    def get_market_share(scrape_data, company):
        if scrape_data:
            share = scrape_data[-1]
            print(f"market-share for {company}: " + str(share))

            return share
        else:
            print("No data")

    @staticmethod
    def get_company_info(relevant_data, company):
        pass


if __name__ == '__main__':
    market_info = MarketInfo()
