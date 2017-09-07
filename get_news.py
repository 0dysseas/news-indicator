from Queue import Queue
from threading import Thread
from news import News
from time import time
import logging
import os
import sys

# TODO-me: Add an attribution link that reads "Powered by NewsAPI"

# TODO-me: Split news and sports sources?

# TODO-me: Put docstring comments in the functions

# TODO-me: Check at the beginning when importing the modultes if it is python2 or python3.
NUM_THREADS = 5

logging.basicConfig(level=logging.INFO)

try:
    API_KEY = os.environ.get('NEWS_API_KEY')
except KeyError:
    print ('Please save your personal NewsAPI key to a "NEWS_API_KEY" env variable.')
    sys.exit(1)


# news_sources = [guardian, al_jaz, hacker_news_top, nation_geog_top, tech_radar_top, next_web, ny_times]
# guardian = 'https://newsapi.org/v1/articles?source=the-guardian-uk&sortBy=latest&apiKey=' + API_KEY

class DownloadWorker(Thread):

    def __init__(self, input_queue):
        Thread.__init__(self, target=self.download_content)
        self.input_queue = input_queue

    def download_content(self):
        raise NotImplementedError


class DownloadNewsWorker(object):

    def __init__(self, output_queue):
        self.output_queue = output_queue

    def __repr__(self):
        return self.output_queue

    def retrieve_news(self):
        # Create an input_queue to store all API endpoints
        input_queue = Queue()

        # Create the worker threads. The number is arbitrary and will be optimized based on performance
        for i in range(NUM_THREADS):
            download_worker = DownloadWorker(input_queue)
            download_worker.setDaemon(True)  # Daemonize the working thread so as for the main thread to always exit
            download_worker.start()
        # TODO-me: Refactor the below into a helper function
        absolute_path = os.path.dirname(os.path.abspath(__file__))
        source_file = os.path.join(absolute_path, '/assets/news_sources.txt')
        with open(source_file, 'r') as f:
            news_sources = dict()
            for line in f:
                if not line.startswith('#') and line.split():
                    split_line = line.split(' = ')
                    news_sources[split_line[0]] = split_line[1]

        #TODO-me: Append to each value of the news_sources the API_KEY




def main():

    start = time()
    # news = News(news_sources)

    logging.info('Retrieving news...')
    # news.retrieve_news()
    print("Finished in: {}".format(time()-start))


if __name__ == '__main__':

    main()