import os
import gi
import signal
gi.require.version('Gtk', '3.0')
gi.require.version('AppIndicator3', '0.1')
from gi.repository import Gtk
from gi.repository import AppIndicator3


class NewsIndicator(object):

    def __init__(self):
        self.app = 'News-Indicator'
        absolute_path = os.path.dirname(os.path.abspath(__file__))
        icon = os.path.join(absolute_path, 'news_icon.png')
        self.indicator = AppIndicator3.Indicator.new(self.app, icon, AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label('News', self.app)

    def create_menu(self):
        menu = Gtk.menu()
        first_item = Gtk.MenuItem('Test_News_Item')
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

NewsIndicator()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()