import logging
import os
import sys
from time import time
from Queue import Queue
from threading import Thread

import requests

from news_helpers import print_json_object, get_news_sources_from_file, delete_redundant_items


# TODO-me: Add an attribution link that reads "Powered by NewsAPI"

# TODO-me: Split news and sports sources? Use beautifulsoup for greek sites

# TODO-me: Check  importing the modules if it is python2 or python3.

NUM_THREADS = 8

logging.basicConfig(level=logging.INFO)

try:
    API_KEY = str(os.environ.get('NEWS_API_KEY'))
except KeyError:
    print ('Please save your personal NewsAPI key in a "NEWS_API_KEY" env variable.')
    sys.exit(1)


class DownloadWorker(Thread):

    def __init__(self, input_queue, out_list):
        Thread.__init__(self, target=self.download_content)
        self.input_queue = input_queue
        self.out_list = out_list

    def __repr__(self):
        return self.input_queue

    def _form_news_structure(self, json_news):
        keys_to_remove = ['status', 'sortBy']
        sub_keys_to_remove = ['description', 'author', 'publishedAt']  # TODO-me: Handle the National Geographic case

        # TODO-me: Optimize below code!
        json_1 = delete_redundant_items(json_news, keys_to_remove)

        for _, article in enumerate(json_1['articles']):
            json_2 = delete_redundant_items(article, sub_keys_to_remove)

            self.out_list.append(json_2)

        for k, v in enumerate(self.out_list):
            print k, v
        return json_news

    def download_content(self):
        while True:
            link = self.input_queue.get()
            response = requests.get(link).json()

            self._form_news_structure(response)

            self.input_queue.task_done()

        return None


class DownloadNewsWorker(object):

    def __init__(self, output_list):
        self.output_list = output_list

    def __repr__(self):
        return self.output_queue

    def retrieve_news(self):
        # Create an input_queue to store all API endpoints
        input_queue = Queue()

        # Create the worker threads. The number is arbitrary and will be optimized based on performance
        for i in range(NUM_THREADS):
            download_worker = DownloadWorker(input_queue, self.output_list)
            download_worker.setDaemon(True)  # Daemonize the working thread so as the main thread always exits
            download_worker.start()

        news_sources = get_news_sources_from_file()
        # Put each news source into the queue
        for _, val in news_sources.iteritems():
            news_item = '='.join([val, API_KEY])
            input_queue.put(news_item)

        input_queue.join()


def main():

    start = time()

    test_list = list()
    logging.info('Retrieving news...')
    download = DownloadNewsWorker(test_list)
    download.retrieve_news()
    print("Finished in: {}".format(time()-start))


if __name__ == '__main__':

    main()
