import logging
import os
import sys
from Queue import Queue
from threading import Thread

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

import requests

from utils import get_news_sources_from_file, delete_redundant_items

NUM_THREADS = 8

logging.basicConfig(level=logging.INFO)


class DownloadWorker(Thread):
    """
    Main class that retrieves the actual articles from the corresponding urls, in a multi-threaded way.
    """

    def __init__(self, input_queue, out_queue):
        Thread.__init__(self, target=self.download_content)
        self.input_queue = input_queue
        self.out_queue = out_queue

    def __repr__(self):
        return self.input_queue

    def _form_news_structure(self, json_news):
        keys_to_remove = ['status', 'sortBy']
        sub_keys_to_remove = ['description', 'author', 'publishedAt']

        filtered_news_sources_format = delete_redundant_items(json_news, keys_to_remove)

        # Get the first four articles from each source
        for _, article in enumerate(filtered_news_sources_format['articles'][:2]):
            final_news_sources_format = delete_redundant_items(article, sub_keys_to_remove)
            self.out_queue.put(final_news_sources_format)

        return json_news

    def download_content(self):
        while True:
            link = self.input_queue.get()
            response = requests.get(link).json()

            self._form_news_structure(response)

            self.input_queue.task_done()


class DownloadNewsWorker(object):
    """
    Class used to get the news from the sources file and then put them in the input queue
    """

    def __init__(self, output_queue):
        self.output_queue = output_queue

    def __repr__(self):
        return self.output_queue

    def retrieve_news(self):
        try:
            # api_key = str(os.environ.get('NEWS_API_KEY'))
            api_key = os.environ['NEWS_API_KEY']
        except KeyError:
            print ('Please save your personal NewsAPI key in a "NEWS_API_KEY" env variable.')
            sys.exit(1)

        # Create an input_queue to store all API endpoints
        input_queue = Queue()

        # Create the worker threads. The number is arbitrary and will be optimized based on performance
        for i in range(NUM_THREADS):
            download_worker = DownloadWorker(input_queue, self.output_queue)
            # Daemonize the working thread so as the main thread always exits
            download_worker.setDaemon(True)
            download_worker.start()

        news_sources = get_news_sources_from_file()
        # Put each news source into the queue
        for _, val in news_sources.items():
            news_item = '='.join([val, api_key])
            input_queue.put(news_item)

        input_queue.join()
