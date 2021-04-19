from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from config import SITE_SCRAPE_CONFIG
from typing import List


options = Options()
# options.headless = True
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})


class NewsScraper:
    """
    Generic class for scraping news sites.
    """
    def __init__(self, driver):
        self.driver = webdriver.Chrome(executable_path=driver,
                                       chrome_options=options)

    @staticmethod
    def build_url(query_string, search_term, search_term_concat, page) -> str:
        """
        Generates a URL for searches.

        :param query_string: Format string for search
        :type query_string: str
        :param search_term: Word or phrase that is being searched
        :type search_term: str
        :param search_term_concat: String used to concatenate multi-word search terms
        :type search_term_concat: str
        :param page: Page number of search results, if applicable
        :type page: int, str
        :return: URL for search
        """
        return query_string.format(query=search_term.replace(' ', search_term_concat), page=page)

    def scrape(self, site, search_term, num_articles) -> List[str]:
        """
        Returns the content of the specified number of articles as a list.

        :param site: Name of the website, as defined in config.py
        :type site: string
        :param search_term: Word or phrase that is being searched
        :type search_term: str
        :param num_articles: Number of articles that should be scraped
        :type num_articles: int
        :return: List containing contents of articles
        """
        config = SITE_SCRAPE_CONFIG[site]
        self.driver.get(self.build_url(query_string=config['query_string'],
                                       search_term=search_term,
                                       search_term_concat=config['search_term_concat'],
                                       page=config['initial_page_index']))
        links_list = self.scrape_article_links(config, search_term, num_articles)
        return self.scrape_article_content(links_list, config['articles_content_xpath'])

    def scrape_article_links(self, config, search_term, num_articles) -> List[str]:
        """
        Scrapes search page(s) for links for the number of articles specified.

        :param config: Search config for site - see config.py
        :type config: dict
        :param search_term: Word or phrase that is being searched
        :type search_term: str
        :param num_articles: Number of articles that should be scraped
        :type num_articles: int
        :return: List of the links of each article to be scraped
        """
        page_links = list(map(
            lambda tag: tag.get_attribute('href'),
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_all_elements_located((By.XPATH, config['articles_links_xpath']))
            )
        ))
        self.driver.find_element_by_xpath('//body').send_keys(Keys.ESCAPE)

        try:
            if config['search_pagination_type'] == 'new_page':
                page_index = config['initial_page_index'] + 1
                while len(page_links) < num_articles:
                    self.driver.get(self.build_url(query_string=config['query_string'],
                                                   search_term=search_term,
                                                   search_term_concat=config['search_term_concat'],
                                                   page=page_index))
                    page_links.extend(list(map(
                        lambda tag: tag.get_attribute('href'),
                        WebDriverWait(self.driver, 10).until(
                            ec.presence_of_all_elements_located((By.XPATH, config['articles_links_xpath']))
                        )
                    )))
                    page_index += 1
            elif config['search_pagination_type'] == 'load_button':
                while len(page_links) < num_articles:
                    WebDriverWait(self.driver, 10).until(
                        ec.element_to_be_clickable((By.XPATH, config['load_button_xpath']))
                    ).click()
                    page_links = WebDriverWait(self.driver, 10).until(
                        ec.presence_of_all_elements_located((By.XPATH, config['articles_links_xpath']))
                    )
                page_links = list(map(lambda tag: tag.get_attribute('href'), page_links))

        except Exception as e:
            print(e)
            return []

        return page_links[:num_articles]

    def scrape_article_content(self, links_list, article_content_xpath) -> List[str]:
        """
        Scrapes each link for article content.

        :param links_list: List of links to be scraped
        :type links_list: list
        :param article_content_xpath: XPATH of the content to be scraped
        :type article_content_xpath: str
        :return: List of the content of each article scraped
        """
        content_list = []
        for link in links_list:
            self.driver.get(link)
            try:
                text_tags = WebDriverWait(self.driver, 20).until(
                    ec.presence_of_all_elements_located((By.XPATH, article_content_xpath))
                )
                content_list.append(' '.join(p.text for p in text_tags))
                print(content_list[-1])

            except Exception as e:
                print(e)
                continue
        return content_list
