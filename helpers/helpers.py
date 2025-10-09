import gi
import subprocess

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # noqa # type: ignore


# TODO: Use Gio.HANDELS_COMMAND_LINE proporley
def runCommand(
    command, shell=True, capture_output=True, text=True, check=True, input=""
):
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=capture_output,
            text=text,
            check=check,
            input=input,
        )
        output = [result.stdout, result.stderr, result.returncode]

    except subprocess.CalledProcessError as e:
        output = [f"Error executing command: {e}", "", ""]

    except FileNotFoundError:
        output = ["Error: Command not found.", "", ""]

    return output


class ModalWindow(Gtk.Dialog):
    title = ""
    text = ""

    def __init__(self, title, text):
        super().__init__()

        self.title = title
        self.text = text

    def showModal(self):
        # Create dialog with proper transient parent
        dialog = Gtk.Dialog(
            title=self.title,
            transient_for=self,
            modal=True,
        )
        dialog.set_default_size(360, -1)

        # --- Header bar (modern button placement) ---
        headerbar = Gtk.HeaderBar()
        headerbar.set_show_title_buttons(False)
        dialog.set_titlebar(headerbar)

        cancel_button = Gtk.Button(label="Cancel")
        ok_button = Gtk.Button(label="OK", css_classes=["suggested-action"])

        headerbar.pack_start(cancel_button)
        headerbar.pack_end(ok_button)

        # --- Content area styled like Gtk.MessageDialog ---
        content_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
            margin_top=16,
            margin_bottom=16,
            margin_start=16,
            margin_end=16,
        )

        # Right side of dialog: label + entry field
        text_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL, spacing=8, hexpand=True
        )
        entry = Gtk.Entry()
        entry.set_text(self.text)

        text_box.append(entry)
        content_box.append(text_box)

        dialog.set_child(content_box)

        # --- Signal connections ---
        cancel_button.connect("clicked", lambda *_: dialog.destroy())
        ok_button.connect("clicked", lambda *_: dialog.destroy())
        entry.connect("activate", lambda *_: dialog.destroy())

        dialog.present()


# TODO: Make this inherit ModalWindow for a better workflow
class CommandModalWindow(Gtk.Dialog):
    title = ""
    text = ""
    placeholder = ""
    command = ""

    def __init__(self, title, text, placeholder, command):
        super().__init__()

        self.title = title
        self.text = text
        self.placeholder = placeholder
        self.command = command

    def showModal(self):
        # Create dialog with proper transient parent
        dialog = Gtk.Dialog(
            title=self.title,
            transient_for=self,
            modal=True,
        )
        dialog.set_default_size(360, -1)

        # --- Header bar (modern button placement) ---
        headerbar = Gtk.HeaderBar()
        headerbar.set_show_title_buttons(False)
        dialog.set_titlebar(headerbar)

        cancel_button = Gtk.Button(label="Cancel")
        ok_button = Gtk.Button(label="OK", css_classes=["suggested-action"])

        headerbar.pack_start(cancel_button)
        headerbar.pack_end(ok_button)

        # --- Content area styled like Gtk.MessageDialog ---
        content_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
            margin_top=16,
            margin_bottom=16,
            margin_start=16,
            margin_end=16,
        )

        # Right side of dialog: label + entry field
        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        label = Gtk.Label(label=self.text, wrap=True, xalign=0)
        entry = Gtk.Entry(placeholder_text=self.placeholder)

        text_box.append(label)
        text_box.append(entry)
        content_box.append(text_box)

        dialog.set_child(content_box)

        # --- Signal connections ---
        cancel_button.connect("clicked", lambda *_: dialog.destroy())
        ok_button.connect("clicked", lambda *_: self.on_dialog_ok(dialog, entry))
        entry.connect("activate", lambda *_: self.on_dialog_ok(dialog, entry))

        dialog.present()

    def on_dialog_ok(self, dialog, entry):
        text = entry.get_text().strip()

        if entry == "":
            print("User entered nothing")
        else:
            runCommand(self.command.replace("{user_output}", text))

        dialog.destroy()
