SITE_SCRAPE_CONFIG = {
    'daily_wire': {
        'full_name': 'Daily Wire',
        'search_pagination_type': 'new_page',
        'query_string': r'https://www.dailywire.com/search/news?query={query}&page={page}',
        'initial_page_index': 1,
        'search_term_concat': r'%20',
        'articles_links_xpath': r'//article/a',
        'articles_content_xpath': r'//div[@id="post-body-text"]//p',
        'sub_button_xpath': r'//button[@data-testid="continue-reading-button-reader"]'
    },
    'blaze': {
        'full_name': 'The Blaze',
        'search_pagination_type': 'load_button',
        'query_string': r'https://www.theblaze.com/search/?q={query}',
        'initial_page_index': '',
        'search_term_concat': r'+',
        'load_button_xpath': r'//div[@load-type="button"]',
        'articles_links_xpath': r'//article//div[@class="widget__head"]/a',
        'articles_content_xpath': r'//div[@class="body-description"]//p'
    },
    'breitbart': {
        'full_name': 'Breitbart',
        'search_pagination_type': 'new_page',
        'query_string': r'https://www.breitbart.com/search/?s={query}#gsc.tab=0&gsc.q={query}&gsc.page={page}',
        'initial_page_index': 1,
        'search_term_concat': r'%20',
        'articles_links_xpath': r'//article//div[@class="gsc-thumbnail-inside"]//a[contains(@class, "gs-title") and not(contains(@href, "/tag/"))]',
        'articles_content_xpath': r'//div[@class="entry-content"]/p',
        'popup_close_button_xpath': r'//span[@id="ISCTO_close"]'
    },
    'slate': {
        'full_name': 'Slate',
        'search_pagination_type': 'new_page',
        'query_string': r'https://slate.com/search?q={query}#gsc.tab=0&gsc.q={query}&gsc.sort=&gsc.page={page}',
        'initial_page_index': 1,
        'search_term_concat': r'%20',
        'articles_links_xpath': r'//section//div[@class="gsc-thumbnail-inside"]//a[contains(@class, "gs-title")]',
        'articles_content_xpath': r'//div[@class="article__content"]//p[contains(@class, "slate-paragraph")]'
    },
    'bipartisan_report': {
        'full_name': 'Bipartisan Report',
        'search_pagination_type': 'new_page',
        'query_string': r'https://bipartisanreport.com/page/{page}/?s={query}',
        'initial_page_index': 1,
        'search_term_concat': r'+',
        'articles_links_xpath': r'//div[contains(@class, "td_module_wrap")]//a[@class="td-image-wrap"]',
        'articles_content_xpath': r'//div[@class="td-post-content"]//p[not(.//iframe) and not(.//script)]',
        'popup_close_button_path': r'//img[id="mCaddyClose"]'
    },
    'tpm': {
        'full_name': 'Talking Points Memo',
        'search_pagination_type': 'new_page',
        'query_string': r'https://talkingpointsmemo.com/search/{query}/page/{page}',
        'initial_page_index': 1,
        'search_term_concat': r'+',
        'articles_links_xpath': r'//a[@class="Archive__PostImage"]',
        'articles_content_xpath': r'//div[@id="article-content"]//p',
        'sub_button_xpath': r'//div[@class="PrimePaywall__Button"]'
    },
    'cnbc': {
        'full_name': 'CNBC',
        'search_pagination_type': 'infinite_scroll',
        'query_string': r'https://www.cnbc.com/search/?query={query}&qsearchterm={query}',
        'initial_page_index': '',
        'search_term_concat': r'%20',
        'articles_links_xpath': r'//div[@class="SearchResult-searchResultImage"]/..',
        'articles_content_xpath': r'//div[@class="ArticleBody-articleBody"]//div[@class="group"]//p'
    },
    'fox_news': {
        'full_name': 'Fox News',
        'search_pagination_type': 'load_button',
        'query_string': r'https://www.foxnews.com/search-results/search?q={query}',
        'initial_page_index': '',
        'search_term_concat': r'%20',
        'load_button_xpath': r'//div[contains(@class, "button load-more")]',
        'articles_links_xpath': r'//article//h2[@class="title"]/a[not(contains(@href, "/video."))]',
        'articles_content_xpath': r'//div[@class="article-body"]//p'
    },
    'msnbc': {
        'full_name': 'MSNBC',
        'search_pagination_type': 'new_page',
        'query_string': r'https://www.msnbc.com/search/?q={query}#gsc.tab=0&gsc.q={query}&gsc.page={page}',
        'initial_page_index': 1,
        'search_term_concat': r'%20',
        'articles_links_xpath': (
            r'//div[@class="gsc-wrapper"]//div[@class="gsc-thumbnail-inside"]//a[contains(@class, "gs-title") '
            r'and not(contains(@href, "/watch/"))]'
        ),
        'articles_content_xpath': r'//div[@class="article-body__content"]/p'
    },
    'cnn': {
        'full_name': 'CNN',
        'search_pagination_type': 'new_page',
        'query_string': r'https://www.cnn.com/search?q={query}&size=10&from=10&page={page}&sort=relevance',
        'initial_page_index': 1,
        'search_term_concat': r'%20',
        'articles_links_xpath': r'//div[@class="cnn-search__result-contents"]//a',
        'articles_content_xpath': r'//div[@class="l-container"]//*[contains(@class, "zn-body__paragraph")]'
    },
    'abc': {
        'full_name': 'ABC News',
        'search_pagination_type': 'new_page',
        'query_string': r'https://abcnews.go.com/search?searchtext={query}&type=Story&page={page}',
        'initial_page_index': 1,
        'search_term_concat': r'%20',
        'articles_links_xpath': r'//div[@class="ContentRoll__Headline"]//a[not(contains(@href, "/video/"))]',
        'articles_content_xpath': r'//section[contains(@class, "Article__Content")]/p'
    },
    'ny_post': {
        'full_name': 'New York Post',
        'search_pagination_type': 'new_page',
        'query_string': r'https://nypost.com/search/{query}/page/{page}/?orderby=relevance',
        'initial_page_index': 1,
        'search_term_concat': r'+',
        'articles_links_xpath': r'//h3[@class="entry-heading"]/a',
        'articles_content_xpath': r'//div[contains(@class, "entry-content")]/p'
    },
    'cbs': {
        'full_name': 'CBS News',
        'search_pagination_type': 'load_button',
        'query_string': r'https://www.cbsnews.com/search/?q={query}',
        'initial_page_index': '',
        'search_term_concat': r'+',
        'load_button_xpath': r'//a[contains(@class, "component__view-more")]',
        'articles_links_xpath': r'//article[contains(@class, "item--type-article")]/a[not(contains(@href, "/video/"))]',
        'articles_content_xpath': r'//section[@class="content__body"]/p'
    },
    'npr': {
        'full_name': 'NPR',
        'search_pagination_type': 'load_button',
        'query_string': r'https://www.npr.org/search?query={query}',
        'initial_page_index': '',
        'search_term_concat': r'%20',
        'load_button_xpath': r'//button[@class="ais-InfiniteHits-loadMore"]',
        'articles_links_xpath': r'//h2[@class="title"]/a[not(contains(@href, ".org"))]',
        'articles_content_xpath': r'//div[@id="storytext"]/p'
    },
    'politico': {
        'full_name': 'Politico',
        'search_pagination_type': 'new_page',
        'query_string': r'https://www.politico.com/search/{page}?q={query}',
        'initial_page_index': 1,
        'search_term_concat': r'%20',
        'articles_links_xpath': r'//div[@class="summary"]//a',
        'articles_content_xpath': r'//div[contains(@class, "story-text")]/p'
    },
    'axios': {
        'full_name': 'Axios',
        'search_pagination_type': 'new_page',
        'query_string': r'https://www.axios.com/results?q={query}&page={page}',
        'initial_page_index': 1,
        'search_term_concat': r'+',
        'articles_links_xpath': r'//figure[contains(@class, "flex-col")]/a',
        'articles_content_xpath': r'//div[contains(@class, "gtm-story-text")]/p'
    },
    'usa_today': {
        'full_name': 'USA Today',
        'search_pagination_type': 'new_page',
        'query_string': r'https://www.usatoday.com/search/?q={query}&page={page}',
        'initial_page_index': 1,
        'search_term_concat': r'%20',
        'articles_links_xpath': r'//a[contains(@class, "gnt_se_a")]',
        'articles_content_xpath': r'//p[@class="gnt_ar_b_p"]'
    }
}

SITE_CATEGORIES = {
    'conservative': {'daily_wire', 'blaze', 'breitbart'},
    'liberal': {'slate', 'bipartisan_report', 'tpm'}
}

SITE_SPIDER_CONFIG = {
    'daily_wire': {
        'full_name': 'Daily Wire',
        'article_links': {
            'request_type': 'ajax',
            'request_url': 'https://coavros3ua-dsn.algolia.net/1/indexes/*/queries',
            'params': {
                'x-algolia-agent': 'Algolia%20for%20JavaScript%20(4.8.3)%3B%20Browser%20(lite)%3B%20react%20'
                                   '(17.0.1)%3B%20react-instantsearch%20(6.8.2)%3B%20JS%20Helper%20(3.3.4)',
                'x-algolia-api-key': 'a4f0c53db65420b2348b5bd1e0c39967',
                'x-algolia-application-id': 'COAVROS3UA'
            },
            'payload': {
                'requests': [{
                    'indexName': 'wp_prod_wp_posts_post',
                    'params': 'highlightPreTag=%3Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-'
                              '0000000000%3E&query={query}&page={page}&facets=%5B%5D&tagFilters='
                }]
            },
            'initial_page_index': -1,
            'results_level': ['results', 0, 'hits'],
            'url_key': 'slug',
            'base_url': 'https://www.dailywire.com/search/news/',
            'link_exclusions': []
        }
    },
    'blaze': {
        'full_name': 'The Blaze',
        'article_links': {
            'request_type': 'static',
            'request_url': 'https://www.theblaze.com/search/?q={query}',
            'articles_links_xpath': r'//article//div[@class="widget__head"]/a',
            'initial_page_index': 0,
            'base_url': '',
            'link_exclusions': []
        }
    },
    'breitbart': {
        'full_name': 'Breitbart',
        'article_links': {
            'request_type': 'google',
            'link_exclusions': [r'/tag/']
        }
    },
    'slate': {
        'full_name': 'Slate',
        'article_links': {
            'request_type': 'google',
            'link_exclusions': []
        }
    },
    'bipartisan_report': {
        'full_name': 'Bipartison Report',
        'article_links': {
            'request_type': 'static',
            'request_url': r'https://bipartisanreport.com/page/{page}/?s={query}',
            'articles_links_xpath': r'//div[contains(@class, "td_module_wrap")]//a[@class="td-image-wrap"]',
            'initial_page_index': 1,
            'base_url': '',
            'link_exclusions': []
        }
    },
    'tpm': {
        'full_name': 'Talking Points Memo',
        'article_links': {
            'request_type': 'static',
            'request_url': r'https://talkingpointsmemo.com/search/{query}/page/{page}',
            'articles_links_xpath': r'//a[@class="Archive__PostImage"]',
            'initial_page_index': 1,
            'base_url': '',
            'link_exclusions': []
        }
    },
    'cnbc': {
        'full_name': 'CNBC',
        'article_links': {
            'request_type': 'ajax',
            'request_url': 'https://api.queryly.com/cnbc/json.aspx',
            'params': {
                'queryly_key': '31a35d40a9a64ab3',
                'query': '{query}',
                'endIndex': '0',
                'batchsize': '20',
                'callback': '',
                'showfaceted': 'false',
                'timezoneoffset': '240',
                'facetedfields': 'formats',
                'facetedkey': 'formats%7C',
                'facetedvalue': '!Press%20Release%7C',
                'needtoptickers': '0',
                'additionalindexes': '4cd6f71fbf22424d,937d600b0d0d4e23,3bfbe40caee7443e,626fdfcd96444f28'
            },
            'payload': {
            },
            'initial_page_index': -1,
            'results_level': ['results'],
            'url_key': 'url',
            'base_url': '',
            'link_exclusions': []
        }
    },
    'fox_news': {
        'full_name': 'Fox News',
        'article_links': {
            'request_type': 'google',
            'link_exclusions': [r'/video.']
        }
    },
    'msnbc': {
        'full_name': 'MSNBC',
        'article_links': {
            'request_type': 'google',
            'link_exclusions': [r'/watch/']
        }
    },
    'cnn': {
        'full_name': 'CNN',
        'article_links': {
            'request_type': 'ajax',
            'request_url': r'https://search.api.cnn.io/content',
            'params': {
                'q': '{query}',
                'sort': 'relevance',
                'type': 'article',
                'size': '30'
            },
            'payload': {
            },
            'initial_page_index': -1,
            'results_level': ['result'],
            'url_key': 'url',
            'base_url': '',
            'link_exclusions': []
        }
    },
    'abc': {
        'full_name': 'ABC News',
        'article_links': {
            'request_type': 'ajax',
            'request_url': r'https://abcnews.go.com/meta/api/search',
            'params': {
                'q': '{query}',
                'sort': '',
                'type': 'Story',
                'section': '',
                'totalrecords': 'true',
                'offset': '0',
                'limit': '30'
            },
            'payload': {
            },
            'initial_page_index': -1,
            'results_level': ['item'],
            'url_key': 'link',
            'base_url': '',
            'link_exclusions': []
        }
    },
    'ny_post': {
        'full_name': 'New York Post',
        'article_links': {
            'request_type': 'static',
            'request_url': 'https://nypost.com/search/{query}/page/{page}/?orderby=relevance',
            'articles_links_xpath': r'//h3[@class="entry-heading"]/a',
            'initial_page_index': 1,
            'base_url': '',
            'link_exclusions': []
        }
    },
    'cbs': {
        'full_name': 'CBS News',
        'article_links': {
            'request_type': 'ajax',
            'request_url': r'https://api.queryly.com/json.aspx',
            'params': {
                'queryly_key': '4690eece66c6499f',
                'batchsize': '30',
                'query': '{query}',
                'groups': 'live:0_4_2',
                'showfaceted': 'true'
            },
            'payload': {
            },
            'initial_page_index': -1,
            'results_level': ['items'],
            'url_key': 'link',
            'base_url': '',
            'link_exclusions': []
        }
    },
    'npr': {
        'full_name': 'NPR',
        'article_links': {
            'request_type': 'ajax',
            'request_url': 'https://o2dg6462xl-dsn.algolia.net/1/indexes/*/queries',
            'params': {
                'x-algolia-agent': 'Algolia for JavaScript (3.35.1); Browser (lite); '
                                   'react (16.14.0); react-instantsearch (5.7.0); JS Helper (2.28.1)',
                'x-algolia-api-key': '40f2ee3bc56fa66dd5551ca1496ff941',
                'x-algolia-application-id': 'O2DG6462XL'
            },
            'payload': {
                'requests': [
                    {
                        'indexName': 'nprorg',
                        'params': 'query={query}&maxValuesPerFacet=10&page={page}&analytics=true&'
                                  'analyticsTags=%5B%22npr.org%2Fsearch%22%5D&highlightPreTag=%3'
                                  'Cais-highlight-0000000000%3E&highlightPostTag=%3C%2Fais-highlight-0000000000%3E&'
                                  'clickAnalytics=true&filters=&facets=%5B%22hasAudio%22%2C%22lastModifiedDate%22%2C%22'
                                  'shows%22%5D&tagFilters='
                    }
                ]
            },
            'initial_page_index': -1,
            'results_level': ['results', 0, 'hits'],
            'url_key': 'url',
            'link_exclusions': ['.org'],
            'base_url': 'https://www.npr.org'
        }
    },
    'politico': {
        'full_name': 'Politico',
        'article_links': {
            'request_type': 'static',
            'request_url': 'https://www.politico.com/search/{page}?q={query}',
            'articles_links_xpath': r'//div[@class="summary"]//a',
            'initial_page_index': 1,
            'base_url': '',
            'link_exclusions': []
        }
    },
    'axios': {
        'full_name': 'Axios',
        'article_links': {
            'request_type': 'static',
            'request_url': 'https://www.axios.com/results?q={query}&page={page}',
            'articles_links_xpath': r'//figure[contains(@class, "flex-col")]/a',
            'initial_page_index': 0,
            'base_url': '',
            'link_exclusions': []
        }
    },
    'usa_today': {
        'full_name': 'USA Today',
        'article_links': {
            'request_type': 'static',
            'request_url': 'https://www.usatoday.com/search/?q={query}&page={page}',
            'articles_links_xpath': r'//a[contains(@class, "gnt_se_a")]',
            'initial_page_index': 1,
            'base_url': 'https://www.usatoday.com',
            'link_exclusions': ['/videos/']
        }
    }
}

AJAX_HEADERS = {
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '"
                  "'Chrome/83.0.4103.97 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'"
              "'application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.google.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
}
