import sys
import signal
import logging
import webbrowser
from Queue import Queue
from datetime import datetime

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

import notify2
from gi.repository import Gtk, AppIndicator3, GObject
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED

from get_news import DownloadNewsWorker
from utils import get_asset
from about_and_settings_wins import SettingsState, render_settings_window, render_about_window, INTERVALS

# Constants
APP = 'News-Indicator'
JOB_ID = 'news_job'
ICON = get_asset(asset='icon')

try:
    scheduler = BlockingScheduler()
except ImportError:
    raise ImportError('Failed to import Scheduler')
    sys.exit(1)


class NewsIndicator(object):
    """
    The main Indicator class. It's the Observer B in the Observer pattern and changes state (notifications, interval)
    based on the Observable's behavior.
    """

    # Class variables to be shared among all NewsIndicator instances
    menu = None
    update_interval = 10
    notifications = True

    indicator = AppIndicator3.Indicator.new(APP, ICON, AppIndicator3.IndicatorCategory.OTHER)
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    def __init__(self):
        self.app = APP
        self.settings_changed = False

    def __repr__(self):
        return self.app

    @staticmethod
    def open_news_url(self, url):
        """
        Opens the selected url in the default browser
        """

        try:
            if not webbrowser.open_new_tab(url):
                raise webbrowser.Error
        except webbrowser.Error:
            print('Unable to open a web browser, try accessing this URL manually instead:\n{0}'.format(url))

    @staticmethod
    def stop(self):
        scheduler.shutdown(wait=False)
        Gtk.main_quit()
        sys.exit(1)

    @staticmethod
    def on_about(self):
        """
        Callback function for the about menu item
        """
        render_about_window()

    @staticmethod
    def on_settings(self):
        """
        Callback function for the settings menu item. Pulls the app state, notifications state & the interval
        selected by the user, and updates accordingly the SettingsState class.
        """

        # Pull the current app state from the relay Observer object
        status, interval, ntfc_status, ntfc_state = settings_state.get_state()

        # Pass it to the Observable object in order to render the Settings window
        settings_changed, update_interval, ntfc_changed, ntfc_selected = render_settings_window(
            status, interval, ntfc_status, ntfc_state, settings_state)

        # Register any state changes
        settings_state.update_state(settings_changed, update_interval, ntfc_changed, ntfc_selected)

        # If the interval has changed, reprogram scheduler to run at the new interval
        if settings_state.intrvl_change_trig:
            modify_scheduler(JOB_ID, settings_state.settings_interval)

        if settings_state.notification_change_trig:
            NewsIndicator.notifications = False if not settings_state.notification_state else True

    def create_and_update_menu(self, list_of_news):
        """
        Wrapper for creating and updating the indicator menu
        with the list of news.
        """
        self.create_menu(list_of_news)

    def create_menu(self, menu_items):
        # create indicator
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

        # exit item
        exit_item = Gtk.MenuItem('Exit')
        exit_item.connect('activate', self.stop)
        self.menu.append(exit_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)

        return self.menu


def show_notifications(run_time):
    """
    Show the notification pop-up window
    """
    # Initialize the d-bus connection and create the notification object
    notify2.init("News Indicator")
    n = notify2.Notification(None, icon=ICON)

    # Set the urgency level and the timeout
    n.set_urgency(notify2.URGENCY_NORMAL)
    n.set_timeout(10000)
    formatted_time = run_time.time().strftime('%H:%M')
    message = 'Your {} news are here!'.format(formatted_time)

    n.update('News Indicator', message=message, icon=ICON)
    n.show()


def listen_for_new_updates(event):
    """
    Listener that's triggered every time a successful job(news retrieval) is executed.
    Upon its call it creates and renders the main indicator menu."
    """

    if event.retval:
        news_indicator.create_and_update_menu(event.retval)
        if NewsIndicator.notifications:
            show_notifications(event.scheduled_run_time)
        Gtk.main()


def modify_scheduler(job_id, new_interval):
    """
    Modifies the scheduler object in order to retrieve the news based on the new interval, as selected by the
    user in the indicator settings.
    """
    minutes = INTERVALS[new_interval][:2]
    scheduler.reschedule_job(job_id, trigger='interval', minutes=int(minutes))


@scheduler.scheduled_job('interval', next_run_time=datetime.now(), minutes=10, id=JOB_ID, name='retrieve_news_job')
def main():
    """
    Main function used to retrieve the news from the sources, based on a defined time interval

    """
    output_queue = Queue()

    out_list = list()

    logging.info('Retrieving news...')
    download = DownloadNewsWorker(output_queue)
    download.retrieve_news()

    while not output_queue.empty():
        item = output_queue.get()
        out_list.append(item)

    return out_list


def run_indicator():
    global news_indicator
    global settings_state
    news_indicator = NewsIndicator()
    # Init the default newsindicator settings state to: news retrieval per 10' & notifications True
    settings_state = SettingsState(False, 0, False, True)
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    scheduler.add_listener(listen_for_new_updates, EVENT_JOB_EXECUTED)
    scheduler.start()


if __name__ == '__main__':
    run_indicator()
