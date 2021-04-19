from news_scraper import NewsScraper
from textblob import TextBlob

DRIVER = 'C:/Users/jason/chromedriver/chromedriver.exe'

scraper = NewsScraper(DRIVER)
articles = scraper.scrape('blaze', 'georgia voting', 25)
scraper.driver.close()
