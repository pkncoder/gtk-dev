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
        self.countButton.connect("clicked", self.showModal)

    def showModal(self, button):
        # Create a modal dialog
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text="Are you sure you want to continue?"
        )
        #
        # box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        #
        # # Get the content area and add content
        # label = Gtk.Label(label="This is a modal dialog — like a Bootstrap modal!")
        # label.set_margin_top(12)
        # label.set_margin_bottom(12)
        # box.append(label)
        #
        # # Add a close button
        # close_button = Gtk.Button(label="Close")
        # close_button.connect("clicked", lambda b: dialog.close())
        # box.append(close_button)
        #
        # dialog.set_child(box)

        response = dialog.present()

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

