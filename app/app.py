import gi

from helpers.helpers import runCommand

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio  # noqa # type: ignore


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


@Gtk.Template(filename="app/ui.ui")
class MyAppWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "GithubSetup"

    # Entries
    username = Gtk.Template.Child()
    email = Gtk.Template.Child()

    # Buttons
    username_save_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.username_save_button.grab_focus()

    # Fetch git global configs

    @Gtk.Template.Callback()
    def fetch_git_username(self, entry):
        username = runCommand("git config --global user.name")
        entry.set_text(username.strip())

    @Gtk.Template.Callback()
    def fetch_git_email(self, entry):
        email = runCommand("git config --global user.email")
        entry.set_text(email.strip())

    # Save git global configs

    @Gtk.Template.Callback()
    def save_git_username(self, button):
        runCommand(
            f"git config --global user.name {self.username.get_text()}",
            capture_output=False,
            text=False,
        )

    @Gtk.Template.Callback()
    def save_git_email(self, button):
        runCommand(
            f"git config --global user.email {self.email.get_text()}",
            capture_output=False,
            text=False,
        )


class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="com.pkncoder.githubsetup",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )
        self.builder = None

    def do_activate(self):
        window = MyAppWindow(application=self)
        window.set_focus(None)
        window.present()


if __name__ == "__main__":
    app = MyApp()
    app.run(None)
