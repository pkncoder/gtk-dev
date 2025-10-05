import gi
import subprocess
import os

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio

@Gtk.Template(filename = "appUI.ui")
class MyAppWindow(Gtk.ApplicationWindow):

    __gtype_name__ = "GithubSetup"

    @Gtk.Template.Callback()
    def on_button_clicked(self, button):

        try:
            result = subprocess.run(
                'echo "clicked" >> /home/kia/code/gtk-dev/lines.txt && cat /home/kia/code/gtk-dev/lines.txt | wc -l',
                capture_output=True,
                text=True,
                check=True
            )
            output = result.stdout
        except subprocess.CalledProcessError as e:
            output = f"Error executing command: {e}"
        except FileNotFoundError:
            output = f"Error: Command not found."

        button.set_label(output)

        print("Clicked!")

class MyApp(Gtk.Application):

    def __init__(self):
        super().__init__(
            application_id="com.pkncoder.githubsetup",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )
        self.builder = None

    def do_activate(self):

        # if not self.builder:
        #     self.builder = Gtk.Builder()
        #     self.builder.add_from_file("appUI.ui")
        #     self.builder.connect_signals(self)

        window = MyAppWindow(application = self)
        window.present()

if __name__ == "__main__":
    app = MyApp()
    app.run(None)



# import gi
# gi.require_version("Gtk", "4.0")
# from gi.repository import Gtk, GLib
#
# class MyApp(Gtk.Application):
#     def __init__(self):
#         super().__init__(application_id="com.example.MyApp",
#                          flags=GLib.ApplicationFlags.FLAGS_NONE)
#         self.builder = None
#
#     def do_activate(self):
#         if not self.builder:
#             self.builder = Gtk.Builder()
#             self.builder.add_from_file("my_app.ui")
#             self.builder.connect_signals(self)
#
#         window = self.builder.get_object("main_window")
#         window.set_application(self)
#         window.present()
#
#     def on_button_clicked(self, button):
#         label = self.builder.get_object("my_label")
#         label.set_label("Button clicked!")
#
# if __name__ == "__main__":
#     app = MyApp()
#     app.run(None)
