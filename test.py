from news_scraper import NewsScraper
from textblob import TextBlob

DRIVER = 'C:/Users/jason/chromedriver/chromedriver.exe'

scraper = NewsScraper(DRIVER)
articles = scraper.scrape('tpm', 'georgia voting law', 10)
# scraper.driver.close()
