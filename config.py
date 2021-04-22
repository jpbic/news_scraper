SITE_SCRAPE_CONFIG = {
    'daily_wire': {
        'full_name': 'Daily Wire',
        'search_pagination_type': 'new_page',
        'query_string': r'https://www.dailywire.com/search/news?query={query}&page={page}',
        'initial_page_index': 1,
        'search_term_concat': r'%20',
        'articles_links_xpath': r'//article/a',
        'articles_content_xpath': r'//div[@id="post-body-text"]//p'
    },
    'blaze': {
        'full_name': 'The Blaze',
        'search_pagination_type': 'load_button',
        'query_string': r'https://www.theblaze.com/search/?q={query}',
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
        'articles_links_xpath': r'//article//div[@class="gsc-thumbnail-inside"]//a[contains(@class, "gs-title")]',
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
        'articles_content_xpath': r'//div[@class="td-post-content"]//p'
    },
    'tpm': {
        'full_name': 'Talking Points Memo',
        'search_pagination_type': 'new_page',
        'query_string': r'https://talkingpointsmemo.com/search/{query}/page/{page}',
        'initial_page_index': 1,
        'search_term_concat': r'+',
        'articles_links_xpath': r'//a[@class="Archive__PostImage"]',
        'articles_content_xpath': r'//div[@id="article-content"]//p'
    },
    'cnbc': {
        'full_name': 'CNBC',
        'search_pagination_type': 'infinite_scroll',
        'query_string': r'https://www.cnbc.com/search/?query={query}&qsearchterm={query}',
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
        'articles_links_xpath': r'//article//h2[@class="title"]/a',
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
        'query_string': r'https://www.cnn.com/search?q={query}&size=10&from=10&page={page}',
        'initial_page_index': 1,
        'search_term_concat': r'%20',
        'articles_links_xpath': r'//div[@class="cnn-search__result-contents"]//a',
        'articles_content_xpath': r'//div[@class="l-container"]//*[contains(@class, "zn-body__paragraph")]',
        'sort_button_xpath': r'//ul[contains(@class, "n_search-drop")]',
        'relevance_button_xpath': r'//li[@id="relevance"]'
    },
    'abc': {

    },
    'ny_post': {

    },
    'cbs': {

    },
    'npr': {

    },
    'politico': {

    },
    'axios': {

    }
}

SITE_CATEGORIES = {
    'Conservative': ['daily_wire', 'blaze', 'breitbart'],
    'Liberal': ['slate', 'bipartisan_report', 'tpm'],
    'Mainstream': ['cnbc']
}
