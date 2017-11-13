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
        # about.set_logo(put icon here) # TODO-me:Here
        about.run()
        about.destroy()

    def __repr__(self):
        return self.get_title()
    

class Settings(Gtk.Window):

    def __init__(self, called, interv, state):
        self.interval = interv
        self.settings_called = called
        Gtk.Window.__init__(self, title="Settings")
        self.set_size_request(300, 200)
        self.set_border_width(10)

        # Create the outer box
        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(box_outer)

        # and then the main List box
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        horizontal_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(horizontal_box)
        vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        horizontal_box.pack_start(vertical_box, True, True, 0)

        # Create the Notification label
        notification_label = Gtk.Label("Enable Notifications", xalign=0)
        vertical_box.pack_start(notification_label, True, True, 0)

        # and its switch
        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER
        horizontal_box.pack_start(switch, False, True, 0)

        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)

        retrieval_label = Gtk.Label("Retrieval Intervals", xalign=0)

        # Create the main combo-box
        combo = Gtk.ComboBoxText()
        combo.insert(0, "0", "10 Mins")  
        combo.insert(1, "1", "15 Mins")
        combo.insert(2, "2", "20 Mins")
        combo.insert(3, "3", "30 Mins")
        combo.insert(4, "4", "60 Mins")
        # Default retrieval time is 10 mins
        combo.set_active(self.interval)
        combo.connect('changed', self.on_change, state)
        hbox.pack_start(retrieval_label, True, True, 0)
        hbox.pack_start(combo, False, True, 0)

        listbox.add(row)

        # Create the apply & select buttons and place them on the lower right corner
        self.fixed = Gtk.Fixed()
        listbox.add(self.fixed)
        self.fixed.show()
        apply_button = Gtk.Button("Apply")
        cancel_button = Gtk.Button("Cancel")
        self.fixed.put(apply_button, 140, 95)
        self.fixed.put(cancel_button, 200, 95)

        # add event listeners for each button
        apply_button.connect('activate', self.on_apply)
        cancel_button.connect('activate', self.on_cancel)

    def on_change(self, combo, state):
        self.settings_called = True
        state.set_called = True
        print('Settings changed and value is:{}'.format(self.settings_called))
        model = combo.get_model()
        index = combo.get_active_text()
        active = combo.get_active()
        print('Model is:')
        print (active)
        if index:
            combo.set_active(active)
            # Get the number of minutes
            print('Number of minutes selected:')
            print index[:2]
            self.interval = active
            state.set_interv = index[:2]
        return self.interval

    def on_apply(self):
        pass

    def on_cancel(self):
        pass

    def __repr__(self):
        return self.get_title()


class SettingsState(object):

    def __init__(self, set_called, set_interv):
        self.set_called = set_called
        self.set_interv = set_interv

    def get_state(self):
        print ('State now is: {}'.format(self.set_called))
        print ('Interval now is: {}'.format(self.set_interv))

        return self.set_called, self.set_interv

    def update_state(self, new_called, new_interv):
        self.set_called = new_called
        self.set_interv = new_interv


def render_settings_window(s_called, s_int, s_state):
    win = Settings(s_called, s_int, s_state)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    print ('in render_settings_window.called is{a} and interval is{b}'.format(a=win.settings_called, b=win.interval))
    return win.settings_called, win.interval


def render_about_window():
    AboutWindow()
    Gtk.main()
