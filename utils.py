from news_scraper import NewsScraper
from spiders.news_spider import NewsSpider
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import SITE_SPIDER_CONFIG
from time import perf_counter, sleep
import csv

DRIVER = 'C:/Users/jason/chromedriver/chromedriver.exe'  # Path to ChromeDriver
SEARCH_TERM = 'georgia voting law'  # Term to be searched - **NEED TO MAKE USER INPUT**
NUM_ARTICLES = 10  # Number of articles to be scraped
MAX_PROCESS_WORKERS = 2  # Number of cores for processing - **NEED TO FIND PACKAGE TO GENERATE BASED ON CLIENT MACHINE**
MAX_THREAD_WORKERS = 4
DEFAULT_CSV_PATH = './data/news_scraper_data.csv'


def run_scraper(site):
    """Function wrapper used for multi-threading scrapers."""
    scraper = NewsScraper(DRIVER)
    articles = scraper.scrape(site, SEARCH_TERM, NUM_ARTICLES)
    scraper.driver.quit()
    return articles


def scraper_output_to_csv(article_dict, filepath=DEFAULT_CSV_PATH):
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


def spider_retrieve_articles(search_term, site):
    ns = NewsSpider(site)
    articles = ns.retrieve_article_links(search_term)
    return articles


def multithread_spider_article_links(search_term):
    links_dict = {}
    with ThreadPoolExecutor(max_workers=MAX_THREAD_WORKERS) as executor:
        futures = {executor.submit(spider_retrieve_articles, search_term, site): site for site in SITE_SPIDER_CONFIG}
        for f in as_completed(futures):
            links_dict[futures[f]] = f.result()

    return links_dict


def spider_retrieve_article_content(args):
    site, index, article_link = args
    print(site + ': scraping article ' + str(index + 1))
    ns = NewsSpider(site)
    res = ns.scrape_article_content(article_link)
    sleep(0.25)
    return res


def multithread_spider_article_content(links_dict):
    # to minimize the risk of being banned, we create a list ordered by index then site - this way, we don't make
    # several requests to the same domain in very short (<1s) time intervals
    thread_list = []
    for i in range(10):
        for site, link_list in links_dict.items():
            if len(link_list) >= i + 1:
                thread_list.append((site, i, link_list[i]))

    with ThreadPoolExecutor(max_workers=MAX_THREAD_WORKERS) as executor:
        for row, article in zip(thread_list, executor.map(spider_retrieve_article_content, thread_list)):
            links_dict[row[0]][row[1]] = article

    return links_dict


if __name__ == '__main__':
    # # start timer to measure performance
    start = perf_counter()
    links = multithread_spider_article_links(SEARCH_TERM)
    scraper_output_to_csv(multithread_spider_article_content(links), './data/news_scraper_data.csv')
    end = perf_counter()
    print(f'Ran in {end - start:0.4f} seconds')
