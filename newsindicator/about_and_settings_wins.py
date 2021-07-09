import gi

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')

from gi.repository import Gtk

COMMENT = 'News Indicator is an appindicator that retrieves the latest news articles,' \
          ' on a variety of topics from top media outlets.\n\n\nBuilt with Python and powered by NewsAPI.'

# News retrieval intervals
INTERVALS = {0: '10 Minutes', 1: '15 Minutes', 2: '20 Minutes', 3: '30 Minutes', 4: '60 Minutes'}


class AboutWindow(Gtk.Dialog):
    """
    About window
    """

    def __init__(self):
        # About window constructor
        super(AboutWindow, self).__init__()
        about = Gtk.AboutDialog()
        about.set_program_name('News Indicator')
        about.set_logo_icon_name(None)
        about.set_comments(COMMENT)
        about.set_title('')
        about.connect('response', self.on_close)
        about.show()

    def on_close(self, action, parameter):
        """
        Destroy window on close.
        """
        action.destroy()

    def __repr__(self):
        # object representation
        return self.get_title()


class SettingsState(object):
    """
    Observer A. Based on the Observer pattern it is responsible to hold the current state of the app.
    It models the dependent functionality (notifications & retrieval interval) and is used as a relay to the other
    observer too.
    """

    def __init__(self, intrvl_change_trig, settings_interval, ntfc_change_trig, notification_state):
        # Notification switch state variables
        self.notification_change_trig = ntfc_change_trig
        self.notification_state = notification_state
        # Interval dd menu state variables
        self.intrvl_change_trig = intrvl_change_trig
        self.settings_interval = settings_interval

    def get_state(self):
        # gets the overall state
        return self.intrvl_change_trig, self.settings_interval, self.notification_change_trig, self.notification_state

    def update_state(self, new_settings_instance_trig, new_interval, new_ntfc_instance_trig, new_ntfc_change):
        # Update notification switch state
        self.notification_change_trig = new_ntfc_instance_trig
        self.notification_state = new_ntfc_change
        # Update interval option
        self.intrvl_change_trig = new_settings_instance_trig
        self.settings_interval = new_interval


class Settings(Gtk.ApplicationWindow):
    """
    Observable class,based on the Observer pattern, that renders the settings window.
    It is coupled to the SettingsState class and holds the independent functionality (scheduler).
    """

    def __init__(self, called, interv, ntfc_called, ntfc_state, state):
        # Store the state of the whole Settings window
        self.settings_called = called
        self.interval = interv
        self.notifications_called = ntfc_called
        self.notifications_state = ntfc_state

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
        # Default notifications state is ON
        switch.set_active(self.notifications_state)
        switch.connect('notify::active', self.on_notification_change)
        horizontal_box.pack_start(switch, False, True, 0)

        listbox.add(row)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)

        retrieval_label = Gtk.Label("Retrieval Intervals", xalign=0)

        # Create the main combo-box
        combo = Gtk.ComboBoxText()
        # and populate it
        for key, value in INTERVALS.items():
            combo.insert(key, str(key), value)

        # Default retrieval time is 10 mins
        combo.set_active(self.interval)
        combo.connect('changed', self.on_interval_change, state)
        hbox.pack_start(retrieval_label, True, True, 0)
        hbox.pack_start(combo, False, True, 0)

        listbox.add(row)

    def on_interval_change(self, combo, state):
        """
        Callback function that is fired when the user changes the time interval.
        """
        self.settings_called = True
        state.intrvl_change_trig = True
        index = combo.get_active_text()
        active = combo.get_active()
        if index:
            # Set the new interval
            combo.set_active(active)
            # Get the number of minutes
            self.interval = active
        return self.interval

    def on_notification_change(self, switch, active):
        """
        Callback function that is fired upon changing the notification state (ON/OFF).
        """
        self.notifications_called = True

        state = switch.get_state()
        switch.set_state(state)
        self.notifications_state = state

        return self.notifications_state

    def __repr__(self):
        return self.get_title()


def render_settings_window(s_called, s_int, ntfc_called, ntfc_state, s_state):
    """
    Render the settings window
    """
    win = Settings(s_called, s_int, ntfc_called, ntfc_state, s_state)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    return win.settings_called, win.interval, win.notifications_called, win.notifications_state


def render_about_window():
    """
    Render the about window
    """
    AboutWindow()
    Gtk.main()
