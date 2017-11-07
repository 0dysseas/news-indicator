import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import GObject, Gtk


class IndicatorABoutWindow(Gtk.Window):

    def __init__(self):
        super(IndicatorABoutWindow, self).__init__()
        about = Gtk.AboutDialog()
        about.set_program_name('News-Indicator')
        about.set_comments('Put comments here')
        # about.set_logo(put icon here)
        about.run()
        about.destroy()

    def __repr__(self):
        return self.get_title()


def render_about_window():
    IndicatorABoutWindow()
    Gtk.main()
