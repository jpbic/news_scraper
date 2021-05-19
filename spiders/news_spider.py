import requests
from bs4 import BeautifulSoup
from lxml import etree
from googleapiclient.discovery import build
from copy import deepcopy
from string import Formatter
from config import SITE_SPIDER_CONFIG
from api_keys import API_KEY_CONFIG


class NewsSpider:
    """
    Class wrapper for scraping articles from news sites based on a search term.
    """
    TARGET_RESULT_LENGTH = 10
    CHAR_REPLACE = [('“', '"'), ('”', '"'), ('‘', '"'), ('’', '"'), ('[', ''), (']', ''), (u'\xa0', ' '), (r'\'', '\'')]

    def __init__(self, site=None):
        self.site = site
        self.config = None if not site else SITE_SPIDER_CONFIG[site]

    def set_site(self, site):
        self.site = site
        self.config = None if not site else SITE_SPIDER_CONFIG[site]

    @staticmethod
    def format_payload_params(config, search_term, page):
        """
        Formats query and form parameters with search term and page data based on site configuration in config.py

        :param config: configuration object with URL, payload, and query parameter information
        :type config: Any
        :param search_term: word or phrased being searched
        :type search_term: str
        :param page: page number to be sent in query/form parameters
        :type page: int
        :return: config object formatted with search term and page information
        """
        f_dict = deepcopy(config)

        for k, v in f_dict.items():
            if isinstance(v, dict):
                f_dict[k] = NewsSpider.format_payload_params(f_dict[k], search_term, page)
            elif isinstance(v, list):
                f_dict[k] = [NewsSpider.format_payload_params(i, search_term, page)
                             for i in v]
            elif v == '':
                pass
            elif next(Formatter().parse(v))[1]:
                f_dict[k] = v.format(query=search_term, page=page)

        return f_dict

    @staticmethod
    def fill_article_link_list(initial_page_index, al_func, **func_kwargs):
        """
        Repeats appropriate query function for retrieving article links until target number of articles are found

        :param initial_page_index: index of first page of results
        :type initial_page_index: int
        :param al_func: query function for searching
        :type al_func: function
        :param func_kwargs: keyword arguments to pass to query function
        :return: list of article links of target number length
        """
        result = []
        prev_results = -1
        while prev_results < len(result) < NewsSpider.TARGET_RESULT_LENGTH:
            initial_page_index += 1
            prev_results = len(result)
            result.extend(al_func(**dict(func_kwargs, page=initial_page_index)))
        return result[:NewsSpider.TARGET_RESULT_LENGTH]

    @staticmethod
    def ajax_search(al_config, search_term, page):
        """
        Query function to retrieve article links for sites requiring ajax calls

        :param al_config: article links config for site from config.py
        :type al_config: dict
        :param search_term: word or phrased being searched for
        :type search_term: str
        :param page: page number to include in ajax calls
        :type page: int
        :return: list of article links
        """
        # if an ajax request is required, there will be an associated set of params and payload that needs to be
        # formatted with search term and page
        params = NewsSpider.format_payload_params(al_config['params'], search_term, page)
        payload = NewsSpider.format_payload_params(al_config['payload'], search_term, page)
        search_params = {'url': al_config['request_url'].format(query=search_term, page=page),
                         'params': params}
        with requests.Session() as req:
            if al_config['payload']:
                res = req.post(**search_params, json=payload).json()
            else:
                res = req.get(**search_params).json()

        # the result will be a JSON object with nested keys - use config to find links/slugs
        for ind in al_config['results_level']:
            res = res[ind]

        # remove any hrefs for non-text articles (videos, radio shows, etc)
        for excl in al_config['link_exclusions']:
            res = list(filter(lambda result: result[al_config['url_key']].find(excl) == -1, res))

        # if request yields slugs, base_url will have the domain. otherwise it'll be empty
        return [al_config['base_url'] + result[al_config['url_key']] for result in res]

    @staticmethod
    def google_search(search_term, cse_id, link_exclusions, service, page, site):
        """
        Query function to retrieve article links for sites implementing Google's custom search API

        :param search_term: word or phrase being searched for
        :type search_term: str
        :param cse_id: search engine ID for Google CSE API for site
        :type cse_id: str
        :param link_exclusions: list of terms which, if found in URL, should be excluded from results
        :type link_exclusions: list
        :param service: googleapiclient service
        :type service: googleapiclient.discovery.Resource
        :param page: page of search results
        :type page: int
        :param site: site being searched by service
        :type site: str
        :return: list of article links
        """
        # use Google CSE to get search items
        res = [item['link'] for item in
               service.cse().list(q=search_term, cx=cse_id, start=(page*10 + 1)).execute()['items']]

        # remove any hrefs for non-text articles (videos, radio shows, etc)
        for excl in link_exclusions:
            res = list(filter(lambda link: link.find(excl) == -1, res))

        # sometimes google CSE will return the base URL - in this case, exlude from result
        res = list(filter(lambda link: link != 'https://www.' + site + '.com/', res))

        return res

    @staticmethod
    def static_search(al_config, search_term, page):
        """
        Query function to retrieve article links for sites with search results on different URLs

        :param al_config: article links config for site from config.py
        :type al_config: dict
        :param search_term: word or phrased being searched for
        :type search_term: str
        :param page: page number to include in ajax calls
        :type page: int
        :return: list of article links
        """
        # bs4 parses the HTML response
        soup = BeautifulSoup(requests.get(
            url=al_config['request_url'].format(query=search_term, page=page)
        ).content, 'html.parser')

        # lxml allows us to search for links by xpath
        dom = etree.HTML(str(soup))
        res = [al_config['base_url'] + el.get('href') for el in dom.xpath(al_config['articles_links_xpath'])]

        # remove any hrefs for non-text articles (videos, radio shows, etc)
        for excl in al_config['link_exclusions']:
            res = list(filter(lambda link: link.find(excl) == -1, res))

        return res[:NewsSpider.TARGET_RESULT_LENGTH]

    @staticmethod
    def replace_chars(text):
        """
        Function for replacing characters that make text analysis difficult/less reliable

        :param text: text to be cleaned
        :type text: str
        :return: cleaned text
        """
        for pair in NewsSpider.CHAR_REPLACE:
            if pair[0] in text:
                text = text.replace(pair[0], pair[1])
        return text

    def retrieve_article_links(self, search_term, api_key=None, cse_id=None):
        """
        Function wrapper for executing the proper query function based on instance configuration

        :param search_term: word or phrase being searched for
        :type search_term: str
        :param api_key: Google developer API key
        :type api_key: str
        :param cse_id: search engine ID for Google CSE for site
        :type api_key: str
        :return: list of article links
        """
        # config for retrieving article links
        al_config = self.config['article_links']

        print('Retrieving article links for ' + self.config['full_name'])
        if al_config['request_type'] == 'ajax':
            return self.fill_article_link_list(
                initial_page_index=al_config['initial_page_index'],
                al_func=self.ajax_search,
                al_config=al_config,
                search_term=search_term
            )
        # if a google custom search is required, call the Google CSE API
        elif al_config['request_type'] == 'google':
            return self.fill_article_link_list(
                initial_page_index=-1,
                al_func=self.google_search,
                search_term=search_term,
                cse_id=cse_id if cse_id else API_KEY_CONFIG['search_keys'][self.site],
                link_exclusions=al_config['link_exclusions'],
                service=build('customsearch', 'v1', developerKey=api_key if api_key else API_KEY_CONFIG['dev_api_key']),
                site=self.site
            )
        # otherwise, retrieve the html and use xpath to get links
        else:
            return self.fill_article_link_list(
                initial_page_index=al_config['initial_page_index'],
                al_func=self.static_search,
                al_config=al_config,
                search_term=search_term
            )

    def scrape_article_content(self, link):
        """
        Function for scraping article content based on xpath

        :param link: link to article
        :type link: str
        :return: article text
        """
        ac_config = self.config['article_content']
        content = ''

        with requests.Session() as req:
            soup = BeautifulSoup(req.get(url=link).content, 'lxml')

        dom = etree.HTML(str(soup))
        for t in dom.xpath(ac_config['article_content_xpath']):
            try:
                content += ' ' + self.replace_chars(t.strip())
            except Exception as e:
                print(e)
                continue

        return content.strip()
