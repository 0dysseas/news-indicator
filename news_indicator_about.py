import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import GObject, Gtk as gtk


class IndicatorABoutWindow(gtk.Window):

    def __init__(self):
        super(IndicatorABoutWindow, self).__init__()
        self.set_size_request(300, 150)
        self.set_position(gtk.WIN_POS_CENTER)
        self.connect('destroy', gtk.main_quit)
        self.set_title('About')

        button = gtk.Button('About')
        button.set_size_request(80, 30)
        button.connect('clicked', self.on_click)

        fix = gtk.Fixed()
        fix.put(button, 20, 20)

        self.add(fix)
        self.show_all()

    def on_click(self, widget):
        about = gtk.AboutDialog()
        about.set_program_name('News-Indicator')
        about.set_comments('Put comments here')
        # about.set_logo(put icon here)
        about.run()
        about.destroy()

    def __repr__(self):
        return self.get_title()


def render_about_window():
    IndicatorABoutWindow()
    gtk.main()