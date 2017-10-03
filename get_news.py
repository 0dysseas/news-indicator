import logging
import os
import signal
import sys
from time import time
from Queue import Queue
from threading import Thread

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, AppIndicator3, GObject
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_ALL
import requests

from news_indicator import NewsIndicator
from news_helpers import print_json_object, get_news_sources_from_file, delete_redundant_items


# TODO-me: Add an attribution link that reads "Powered by NewsAPI"

# TODO-me: Split news and sports sources? Use beautifulsoup for greek sites

# TODO-me: Check  importing the modules if it is python2 or python3.

NUM_THREADS = 8

logging.basicConfig(level=logging.INFO)

try:  # TODO-me: Refactor the two try clauses
    API_KEY = str(os.environ.get('NEWS_API_KEY'))
except KeyError:
    print ('Please save your personal NewsAPI key in a "NEWS_API_KEY" env variable.')
    sys.exit(1)

try:
    sched = BlockingScheduler()
except ImportError:
    print ('Failed to import Scheduler')
    sys.exit(1)


class DownloadWorker(Thread):

    def __init__(self, input_queue, out_queue):
        Thread.__init__(self, target=self.download_content)  # TODO-me: Add intervals for continuous thread running i.e. downloading of sources
        self.input_queue = input_queue
        self.out_queue = out_queue

    def __repr__(self):
        return self.input_queue

    def _form_news_structure(self, json_news):
        keys_to_remove = ['status', 'sortBy']
        sub_keys_to_remove = ['description', 'author', 'publishedAt']  # TODO-me: Handle the National Geographic case

        # TODO-me: Optimize below code!
        json_1 = delete_redundant_items(json_news, keys_to_remove)

        # Get the first four articles from each source
        for _, article in enumerate(json_1['articles'][:2]):
            json_2 = delete_redundant_items(article, sub_keys_to_remove)

            self.out_queue.put(json_2)

        # for k, v in enumerate(self.out_queue):
        #     print k, v
        return json_news

    def download_content(self):
        while True:
            link = self.input_queue.get()
            response = requests.get(link).json()

            self._form_news_structure(response)

            self.input_queue.task_done()


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
            download_worker = DownloadWorker(input_queue, self.output_queue)
            download_worker.setDaemon(True)  # Daemonize the working thread so as the main thread always exits
            download_worker.start()

        news_sources = get_news_sources_from_file()
        # Put each news source into the queue
        for _, val in news_sources.iteritems():
            news_item = '='.join([val, API_KEY])
            input_queue.put(news_item)

        input_queue.join()


@sched.scheduled_job('interval', minutes=2, name='my_job_1')  # TODO-me: Change the job_id
def main():

    # start = time()

    output_queue = Queue()

    out_list = list()

    print('here')
    # logging.info('Retrieving news...')
    download = DownloadNewsWorker(output_queue)
    download.retrieve_news()
    # logging.info('Printing output queue...')
    # while not output_queue.empty():
    #     print (output_queue.get())
    # logging.info('Output..')
    while not output_queue.empty():
        item = output_queue.get()  # Using output queue and then feed that into a list??? That's dummmy.FInd a better way..
        out_list.append(item)

    print('after')
    # NewsIndicator(out_list)  # TODO-me: Update the idle thread not the main one
    # signal.signal(signal.SIGINT, signal.SIG_DFL)
    # Gtk.main()
    return out_list
    # print("Finished in: {}".format(time()-start))


# Listener that is triggered when each job is executed
def my_listener(event):  # TODO-me:Rename this
    if event.retval:
        print event.retval
        NewsIndicator(event.retval)  # Feed the out_list of main() to NewsIndicator
        Gtk.main()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sched.add_listener(my_listener, EVENT_JOB_EXECUTED)
    sched.start()

    # print('before')
    # final_list = main()
    # print('after')
    # NewsIndicator(final_list)  #TODO-me: Update the idle thread not the main one
    # signal.signal(signal.SIGINT, signal.SIG_DFL)
    # Gtk.main()
