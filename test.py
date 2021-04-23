from news_scraper import NewsScraper
import config
from time import perf_counter
from textblob import TextBlob

DRIVER = 'C:/Users/jason/chromedriver/chromedriver.exe'
SEARCH_TERM = 'georgia voting law'
NUM_ARTICLES = 10

start = perf_counter()
scraper = NewsScraper(DRIVER)
scrape_data = {}
for item in config.SITE_SCRAPE_CONFIG:
    scrape_data[item] = scraper.scrape(item, SEARCH_TERM, NUM_ARTICLES)
for key in scrape_data:
    print(key)
    print(len(scrape_data[key]))
end = perf_counter()
print(f'Ran in {end - start:0.4f} seconds')
