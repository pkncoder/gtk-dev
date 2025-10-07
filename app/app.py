import gi

from helpers.helpers import runCommand

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio  # noqa # type: ignore


@Gtk.Template(filename="app/ui.ui")
class MyAppWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "GithubSetup"

    # Entries
    username = Gtk.Template.Child()
    email = Gtk.Template.Child()
    github_connection_status = Gtk.Template.Child()

    # Buttons
    username_save_button = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # Fetch git global configs

    @Gtk.Template.Callback()
    def fetch_git_username(self, entry):
        username = runCommand("git config --global user.name")
        entry.set_text(username[0].strip())

    @Gtk.Template.Callback()
    def fetch_git_email(self, entry):
        email = runCommand("git config --global user.email")
        entry.set_text(email[0].strip())

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

    # TODO: Fix the stalling issue
    @Gtk.Template.Callback()
    def test_git_connection(self, button):
        output = runCommand(
            ["ssh", "-T", "git@github.com", "-o", "BatchMode=yes"],
            shell=False,
            check=False,
        )

        self.github_connection_status.set_text(
            f"The status for Github Connection is: {output[1].find("You've successfully authenticated") != -1}"
        )


class MyApp(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="com.pkncoder.githubsetup",
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )

    def do_activate(self):
        window = MyAppWindow(application=self)
        window.set_focus(None)
        window.present()
