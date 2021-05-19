from utils import multithread_spider_article_links, multithread_spider_article_content
from text_analysis import ArticleTextAnalyzer
from time import perf_counter


if __name__ == '__main__':
    # prompt user for search term
    search_term = input('Please enter word or phrase you wish to search for: ')

    # begin timer for performance measurement
    start = perf_counter()

    # get set of article links
    links = multithread_spider_article_links(search_term)

    # scrape links
    article_dict = multithread_spider_article_content(links)

    # create text analyzer
    ata = ArticleTextAnalyzer(article_dict, search_term)

    # classify articles
    cl = ata.classify_nonpartisan_articles()

    # return execution time
    end = perf_counter()
    print(f'Ran in {end - start:0.4f} seconds')

    # print classifications and generate output
    ata.plot_output(cl)
