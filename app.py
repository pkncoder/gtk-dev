import gi
import subprocess
import os

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio

@Gtk.Template(filename = "ui.ui")
class MyAppWindow(Gtk.ApplicationWindow):

    __gtype_name__ = "GithubSetup"

    @Gtk.Template.Callback()
    def count(self, button):

        try:
            result = subprocess.run(
                'printf "clicked\n" >> $HOME/code/gtk-dev/lines.txt && cat $HOME/code/gtk-dev/lines.txt | wc -l',
                shell=True,
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

    @Gtk.Template.Callback()
    def wipe(self, button):
        
        try:
            subprocess.run(
                'printf "" > $HOME/code/gtk-dev/lines.txt',
                shell=True,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
        except FileNotFoundError:
            print("Error: Command not found.")

        button.set_label("Click Me")

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

