import gi
import sys

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import GObject, Gtk

COMMENT = 'News_Indicator is an applet indicator for Linux systems that retrieves the latest news articles,' \
          ' on a variety of topics from top media outlets.\n\n\nBuilt with Python and powered by NewsAPI.'


class AboutWindow(Gtk.Window):

    def __init__(self):
        super(AboutWindow, self).__init__()
        about = Gtk.AboutDialog()
        about.set_program_name('News_Indicator')
        about.set_comments(COMMENT)
        # about.set_logo(put icon here)
        about.run()
        about.destroy()

    def __repr__(self):
        return self.get_title()
    

class Settings(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Settings")
        self.set_size_request(300, 200)
        self.set_border_width(10)

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_outer)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        horizontal_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(horizontal_box)
        vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        horizontal_box.pack_start(vertical_box, True, True, 0)

        label1 = Gtk.Label("Enable Notifications", xalign=0)
        vertical_box.pack_start(label1, True, True, 0)
        
        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER
        horizontal_box.pack_start(switch, False, True, 0)

        listbox.add(row)        

    def __repr__(self):
        return self.get_title()


def render_settings_window():
    win = Settings()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()


def render_about_window():
    AboutWindow()
    Gtk.main()
