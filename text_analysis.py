# initialization
import csv
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from nltk.corpus import stopwords
from psutil import cpu_count

# analysis
from concurrent.futures import ProcessPoolExecutor, as_completed
import random
from statistics import mean
from config import SITE_CATEGORIES, SITE_SPIDER_CONFIG

# visualization
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from wordcloud import WordCloud
from config import SCATTER_PLOT_STYLE_PARAMS

# misc
from time import perf_counter
from typing import List


class ArticleTextAnalyzer:
    """Generic class to classify news articles and return most common words and phrases."""
    SENTENCES_CLASSIFIED_PER_ARTICLE = 50
    MAX_PROCESS_WORKERS = cpu_count(logical=False)
    STOP_WORDS = stopwords.words('english')
    STOP_WORDS.extend([
        'democrat', 'democrats', 'republican', 'republicans'
    ])

    def __init__(self, art_dict, search_term=''):
        self.article_blobs_dict = self.create_clean_sentences(art_dict, search_term)
        self.classifier = NaiveBayesClassifier(self.generate_training_data(self.article_blobs_dict))
        print('finished training classifier')

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
    def generate_training_data(art_dict) -> List[tuple]:
        """
        Creates training data for classifier from article dict based on site classifications in config.SITE_CATEGORIES

        :param art_dict: dict of the form {site: {sentences: list, subjectivity: list}}
        :type art_dict: dict
        :return: list of tuples to use as training data for classifier
        """

        sentence_cl = {cl: [] for cl in SITE_CATEGORIES}
        for site, sentence_analysis in art_dict.items():
            for cl, site_set in SITE_CATEGORIES.items():
                if site in site_set:
                    sentence_cl[cl].extend([(sentence, cl) for sentence in sentence_analysis['sentences']])
        max_articles = min(list(map(len, sentence_cl.values())))
        for cl in sentence_cl:
            sentence_cl[cl] = random.sample(sentence_cl[cl], max_articles)
        print('Number of sentences used to train classifier by type: ' + str(max_articles))

        return [tup for tup_list in sentence_cl.values() for tup in tup_list]

    @staticmethod
    def create_clean_sentences(article_dict, search_term) -> dict:
        """
        Wrapper for multiprocessing cleaning each article and creating sentences for classification

        :param search_term: word or phrase being searched
        :type search_term: str
        :param article_dict: dict of the form {site: list}
        :type article_dict: dict
        :return: dict of sites with dict values that contain cleaned and lemmatized sentences and subjectivity
        """
        clean_dict = {site: {'sentences': [], 'subjectivity': []} for site in article_dict}
        with ProcessPoolExecutor(max_workers=ArticleTextAnalyzer.MAX_PROCESS_WORKERS) as ex:
            futures = {ex.submit(ArticleTextAnalyzer.clean_text_blob, search_term,
                                 TextBlob(article), site, article_list.index(article), len(article_list)): site
                       for site, article_list in article_dict.items() for article in article_list}
            for f in as_completed(futures):
                for key, value in f.result().items():
                    clean_dict[futures[f]][key].extend(value)

        return clean_dict

    @staticmethod
    def clean_text_blob(search_term, art_tb, site, index, num_articles) -> dict:
        """
        Accepts articles as TextBlobs and breaks them up into sentences, removes stop words and lemmatizes,
        and measures subjectivity

        :param search_term: word or phrase being searched - will be excluded from final text
        :type search_term: str
        :param art_tb: TextBlob of a full article
        :type art_tb: TextBlob
        :param site: website key
        :type site: str
        :param index: index of article in list of articles for site
        :type index: int
        :param num_articles: total articles scraped for site
        :type num_articles: int
        :return: dict of the form {'sentences': list, 'subjectivity': list}
        """
        print(site + ': cleaning article ' + str(index + 1) + ' of ' + str(num_articles) + '.')
        clean_article = []
        subjectivity = []
        for sentence in art_tb.sentences[:ArticleTextAnalyzer.SENTENCES_CLASSIFIED_PER_ARTICLE]:
            if sentence.raw.find(SITE_SPIDER_CONFIG[site]['full_name']) > -1:
                continue
            clean_sentence = ''
            for word, pos in sentence.pos_tags:
                if word.lower() not in ArticleTextAnalyzer.STOP_WORDS and word not in ArticleTextAnalyzer.STOP_WORDS:
                    if word.lower() in TextBlob(search_term).words.lower():
                        continue
                    elif pos == 'NNP' or word == 'Crow':
                        clean_sentence += ' ' + word
                    elif pos == 'NNPS':
                        clean_sentence += ' ' + word.singularize()
                    else:
                        clean_sentence += ' ' + word.lemmatize().lower()
            clean_article.append(clean_sentence.strip())
            subjectivity.append(sentence.sentiment.subjectivity)
        print(site + ': finished cleaning article ' + str(index + 1) + ' of ' + str(num_articles) + '.')

        return {'sentences': clean_article, 'subjectivity': subjectivity}

    @staticmethod
    def generate_wordclouds(data, bgcolor, axes):
        cloud_strings = {bias: '' for bias in SITE_CATEGORIES}
        for key, sa in data.items():
            for bias, site_set in SITE_CATEGORIES.items():
                if key in site_set:
                    cloud_strings[bias] += ' ' + ' '.join([sentence for sentence in sa['sentences']])

        colors1 = [(1, 1, 1), (0, 0.48, 1)]
        colors2 = [(1, 1, 1), (1, 0.13, 0.13)]
        colormaps = [
            LinearSegmentedColormap.from_list(name='cm1', colors=colors1, N=100),
            LinearSegmentedColormap.from_list(name='cm1', colors=colors2, N=100)
        ]

        for axis, (bias, cloud_string), cm in zip(axes, cloud_strings.items(), colormaps):
            wc = WordCloud(
                background_color=bgcolor,
                max_words=100,
                collocations=True,
                colormap=cm
            ).generate_from_frequencies(TextBlob(cloud_string).np_counts)
            axis.imshow(wc)
            axis.axis('off')
            axis.set_title(bias.capitalize(), color='white', fontsize=16)

    def classify_nonpartisan_articles(self):
        """
        Classifies each article for each site not part of the training set.

        :return: Dictionary of the form {site: [classification(article)]
        """
        classifications = {}
        with ProcessPoolExecutor(max_workers=ArticleTextAnalyzer.MAX_PROCESS_WORKERS) as ex:
            for site, cl_dict in zip(self.article_blobs_dict.keys(), ex.map(self.calculate_means,
                                                                            self.article_blobs_dict.items())):
                classifications[site] = cl_dict

        return classifications

    def calculate_means(self, blobs_dict_item):
        site, sentence_analysis = blobs_dict_item
        print('calculating mean bias and subjectivity for ' + site)
        return {
            'bias': mean([self.classifier.prob_classify(sentence).prob('conservative')
                          for sentence in sentence_analysis['sentences']]),
            'subjectivity': mean(sentence_analysis['subjectivity'])
        }

    def plot_output(self, cl):
        # create dataframe for scatter plot
        plot_df = pd.DataFrame.from_dict(cl)
        plot_df = plot_df.transpose().reset_index()
        plot_df.rename(columns={'index': 'site'}, inplace=True)
        plot_df['full_name'] = plot_df['site'].apply(lambda x: SITE_SPIDER_CONFIG[x]['full_name'])
        print(plot_df)

        # scatter plot styling
        sns.set_style('ticks', SCATTER_PLOT_STYLE_PARAMS)

        # layout for output
        fig = plt.figure(constrained_layout=True)
        gs = fig.add_gridspec(2, 2)
        ax1 = fig.add_subplot(gs[0, :])
        ax1.spines['right'].set_visible(False)
        ax1.spines['top'].set_visible(False)
        ax2 = fig.add_subplot(gs[1, 0])
        ax3 = fig.add_subplot(gs[1, 1])

        # create scatter plot with point labels and assign to top row of layout
        sns.scatterplot(
            data=plot_df,
            x='bias',
            y='subjectivity',
            hue='bias',
            ax=ax1,
            legend=None,
            palette=sns.color_palette('coolwarm', as_cmap=True)
        )
        for i in range(plot_df.shape[0]):
            ax1.annotate(
                text=plot_df.full_name[i],
                xy=(plot_df.bias[i], plot_df.subjectivity[i]),
                textcoords='offset points',
                xytext=(0, 5),
                ha='center',
                fontsize=8,
                color='white'
            )

        # create word clouds and assign to bottom two slots in layout
        self.generate_wordclouds(
            data=self.article_blobs_dict,
            bgcolor='black',
            axes=[ax2, ax3]
        )

        plt.show()


if __name__ == '__main__':
    start = perf_counter()
    article_dict = ArticleTextAnalyzer.read_news_scraper_output_file_into_dict('./data/news_scraper_data.csv')
    ata = ArticleTextAnalyzer(article_dict, 'georgia voting law')
    cl = ata.classify_nonpartisan_articles()
    end = perf_counter()
    print(f'Ran in {end - start:0.4f} seconds')
    print(cl)
    ata.plot_output(cl)
