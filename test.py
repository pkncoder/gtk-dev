import gi

# Specify the GTK version
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # noqa # type: ignore


class MyWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="GTK4 Notebook App")

        # Create a new GtkNotebook
        notebook = Gtk.Notebook()
        self.set_child(notebook)

        # Create the content for the first tab
        page1_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        page1_content.set_margin_top(10)
        page1_content.set_margin_bottom(10)
        page1_content.set_margin_start(10)
        page1_content.set_margin_end(10)
        page1_content.append(Gtk.Label(label="This is the content for Tab 1."))

        # Create the content for the second tab
        page2_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        page2_content.set_margin_top(10)
        page2_content.set_margin_bottom(10)
        page2_content.set_margin_start(10)
        page2_content.set_margin_end(10)
        page2_content.append(Gtk.Label(label="This is the content for Tab 2."))

        # Append the pages to the notebook
        notebook.append_page(page1_content, Gtk.Label(label="Tab 1"))
        notebook.append_page(page2_content, Gtk.Label(label="Tab 2"))


def on_activate(app):
    win = MyWindow(app)
    win.present()


if __name__ == "__main__":
    app = Gtk.Application(application_id="org.gtk.example")
    app.connect("activate", on_activate)
    app.run(None)
