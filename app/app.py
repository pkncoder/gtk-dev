import gi

from helpers.modals import ModalWindow, runCommand

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio  # noqa # type: ignore


@Gtk.Template(filename="app/ui.ui")
class MyAppWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "GithubSetup"

    # Entries
    username = Gtk.Template.Child()
    email = Gtk.Template.Child()

    # Labels
    github_connection_status = Gtk.Template.Child()
    ssh_keys = Gtk.Template.Child()

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

    # TODO: Fix the stalling issue (run in background)
    # TODO: Account for a timeout
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

    # TODO: make this a selectable list
    @Gtk.Template.Callback()
    def fetch_ssh_keys(self, label):
        output = runCommand("ls ~/.ssh/ | grep 'id_'")

        label.set_text(output[0].strip())

    # TODO: Make some checks to see if it is needed to create a key (maybe make a different name for github)
    @Gtk.Template.Callback()
    def create_ssh_key(self, button):
        print("faire")

        runCommand(
            f"ssh-keygen -t ed25519 -C {self.email.get_text().strip()}", input="\n\n\n"
        )

        runCommand('eval "$(ssh-agent -s)"')

        runCommand("ssh-add ~/.ssh/id_ed25519")

    # TODO: Make this use a selected ssh key, instead of the default
    @Gtk.Template.Callback()
    def view_ssh_pub_key(self, button):
        ssh_pub_key = self.fetch_pub_ssh_key()

        ModalWindow(
            "SSH Pub Key",
            ssh_pub_key,
            body='1. Open https://www.github.com\n2. Go to your user account settings\n3. Find "SSH and GPG keys"\n4. Click the "New SSH key" button in the top left of the content area\n5. Give a title about your new ssh key in the "Title" entry (eg. your computer\'s name (eg. johndoe@archlinux))\n6. Paste your public ssh key (above) into the "Key" entry\n7. Click the "Add SSH key" button\n\nI recommend running a test for git connection after with this app!',
        ).showModal(self.get_root())

    def fetch_pub_ssh_key(self):
        return runCommand("cat /home/kia/.ssh/id_ed25519.pub")[0].strip()


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
