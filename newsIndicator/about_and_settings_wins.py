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
        # Default notifications state is OFF
        switch.set_active(self.notifications_state)
        switch.connect('state-set', self.on_notification_change, state)
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
        combo.connect('changed', self.on_interval_change, state)
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

    def on_interval_change(self, combo, state):
        self.settings_called = True
        state.intrvl_change_trig = True
        print('Settings changed and value is:{}'.format(self.settings_called))
        # model = combo.get_model()
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
            state.settings_interval = index[:2]
        return self.interval

    def on_notification_change(self, switch, state):
        self.notifications_called = True
        state.notification_change_trig = True

        state = switch.get_state()
        switch.set_state(state)
        self.notifications_state = state

        return self.notifications_state

    def on_apply(self):
        pass

    def on_cancel(self):
        pass

    def __repr__(self):
        return self.get_title()


class SettingsState(object):

    def __init__(self, intrvl_change_trig, settings_interval, ntfc_change_trig, notification_state):
        # Notification switch state variables
        self.notification_change_trig = ntfc_change_trig
        self.notification_state = notification_state
        # Interval dd menu state variables
        self.intrvl_change_trig = intrvl_change_trig
        self.settings_interval = settings_interval

    def get_state(self):
        print ('Interval state now is: {}'.format(self.intrvl_change_trig))
        print ('Interval now is: {}'.format(self.settings_interval))
        print ('Notifications state now is: {}'.format(self.notification_change_trig))
        print ('Notifications are now: {}'.format(self.notification_state))

        return self.intrvl_change_trig, self.settings_interval, self.notification_change_trig, self.notification_state

    def update_state(self, new_settings_instance_trig, new_interval, new_ntfc_instance_trig, new_ntfc_change):
        # Update notification switch state
        self.notification_change_trig = new_ntfc_instance_trig
        self.notification_state = new_ntfc_change
        # Update interval option
        self.intrvl_change_trig = new_settings_instance_trig
        self.settings_interval = new_interval


def render_settings_window(s_called, s_int, ntfc_called, ntfc_state, s_state):
    win = Settings(s_called, s_int, ntfc_called, ntfc_state, s_state)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    print ('in render_settings_window.called is{a} and interval is{b}'.format(a=win.settings_called, b=win.interval))
    return win.settings_called, win.interval, win.notifications_called, win.notifications_state


def render_about_window():
    AboutWindow()
    Gtk.main()
