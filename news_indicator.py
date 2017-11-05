import os
import webbrowser

import gi

import news_indicator_about

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, AppIndicator3, GObject

APP = 'News-Indicator'


class NewsIndicator(object):
    # Class variables to be shared among all NewsIndicator instances
    menu = None
    absolute_path = os.path.dirname(os.path.abspath(__file__))
    icon = os.path.join(absolute_path, 'assets/news_icon.png')

    indicator = AppIndicator3.Indicator.new(APP, icon, AppIndicator3.IndicatorCategory.OTHER)
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    def __init__(self):
        self.app = APP

    def __repr__(self):
        return self.app

    @staticmethod
    def open_news_url(self, url):
        try:
            if not webbrowser.open_new_tab(url):
                raise webbrowser.Error
        except webbrowser.Error:
            print('Unable to open a web browser, try accessing this URL manually instead:\n{0}').format(url)

    @staticmethod
    def stop(self):
        Gtk.main_quit()

    def on_about(self):
        news_indicator_about.render_about_window()

    def on_settings(self):
        pass

    def remove_previous_menu_entries(self, previous_menu):
        if previous_menu.get_children():
            for item in previous_menu.get_children():
                previous_menu.remove(item)

    def create_and_update_menu(self, menu_id, list_of_news):
        if menu_id is None:
            self.create_menu(list_of_news)
        else:
            self.remove_previous_menu_entries(menu_id)
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
        quit_item.connect('activate', NewsIndicator.stop)
        self.menu.append(quit_item)

        self.menu.show_all()
        self.indicator.set_menu(self.menu)
        self.indicator.set_label('News', APP)

        return self.menu




