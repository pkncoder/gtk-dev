import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class MyDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="My Dialog", transient_for=parent, modal=True)

        # Add buttons
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)

        box = Gtk.Box()

        text = Gtk.Label(label="Get 100000000 Free Robux!!!!!")
        box.append(text)
        self.get_child().append(box)

        

        # Connect the response signal to a handler
        self.connect("response", self.on_response)

    def on_response(self, dialog, response_id):
        if response_id == Gtk.ResponseType.OK:
            print("OK button pressed")
        elif response_id == Gtk.ResponseType.CANCEL:
            print("Cancel button pressed")
        self.destroy()

class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Main Window")
        self.set_default_size(400, 300)

        button = Gtk.Button(label="Open Dialog")
        button.connect("clicked", self.on_open_dialog_clicked)
        self.set_child(button)

    def on_open_dialog_clicked(self, button):
        dialog = MyDialog(self)
        dialog.present()

def on_activate(app):
    win = MyWindow(app)
    win.present()

app = Gtk.Application(application_id="org.example.MyApplication")
app.connect("activate", on_activate)
app.run(None)
