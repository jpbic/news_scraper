from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from config import SITE_CATEGORIES
import csv
from typing import List


class ArticleTextAnalyzer:
    """Generic class to classify news articles and return most common words and phrases."""
    def __init__(self, art_dict):
        self.classifier = NaiveBayesClassifier(self.generate_training_data(art_dict))
        self.article_blobs_dict = self.articles_to_text_blobs(art_dict)

    @staticmethod
    def generate_training_data(training_dict) -> List[tuple]:
        """
        Generates the training data set used to build the classifier.

        :param training_dict: Dictionary of the form {site: list of articles}
        :type training_dict: dict
        :return: Training data of the form [(article, classification)]
        """
        train = [(article, 'conservative') for key in training_dict
                 for article in training_dict[key]
                 if key in SITE_CATEGORIES['conservative']]
        train.extend([(article, 'liberal') for key in training_dict
                      for article in training_dict[key]
                      if key in SITE_CATEGORIES['liberal']])
        return train

    @staticmethod
    def read_news_scraper_output_file_into_dict(filepath) -> dict:
        """
        Reads the CSV output from the NewsScraper class into a dictionary.

        :param filepath: File path of the CSV.
        :type filepath: str
        :return: Returns a dictionary of the form {site: list of articles}
        """
        with open(filepath) as f:
            reader = csv.DictReader(f, delimiter='|')
            prev_site = ''
            output_dict = {}
            for row in reader:
                if row['site'] == prev_site:
                    output_dict[row['site']].append(row['article'])
                else:
                    prev_site = row['site']
                    output_dict[row['site']] = [row['article']]
            return output_dict

    def articles_to_text_blobs(self, art_dict) -> dict:
        """
        Converts article text for sites not part of the training set into TextBlobs

        :param art_dict: Dictionary of articles of the form {site: list of articles}
        :return: Dictionary of the form {site: [TextBlob(article)]
        """
        for key in art_dict:
            art_dict[key] = [TextBlob(article, classifier=self.classifier) for article in art_dict[key]
                             if key not in SITE_CATEGORIES['conservative'] and key not in SITE_CATEGORIES['liberal']]
        return art_dict

    def classify_nonpartisan_articles(self):
        """
        Classifies each article for each site not part of the training set.

        :return: Dictionary of the form {site: [classification(article)]
        """
        classifications = {}
        for key in self.article_blobs_dict:
            classifications[key] = [self.classifier.prob_classify(article).prob('conservative')
                                    for article in self.article_blobs_dict[key]]
        return classifications


if __name__ == '__main__':
    article_dict = ArticleTextAnalyzer.read_news_scraper_output_file_into_dict('./data/news_scraper_data.csv')
    ata = ArticleTextAnalyzer(article_dict)
    # print(ata.classifier)
    # print(ata.classifier.show_informative_features())
    print(ata.classifier.prob_classify('restrictions').max())
    # print(ata.classify_nonpartisan_articles())
    # print(TEST_ARTICLES)
