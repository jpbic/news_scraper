from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.options import Options
from config import SITE_SCRAPE_CONFIG
from typing import List
import time
import csv


options = Options()
options.headless = True
options.add_argument('start-maximized')
options.add_argument('--enable-automation')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})


class NewsScraper:
    """
    Generic class for scraping news sites using Chrome and ChromeDriver.
    """
    PAGE_LOAD_TIMEOUT = 15

    def __init__(self, driver):
        self.driver = webdriver.Chrome(executable_path=driver,
                                       chrome_options=options)
        self.driver.set_page_load_timeout(self.PAGE_LOAD_TIMEOUT)

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

    @staticmethod
    def attempt_multiple(limit, exc_owner, exc_type, func, *func_args):
        """
        Attempts to perform a function up to a specified number of times, catching exception if all attempts fail
        and returning a user-specified default type

        :param limit: Maximum number of time to attempt function
        :type limit: int
        :param exc_owner: String that appears in error message if all attempts fail. Useful for logging source of
                          exception.
        :type exc_owner: str
        :param exc_type: Data type to return if exception raised. Accepts any Python or user-defined types.
        :param func: Function to attempt running.
        :type func: Callable
        :param func_args: Arguments to pass to func
        :return:
        """
        attempts = 1
        while attempts <= limit:
            try:
                return func(*func_args)
            except Exception as e:
                attempts += 1
                if attempts > limit:
                    print(func.__name__ if exc_owner is None else exc_owner, e)
                    return None if not exc_type else exc_type()

    def get_hrefs_from_elements(self, config) -> List[str]:
        """
        Attempts to retrieve href attribute from article link WebElements.

        :param config: Configuration data for site being scraped.
        :type config: dict
        :return: List of resolved href attributes.
        """
        page_links = self.attempt_multiple(3, config['full_name'] + ' get hrefs', list,
                                           WebDriverWait(self.driver, 5).until,
                                           ec.presence_of_all_elements_located((By.XPATH, config['articles_links_xpath']))
        )
        page_hrefs = []
        for link in page_links:
            try:
                page_hrefs.append(link.get_attribute('href'))
            except:
                continue
        return page_hrefs

    def close_popup(self, popup_close_button_xpath) -> None:
        """
        Closes popup at specified xpath.

        :param popup_close_button_xpath: Xpath of popup close button.
        :type popup_close_button_xpath: str
        :return: None
        """
        try:
            popup_button = WebDriverWait(self.driver, 3).until(
                ec.visibility_of_element_located((By.XPATH, popup_close_button_xpath))
            )
            popup_button.click()
        except:
            pass

    def get_page_links_new_page(self, config, search_term, num_articles) -> List[str]:
        """
        Retrieves links to articles for sites that load additional search results in a new URL.

        :param config: Configuration data for site being scraped.
        :type config: dict
        :param search_term: Word or phrased being searched.
        :type search_term: str
        :param num_articles: Number of articles to scrape.
        :type num_articles: int
        :return: List of resolved href attributes for article links.
        """
        page_links = self.get_hrefs_from_elements(config)
        page_index = config['initial_page_index'] + 1
        while len(page_links) < num_articles:
            prev_length = len(page_links)
            self.attempt_multiple(3, config['full_name'] + ' get page', None, self.driver.get,
                                  self.build_url(query_string=config['query_string'],
                                                 search_term=search_term,
                                                 search_term_concat=config['search_term_concat'],
                                                 page=page_index))
            if 'popup_close_button_xpath' in config:
                self.close_popup(config['popup_close_button_xpath'])
            page_links.extend(self.get_hrefs_from_elements(config))
            if prev_length == len(page_links):
                return page_links
            page_index += 1
        return page_links[:num_articles]

    def get_page_links_load_button(self, config, num_articles) -> List[str]:
        """
        Retrieves links to articles for sites that load additional search results when the user clicks a button.

        :param config: Configuration data for site being scraped.
        :type config: dict
        :param num_articles: Number of articles to scrape.
        :type num_articles: int
        :return: List of resolved href attributes for article links.
        """
        page_links = []
        while len(page_links) < num_articles:
            prev_length = len(page_links)
            self.driver.find_element_by_xpath('//body').send_keys(Keys.ESCAPE)
            self.driver.execute_script("window.scroll(0, 10)")
            button = self.attempt_multiple(3, config['full_name'] + ' get load button', None,
                                           WebDriverWait(self.driver, 3).until,
                                           ec.element_to_be_clickable((By.XPATH, config['load_button_xpath'])))
            if button:
                try:
                    button.click()
                except Exception as e:
                    print('could not click load more button for ' + config['full_name'])
                    print(e)
            page_links = self.attempt_multiple(3, config['full_name'] + ' get page links', list,
                                               WebDriverWait(self.driver, 1).until,
                                               ec.presence_of_all_elements_located((By.XPATH,
                                                                                    config['articles_links_xpath'])))
            if prev_length == len(page_links):
                break
        return list(map(lambda tag: tag.get_attribute('href'), page_links))[:num_articles]

    def get_page_links_infinite_scroll(self, config, num_articles) -> List[str]:
        """
        Retrieves links to articles for sites that load additional search results as the user scrolls.

        :param config: Configuration data for site being scraped.
        :type config: dict
        :param num_articles: Number of articles to scrape.
        :type num_articles: int
        :return: List of resolved href attributes for article links.
        """
        page_links = []
        while len(page_links) < num_articles:
            prev_length = len(page_links)
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
            page_links = self.attempt_multiple(3, config['full_name'] + ' get page links', list,
                                               WebDriverWait(self.driver, 1).until,
                                               ec.presence_of_all_elements_located((By.XPATH,
                                                                                    config['articles_links_xpath'])))
            if prev_length == len(page_links):
                break
        return list(map(lambda tag: tag.get_attribute('href'), page_links))[:num_articles]

    def scrape(self, site, search_term, num_articles) -> List[str]:
        """
        Returns the content of the specified number of articles as a list.

        :param site: Name of the website, as defined in config.py
        :type site: string
        :param search_term: Word or phrase that is being searched
        :type search_term: str
        :param num_articles: Number of articles that should be scraped
        :type num_articles: int
        :return: Tuple (List containing contents of articles, number of articles successfully parsed)
        """
        print('scraping ' + site)
        config = SITE_SCRAPE_CONFIG[site]
        links_list = self.scrape_article_links(config, search_term, num_articles)
        return self.scrape_article_content(links_list, config)

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
        self.attempt_multiple(3, config['full_name'] + ' get initial page', None, self.driver.get,
                              self.build_url(query_string=config['query_string'],
                                             search_term=search_term,
                                             search_term_concat=config['search_term_concat'],
                                             page=config['initial_page_index']))

        if 'popup_close_button_xpath' in config:
            self.close_popup(config['popup_close_button_xpath'])

        if config['search_pagination_type'] == 'new_page':
            page_links = self.get_page_links_new_page(config, search_term, num_articles)
        elif config['search_pagination_type'] == 'load_button':
            page_links = self.get_page_links_load_button(config, num_articles)
        elif config['search_pagination_type'] == 'infinite_scroll':
            page_links = self.get_page_links_infinite_scroll(config, num_articles)
        else:
            page_links = []

        return page_links

    def scrape_article_content(self, links_list, config) -> List[str]:
        """
        Scrapes each link for article content.

        :param links_list: List of links to be scraped
        :type links_list: list
        :param config: Config object for button/article xpaths
        :type config: dict
        :return: Tuple (List of the content of each article scraped, number of articles successfully scraped)
        """
        content_list = []
        for link in links_list:
            print('scraping ' + link)
            self.attempt_multiple(3, link, None, self.driver.get, link)
            if 'sub_button_xpath' in config:
                try:
                    WebDriverWait(self.driver, 1).until(
                        ec.presence_of_element_located((By.XPATH, config['sub_button_xpath'])))
                    print('subscription required for ' + link)
                    continue
                except:
                    pass

            text_tags = self.attempt_multiple(3, link + ' content', list, WebDriverWait(self.driver, 3).until,
                                              ec.presence_of_all_elements_located((By.XPATH,
                                                                                   config['articles_content_xpath'])))
            content = ''
            for tag in text_tags:
                try:
                    content += ' ' + tag.text
                except:
                    continue
            content_list.append(content)
            print('finished scraping ' + link)
        return content_list
