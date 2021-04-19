SITE_SCRAPE_CONFIG = {
    'daily_wire': {
        'search_pagination_type': 'new_page',
        'query_string': r'https://www.dailywire.com/search/news?query={query}&page={page}',
        'initial_page_index': 1,
        'search_term_concat': r'%20',
        'articles_links_xpath': r'//article/a',
        'articles_content_xpath': r'//div[@id="post-body-text"]//p'
    },
    'blaze': {
        'search_pagination_type': 'load_button',
        'query_string': r'https://www.theblaze.com/search/?q={query}{page}',
        'initial_page_index': '',
        'search_term_concat': r'+',
        'load_button_xpath': r'//div[contains(@class, "button-load-more"]',
        'articles_links_xpath': r'//article/a[contains(@class, "custom-post-headline")]',
        'articles_content_xpath': r'//div[@id="body-description"]//p'
    }
}
