import gi
import sys

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import GObject, Gtk

COMMENT = 'News_Indicator is an appindicator that retrieves the latest news articles,' \
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
        self.interval = None
        self.settings_called = False
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

        notification_label = Gtk.Label("Enable Notifications", xalign=0)
        vertical_box.pack_start(notification_label, True, True, 0)
        
        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER
        horizontal_box.pack_start(switch, False, True, 0)

        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)

        retrieval_label = Gtk.Label("Retrieval Intervals", xalign=0)

        combo = Gtk.ComboBoxText()
        combo.insert(0, "0", "10 Mins")  
        combo.insert(1, "1", "15 Mins")
        combo.insert(2, "2", "20 Mins")
        combo.insert(3, "3", "30 Mins")
        combo.insert(4, "4", "60 Mins")
        # Default retrieval time is 10 mins
        # combo.set_active(0)
        combo.connect('changed', self.on_change)
        hbox.pack_start(retrieval_label, True, True, 0)
        hbox.pack_start(combo, False, True, 0)

        listbox.add(row)

        self.fixed = Gtk.Fixed()
        listbox.add(self.fixed)
        self.fixed.show()
        apply_button = Gtk.Button("Apply")
        cancel_button = Gtk.Button("Cancel")
        self.fixed.put(apply_button, 140, 95)
        self.fixed.put(cancel_button, 200, 95)

    def on_change(self, combo):
        self.settings_called = True
        print('Settings changed and value is:{}'.format(self.settings_called))
        model = combo.get_model()
        index = combo.get_active_text()
        if index:
            # Get the number of minutes
            print('Number of minutes selected:')
            print index[:2]
            self.interval = index[:2]
            print (self.interval)
        return self.interval

    def on_button1_clicked(self):
        pass

    def __repr__(self):
        return self.get_title()


def render_settings_window():
    win = Settings()
    win.connect("delete-event", Gtk.main_quit)
    # print ('In render_seetings, wind is {}'.format(id(wind)))
    win.show_all()
    Gtk.main()
    print ('in render_settings_window.called is{a} and interval is{b}'.format(a=win.settings_called, b=win.interval))
    return win.settings_called, win.interval


# def create_overall_settings_window():
#     win = Settings()
#     # win.connect("delete-event", Gtk.main_quit)
#     print ('Windows id is {}'.format(id(win)))
#     return win


def render_about_window():
    AboutWindow()
    Gtk.main()
