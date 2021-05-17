from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from concurrent.futures import ProcessPoolExecutor
from nltk.corpus import stopwords
from time import perf_counter
from statistics import mean
import csv
from typing import List
from config import SITE_CATEGORIES, SITE_SPIDER_CONFIG


class ArticleTextAnalyzer:
    """Generic class to classify news articles and return most common words and phrases."""
    SENTENCES_CLASSIFIED_PER_ARTICLE = 50
    MAX_PROCESS_WORKERS = 2

    def __init__(self, art_dict):
        self.article_blobs_dict = {site: [TextBlob(article) for article in art_dict[site]] for site in art_dict}
        self.classifier = NaiveBayesClassifier(self.generate_training_data(self.article_blobs_dict))
        print('finished training classifier')

    @classmethod
    def generate_training_data(cls, training_dict) -> List[tuple]:
        """
        Generates the training data set used to build the classifier.

        :param training_dict: Dictionary of the form {site: list of articles}
        :type training_dict: dict
        :return: Training data of the form [(article, classification)]
        """
        print('generating training data')
        train = []
        count_num_sentences = {}
        for cl, site_set in SITE_CATEGORIES.items():
            count_num_sentences[cl] = 0
            for site in site_set:
                num_articles = len(training_dict[site])
                for ind in range(num_articles):
                    train.append((training_dict[site][ind], cl, site, ind, num_articles))
        with ProcessPoolExecutor(max_workers=ArticleTextAnalyzer.MAX_PROCESS_WORKERS) as executor:
            train = [(sentence, row[1]) for row, sentence_list in zip(train, executor.map(cls.clean_text_blob, train))
                     for sentence in sentence_list[0]]
        for cl in SITE_CATEGORIES:
            count_num_sentences[cl] = len([row for row in train if row[1] == cl])
        print('Number of sentences being used to train classifier: ' + str(count_num_sentences))
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

    @staticmethod
    def clean_text_blob(row) -> List[list]:
        """
        Converts articles into TextBlobs and removes stop words.

        :param row: Tuple of the form (article (str), category (str), site (str), article number (int),
                          number of articles for site (int))
        :type row: tuple
        :return: List of sentences stripped of stop words and all but proper nouns lemmatized and lowercased
        """
        art_tb, cl, site, index, num_articles = row
        print(site + ': cleaning article ' + str(index + 1) + ' of ' + str(num_articles) + '.')
        clean_article = []
        subjectivity = []
        for sentence in art_tb.sentences[:ArticleTextAnalyzer.SENTENCES_CLASSIFIED_PER_ARTICLE]:
            if sentence.raw.find(SITE_SPIDER_CONFIG[site]['full_name']) > -1:
                continue
            clean_sentence = ''
            for word, pos in sentence.pos_tags:
                if pos in ('NNP', 'NNPS') or word == 'Crow':
                    clean_sentence += ' ' + word
                else:
                    if word not in stopwords.words('english'):
                        clean_sentence += ' ' + word.lemmatize().lower()
            clean_article.append(clean_sentence.strip())
            subjectivity.append(sentence.sentiment.subjectivity)
        print(site + ': finished cleaning article ' + str(index + 1) + ' of ' + str(num_articles) + '.')

        return [clean_article, subjectivity]

    def classify_nonpartisan_articles(self):
        """
        Classifies each article for each site not part of the training set.

        :return: Dictionary of the form {site: [classification(article)]
        """
        classifications = {}
        prob_conserv_list = []
        for key in self.article_blobs_dict:
            art_list_length = len(self.article_blobs_dict[key])
            for ind in range(art_list_length):
                prob_conserv_list.append((self.article_blobs_dict[key][ind], '', key, ind, art_list_length))
        with ProcessPoolExecutor(max_workers=ArticleTextAnalyzer.MAX_PROCESS_WORKERS) as executor:
            prob_conserv_list = [(row[2],
                                  [self.classifier.prob_classify(sentence).prob('conservative')
                                   for sentence in sentence_list[0]],
                                  [sentence for sentence in sentence_list[1]])
                                 for row, sentence_list in zip(prob_conserv_list,
                                                               executor.map(self.clean_text_blob, prob_conserv_list))]
        for row in prob_conserv_list:
            if len(row[1]) > 0:
                if row[0] in classifications:
                    classifications[row[0]].append((mean(row[1]), mean(row[2])))
                else:
                    classifications[row[0]] = [(mean(row[1]), mean(row[2]))]
        for key in classifications:
            classifications[key] = (mean(classifications[key][0]), mean(classifications[key][1]))
        upper_lim = mean([prob[0] for key, prob in classifications.items() if key in SITE_CATEGORIES['conservative']])
        lower_lim = mean([prob[0] for key, prob in classifications.items() if key in SITE_CATEGORIES['liberal']])
        for key in classifications:
            if key in SITE_CATEGORIES['conservative']:
                classifications[key] = (1, classifications[key][1])
            elif key in SITE_CATEGORIES['liberal']:
                classifications[key] = (0, classifications[key][1])
            else:
                classifications[key] = ((classifications[key][0] - lower_lim) / (upper_lim - lower_lim),
                                        classifications[key][1])
        return classifications


if __name__ == '__main__':
    start = perf_counter()
    article_dict = ArticleTextAnalyzer.read_news_scraper_output_file_into_dict('./data/news_scraper_data.csv')
    ata = ArticleTextAnalyzer(article_dict)
    print(ata.classifier.show_informative_features())
    print(ata.classify_nonpartisan_articles())
    end = perf_counter()
    print(f'Ran in {end - start:0.4f} seconds')
