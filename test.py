from news_scraper import NewsScraper
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import SITE_SCRAPE_CONFIG
from time import perf_counter
import csv

DRIVER = 'C:/Users/jason/chromedriver/chromedriver.exe'  # Path to ChromeDriver
SEARCH_TERM = 'georgia voting law'  # Term to be searched - **NEED TO MAKE USER INPUT**
NUM_ARTICLES = 10  # Number of articles to be scraped
MAX_THREAD_WORKERS = 5  # Number of thread workers that minimizes execution time while minimizing timeouts


def run_scraper(site):
    """Function wrapper used for multi-threading scrapers."""
    scraper = NewsScraper(DRIVER)
    articles = scraper.scrape(site, SEARCH_TERM, NUM_ARTICLES)
    scraper.driver.quit()
    return articles


def scraper_output_to_csv(article_dict, filepath):
    """Output results of scraping to a CSV."""
    with open(filepath, mode='w') as f:
        writer = csv.DictWriter(f, delimiter='|', fieldnames=['site', 'article'])
        writer.writeheader()
        for key in article_dict:
            for article in article_dict[key]:
                print(key, article)
                try:
                    writer.writerow({'site': key, 'article': article})
                except:
                    continue


if __name__ == '__main__':
    # start timer to measure performance
    start = perf_counter()

    # initialize data structure that will contain results from threads
    scrape_data = {}

    # Begin generating threads - limit number of workers to avoid timeouts
    with ThreadPoolExecutor(max_workers=MAX_THREAD_WORKERS) as executor:
        futures_data = {executor.submit(run_scraper, site): site for site in SITE_SCRAPE_CONFIG}
        # As threads complete, save results and release the thread
        for key in as_completed(futures_data):
            scrape_data[futures_data[key]] = key.result()
            print('finished ' + futures_data[key])

    # If any sites could not be scraped, try one more time
    # Then log the number of articles that were scraped per site
    for key in SITE_SCRAPE_CONFIG:
        if len(scrape_data[key]) == 0:
            print('re-running ' + key)
            articles = run_scraper(key)
            scrape_data[key] = articles
        print(key, len(scrape_data[key]))

    # Output to CSV in case there is an issue with text analyzer - scraping can take over 10 minutes
    # scraper_output_to_csv(scrape_data, './data/news_scraper_data.csv')

    # Print time to complete
    end = perf_counter()
    print(f'Ran in {end - start:0.4f} seconds')
