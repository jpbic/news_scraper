from news_scraper import NewsScraper
from concurrent.futures import ProcessPoolExecutor
from config import SITE_SCRAPE_CONFIG
from time import perf_counter
import csv

DRIVER = 'C:/Users/jason/chromedriver/chromedriver.exe'  # Path to ChromeDriver
SEARCH_TERM = 'black lives matter'  # Term to be searched - **NEED TO MAKE USER INPUT**
NUM_ARTICLES = 10  # Number of articles to be scraped
MAX_PROCESS_WORKERS = 2  # Number of cores for processing - **NEED TO FIND PACKAGE TO GENERATE BASED ON CLIENT MACHINE**


def run_scraper(site):
    """Function wrapper used for multi-threading scrapers."""
    scraper = NewsScraper(DRIVER)
    articles = scraper.scrape(site, SEARCH_TERM, NUM_ARTICLES)
    scraper.driver.quit()
    return articles


def scraper_output_to_csv(article_dict, filepath):
    """Output results of scraping to a CSV."""
    print('writing scraping result to csv')
    with open(filepath, mode='w') as f:
        writer = csv.DictWriter(f, delimiter='|', fieldnames=['site', 'article'])
        writer.writeheader()
        for key in article_dict:
            article_dict[key] = list(filter(lambda a: len(a.replace(' ', '')) > 0, article_dict[key]))
            for article in article_dict[key]:
                try:
                    writer.writerow({'site': key, 'article': article})
                except:
                    continue


if __name__ == '__main__':
    # start timer to measure performance
    start = perf_counter()

    # initialize data structure that will contain results from threads
    scrape_data = {}

    # Generate threads - limit number of workers to avoid timeouts
    with ProcessPoolExecutor(max_workers=MAX_PROCESS_WORKERS) as executor:
        for site, article_list in zip(SITE_SCRAPE_CONFIG.keys(), executor.map(run_scraper, SITE_SCRAPE_CONFIG.keys())):
            scrape_data[site] = article_list
            print('finished ' + site)

    # If any sites could not be scraped, try one more time
    # Then log the number of articles that were scraped per site
    for key in SITE_SCRAPE_CONFIG:
        if len(scrape_data[key]) == 0:
            print('re-running ' + key)
            articles = run_scraper(key)
            scrape_data[key] = articles
        print(key, len(scrape_data[key]))

    # Output to CSV in case there is an issue with text analyzer - scraping can take over 10 minutes
    scraper_output_to_csv(scrape_data, './data/news_scraper_data.csv')

    # Print time to complete
    end = perf_counter()
    print(f'Ran in {end - start:0.4f} seconds')
