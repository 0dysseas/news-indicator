import gi
import sys

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import GObject, Gtk


class AboutWindow(Gtk.Window):

    def __init__(self):
        super(AboutWindow, self).__init__()
        about = Gtk.AboutDialog()
        about.set_program_name('News-Indicator')
        about.set_comments('Put comments here')
        # about.set_logo(put icon here)
        about.run()
        about.destroy()

    def __repr__(self):
        return self.get_title()


class SettingsWindow(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Settings", application=app)
        self.set_default_size(250, 200)
        self.set_border_width(10)

        button = Gtk.CheckButton()
        button.set_label("Notifications")
        button.connect("toggled", self.on_toggle)
        # by default the check button is false
        button.set_active(False)

        self.add(button)

    def on_toggle(self, button):
        if button.get_active():
           #Enable notifications
            pass
        else:
            #Disable notifications
            pass


class SettingsWindowParent(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        window = SettingsWindow(self)
        window.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


def render_settings_window():
    app = SettingsWindowParent()
    # Gtk.main()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)


def render_about_window():
    AboutWindow()
    Gtk.main()
