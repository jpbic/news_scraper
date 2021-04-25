from news_scraper import NewsScraper
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import SITE_SCRAPE_CONFIG
from time import perf_counter
from textblob import TextBlob

DRIVER = 'C:/Users/jason/chromedriver/chromedriver.exe'
SEARCH_TERM = 'georgia voting law'
NUM_ARTICLES = 10
MAX_THREAD_WORKERS = 5


def run_scraper(site):
    scraper = NewsScraper(DRIVER)
    articles = scraper.scrape(site, SEARCH_TERM, NUM_ARTICLES)
    scraper.driver.quit()
    return articles


if __name__ == '__main__':
    start = perf_counter()
    scrape_data = {}
    with ThreadPoolExecutor(max_workers=MAX_THREAD_WORKERS) as executor:
        futures_data = {executor.submit(run_scraper, site): site for site in SITE_SCRAPE_CONFIG}
        for key in as_completed(futures_data):
            scrape_data[futures_data[key]] = key.result()
            print('finished ' + futures_data[key])

    for key in SITE_SCRAPE_CONFIG:
        print(key)
        print(len(scrape_data[key]))
    end = perf_counter()
    print(f'Ran in {end - start:0.4f} seconds')
