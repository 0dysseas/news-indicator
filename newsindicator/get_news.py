import logging
import os
import sys
from threading import Thread

try:
  from Queue import Queue
except:
  from queue import Queue

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

import requests
import notify2

from .utils import get_news_sources_from_file, delete_redundant_items

NUM_THREADS = 8
MESSAGE = ' NEWS_API_KEY not found!! \nHave you stored it in ~/.profile?'

logging.basicConfig(level=logging.INFO)


def show_alert_notifications():
    """
    Shows the alert notification pop-up window
    """
    # Initialize the d-bus connection and create the notification object
    notify2.init("News Indicator")
    n = notify2.Notification(None)

    # Set the urgency level and the timeout
    n.set_urgency(notify2.URGENCY_NORMAL)
    n.set_timeout(9000)

    n.update('News Indicator', message=MESSAGE)
    n.show()


class DownloadWorker(Thread):
    """
    Main class that retrieves the actual articles from the corresponding urls,using multiple threads.
    """

    def __init__(self, input_queue, out_queue):
        # Init threads and queues
        Thread.__init__(self, target=self.download_content)
        self.input_queue = input_queue
        self.out_queue = out_queue

    def __repr__(self):
        return self.input_queue

    def _form_news_structure(self, json_news):
        """
        Normalize the news JSON and push cleaned article dicts to self.out_queue.

        - Safely handles missing or malformed json_news and articles.
        - Only extracts a small set of useful fields (title, url, source, urlToImage).
        - Limits to the first 4 articles (configurable here).
        - Returns a list of processed article dicts.
        """
        if not isinstance(json_news, dict):
            logging.warning("Expected json_news to be a dict, got %s", type(json_news))
            return []

        articles = json_news.get('articles') or []
        if not isinstance(articles, list):
            logging.warning("Expected 'articles' to be a list, got %s", type(articles))
            return []

        max_items = 4
        processed = []

        for idx, article in enumerate(articles[:max_items]):
            if not isinstance(article, dict):
                logging.debug("Skipping article at index %d because it's not a dict: %r", idx, article)
                continue

            # Prefer whitelisting fields instead of trying to delete many keys.
            source = ''
            src_field = article.get('source')
            if isinstance(src_field, dict):
                source = src_field.get('name') or ''
            elif isinstance(src_field, str):
                source = src_field

            cleaned = {
                'title': article.get('title') or '',
                'url': article.get('url') or '',
                'source': source,
                'urlToImage': article.get('urlToImage') or '',
            }

            # Remove empty values to keep payload small
            cleaned = {k: v for k, v in cleaned.items() if v}

            if cleaned.get('title') and cleaned.get('url'):
                self.out_queue.put(cleaned)
                processed.append(cleaned)
            else:
                logging.debug("Skipping article without title or url: %r", article)

        return processed

    def download_content(self):
        """
        Asynchronously downloads the content from the news sources.
        """
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
        # Init output queue
        self.output_queue = output_queue

    def __repr__(self):
        return self.output_queue

    def retrieve_news(self):
        # retrieves news
        try:
            # api_key = str(os.environ.get('NEWS_API_KEY'))
            api_key = os.environ['NEWS_API_KEY']
        except KeyError:
            show_alert_notifications()
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
