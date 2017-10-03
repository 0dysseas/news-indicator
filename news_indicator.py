import os
import signal

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk, AppIndicator3, GObject


class NewsIndicator(object):
    def __init__(self, news_list):
        self.app = 'News-Indicator'
        self.news_list = news_list

        absolute_path = os.path.dirname(os.path.abspath(__file__))
        icon = os.path.join(absolute_path, 'assets/news_icon.png')

        self.indicator = AppIndicator3.Indicator.new(self.app, icon, AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        print('hello')
        # self.x = self.indicator.get_menu()  #TODO-me:Use this!
        print('hello_2')
        self.indicator.set_menu(self.create_menu(self.news_list))
        print('hello_3')
        self.indicator.set_label('News', self.app)

    def create_menu(self, menu_items_list):

        # if current_menu and current_menu.get_children():  #TODO-me: Make it work
        #     print('in here')
        #     for item in current_menu.get_children():
        #         current_menu.remove(item)

        menu = Gtk.Menu()

        for k, v in enumerate(menu_items_list):
            first_item = Gtk.MenuItem(v['title'])
            menu.append(first_item)
            separator = Gtk.SeparatorMenuItem()
            menu.append(separator)

        quit_item = Gtk.MenuItem('Quit')
        quit_item.connect('activate', self.stop)
        menu.append(quit_item)

        menu.show_all()
        return menu

    def stop(self, source):
        Gtk.main_quit()

#
# if __name__ == '__main__':
#     # NewsIndicator()
#     # signal.signal(signal.SIGINT, signal.SIG_DFL)
#     # Gtk.main()

