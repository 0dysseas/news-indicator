import logging
import os
# import signal
import sys
from Queue import Queue
from threading import Thread
# from datetime import datetime

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

import requests
# from gi.repository import Gtk, AppIndicator3, GObject
# from apscheduler.schedulers.background import BlockingScheduler
# from apscheduler.events import EVENT_JOB_EXECUTED


# from news_indicator import NewsIndicator
from news_helpers import get_news_sources_from_file, delete_redundant_items, print_json_object

# TODO-me: Split news and sports sources? Use beautifulsoup for greek sites

# TODO-me: Check  importing the modules if it is python2 or python3.

NUM_THREADS = 8

logging.basicConfig(level=logging.INFO)

try:  # TODO-me: Refactor the two try clauses
    API_KEY = str(os.environ.get('NEWS_API_KEY'))
except KeyError:
    print ('Please save your personal NewsAPI key in a "NEWS_API_KEY" env variable.')
    sys.exit(1)

# try:
#     sched = BlockingScheduler()
# except ImportError:
#     print ('Failed to import Scheduler')
#     sys.exit(1)


class DownloadWorker(Thread):

    def __init__(self, input_queue, out_queue):
        Thread.__init__(self, target=self.download_content)
        self.input_queue = input_queue
        self.out_queue = out_queue

    def __repr__(self):
        return self.input_queue

    def _form_news_structure(self, json_news):
        keys_to_remove = ['status', 'sortBy']
        sub_keys_to_remove = ['description', 'author', 'publishedAt']  # TODO-me: Handle the National Geographic case

        # TODO-me: Optimize below code!
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


# @sched.scheduled_job('interval', next_run_time=datetime.now(), minutes=2, id='news_job', name='retrieve_news_job')
# def main():
#
#     output_queue = Queue()
#
#     out_list = list()
#
#     logging.info('Retrieving news...')
#     download = DownloadNewsWorker(output_queue)
#     download.retrieve_news()
#
#     while not output_queue.empty():
#         item = output_queue.get()  # Using output queue and then feed that into a list??? That's dummmy.FInd a better way..
#         print_json_object(item)
#         out_list.append(item)
#
#     return out_list
#
#
# # Listener that is triggered when each job is executed
# def listen_for_new_updates(event):
#     if event.retval:
#
#         news_indicator = NewsIndicator()
#         news_indicator.create_and_update_menu(NewsIndicator.menu, event.retval)
#         changed_interv, interv = news_indicator.settings_changed, news_indicator.update_interval
#         # changed_interv, interv = news_indicator.on_settings()
#         if changed_interv:
#             # if interv != 2: # Change this back to 10 min
#             print('In changed_interv, id is:{}'.format(event.job_id))
#             print ('In changed_interv, interv is:{}'.format(interv))
#             # Unschedule decorated function
#             # sched.remove_job(event.job_id)
#             modify_scheduler(event.job_id, interv)
#         Gtk.main()
#
#
# def modify_scheduler(job_id, new_interval):
#     print ('MOdified job')
#     sched.reschedule_job(job_id, trigger='interval', minutes=new_interval)
#
#
#
# if __name__ == '__main__':
#     signal.signal(signal.SIGINT, signal.SIG_DFL)
#     sched.add_listener(listen_for_new_updates, EVENT_JOB_EXECUTED)
#     sched.start()
