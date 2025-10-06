import gi
import subprocess
import os

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio

def runCommand(command, capture_output=True, text=True, stdin=False):

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=capture_output,
            text=text,
            check=True,
            stdin=stdin
        )
        output = result.stdout

    except subprocess.CalledProcessError as e:
        output = f"Error executing command: {e}"

    except FileNotFoundError:
        output = f"Error: Command not found."

    return output

@Gtk.Template(filename = "ui.ui")
class MyAppWindow(Gtk.ApplicationWindow):

    __gtype_name__ = "GithubSetup"

    content_box = Gtk.Template.Child()
    countButton = Gtk.Template.Child()

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # Create a popover and attach it to the button
        popover = Gtk.Popover()
        popover.set_has_arrow(True)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.set_margin_top(10)
        box.set_margin_bottom(10)
        box.set_margin_start(10)
        box.set_margin_end(10)

        box.append(Gtk.Label(label="Hello from Popover!"))
        close_button = Gtk.Button(label="Close Popover", halign=Gtk.Align.CENTER)
        close_button.connect("clicked", lambda b: popover.popdown())
        box.append(close_button)

        popover.set_child(box)
        popover.set_parent(self.countButton)

        # Connect signal to show the popover
        self.countButton.connect("clicked", lambda btn: popover.popup())

    @Gtk.Template.Callback()
    def count(self, button):

        output = runCommand('printf "clicked\n" >> $HOME/code/gtk-dev/lines.txt && cat $HOME/code/gtk-dev/lines.txt | wc -l')

        self.countButton.set_label(output)

    @Gtk.Template.Callback()
    def wipe(self, button):
        
        runCommand('printf "" > $HOME/code/gtk-dev/lines.txt', capture_output=False, text=False)

        self.countButton.set_label("0")

    @Gtk.Template.Callback()
    def gitUsername(self, label):
        
        username = runCommand('git config --global user.name')
        label.set_label(username)

    @Gtk.Template.Callback()
    def gitEmail(self, label):
        
        email = runCommand('git config --global user.email')
        label.set_label(email)



class MyApp(Gtk.Application):

    def __init__(self):
        super().__init__(
            application_id="com.pkncoder.githubsetup",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )
        self.builder = None

    def do_activate(self):
        window = MyAppWindow(application = self)
        window.present()

if __name__ == "__main__":
    app = MyApp()
    app.run(None)

