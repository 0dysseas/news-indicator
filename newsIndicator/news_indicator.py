import os
import signal
import logging
import webbrowser
from Queue import Queue
from datetime import datetime

import gi

import about_and_settings_wins

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

import notify2
from gi.repository import Gtk, AppIndicator3, GObject
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED

from get_news import DownloadNewsWorker
from utils import get_asset
from about_and_settings_wins import SettingsState

APP = 'News-Indicator'
JOB_ID = 'news_job'

try:
    scheduler = BlockingScheduler()
except ImportError:
    print ('Failed to import Scheduler')
    sys.exit(1)


class NewsIndicator(object):
    # Class variables to be shared among all NewsIndicator instances
    menu = None
    update_interval = 10

    icon = get_asset(asset='icon')

    indicator = AppIndicator3.Indicator.new(APP, icon, AppIndicator3.IndicatorCategory.OTHER)
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    def __init__(self):
        self.app = APP
        self.settings_changed = False

    def __repr__(self):
        return self.app

    @staticmethod
    def open_news_url(url):
        try:
            if not webbrowser.open_new_tab(url):
                raise webbrowser.Error
        except webbrowser.Error:
            print('Unable to open a web browser, try accessing this URL manually instead:\n{0}').format(url)

    @staticmethod
    def stop(self):
        Gtk.main_quit()  #TODO-me: scheduler.shutdown(wait=False) gia na kleisei o scheduler kai meta quit = sys.exit(1)

    @staticmethod
    def on_about(self):
        about_and_settings_wins.render_about_window()

    @staticmethod
    def on_settings(self):
        selected_status, selected_interval = settings_state.get_state()
        settings_changed, update_interval = about_and_settings_wins.render_settings_window(selected_status,
                                                                                           selected_interval,
                                                                                           settings_state)
        settings_state.update_state(settings_changed, update_interval)
        if settings_state.settings_triggered:
            modify_scheduler(JOB_ID, int(settings_state.settings_interval))

    def create_and_update_menu(self, list_of_news):
        print('in create menu is None')
        self.create_menu(list_of_news)

    def create_menu(self, menu_items):
        self.menu = Gtk.Menu()

        for k, v in enumerate(menu_items):
            # menu item
            first_item = Gtk.MenuItem(v['title'])
            first_item.connect('activate', self.open_news_url, v['url'])
            self.menu.append(first_item)

            # separator item
            separator = Gtk.SeparatorMenuItem()
            self.menu.append(separator)

        # settings item
        settings_item = Gtk.MenuItem('Settings')
        settings_item.connect('activate', self.on_settings)
        self.menu.append(settings_item)

        # about item
        about_item = Gtk.MenuItem('About')
        about_item.connect('activate', self.on_about)
        self.menu.append(about_item)

        # quit item
        quit_item = Gtk.MenuItem('Quit')
        quit_item.connect('activate', self.stop)
        self.menu.append(quit_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)
        self.indicator.set_label('News', APP)

        return self.menu


@scheduler.scheduled_job('interval', next_run_time=datetime.now(), minutes=10, id=JOB_ID, name='retrieve_news_job')
def main():

    output_queue = Queue()

    out_list = list()

    logging.info('Retrieving news...')
    download = DownloadNewsWorker(output_queue)
    download.retrieve_news()

    while not output_queue.empty():
        item = output_queue.get()  # Using output queue and then feed that into a list??? That's dummmy.FInd a better way..
        out_list.append(item)

    return out_list


# Listener that's triggered when each job is executed
def listen_for_new_updates(event):
    if event.retval:
        news_indicator.create_and_update_menu(event.retval)
        Gtk.main()


def modify_scheduler(job_id, new_interval):
    print ('Modified job')
    print('In modify_scheduler, id is:{}'.format(job_id))
    print ('In modify_scheduler, interv is:{}'.format(new_interval))
    scheduler.reschedule_job(job_id, trigger='interval', minutes=new_interval)


if __name__ == '__main__':
    news_indicator = NewsIndicator()
    settings_state = SettingsState(False, 0)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    scheduler.add_listener(listen_for_new_updates, EVENT_JOB_EXECUTED)
    scheduler.start()


