import os

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, AppIndicator3, GObject


class NewsIndicator(object):

    menu = None

    def __init__(self):
        pass

    @classmethod
    def init_indicator(cls):
        cls.app = 'News-Indicator'
        absolute_path = os.path.dirname(os.path.abspath(__file__))
        icon = os.path.join(absolute_path, 'assets/news_icon.png')

        cls.indicator = AppIndicator3.Indicator.new(cls.app, icon, AppIndicator3.IndicatorCategory.OTHER)
        cls.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        return True

    @classmethod
    def create_menu(cls, menu_items):
        cls.menu = Gtk.Menu()

        for k, v in enumerate(menu_items):
            first_item = Gtk.MenuItem(v['title'])
            cls.menu.append(first_item)
            separator = Gtk.SeparatorMenuItem()
            cls.menu.append(separator)

        quit_item = Gtk.MenuItem('Quit')
        quit_item.connect('activate', NewsIndicator.stop)
        cls.menu.append(quit_item)

        cls.menu.show_all()
        cls.indicator.set_menu(cls.menu)
        cls.indicator.set_label('News', cls.app)

        return cls.menu

    @classmethod
    def create_and_update_menu(cls, upd_menu, list_of_news):  #TODO-me: Rename the upd_menu var
        if upd_menu is None:
            cls.create_menu(list_of_news)
        else:
            cls.remove_old_menu_entries(upd_menu)
            cls.create_menu(list_of_news)

    @classmethod
    def remove_old_menu_entries(cls, old_menu):
        if old_menu.get_children():
            for item in old_menu.get_children():
                old_menu.remove(item)

    @staticmethod
    def stop():
        Gtk.main_quit()
