from .helpers import runCommand

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk  # noqa # type: ignore


class ModalWindow(Gtk.Dialog):
    title = ""
    text = ""
    body = None

    def __init__(self, title, text, body=None):
        super().__init__()

        self.title = title
        self.text = text
        self.body = body

    def createDialogWindow(self, parent):
        # Create dialog with proper transient parent
        dialog = Gtk.Dialog(
            title=self.title,
            transient_for=parent,
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

        return dialog, cancel_button, ok_button

    def showModal(self, parent):
        dialog, cancel_button, ok_button = self.createDialogWindow(parent)

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
        label = Gtk.Label()
        label.set_selectable(True)
        label.set_text(self.text)

        text_box.append(label)

        if self.body is not None:
            body = Gtk.Label()

            body.set_wrap_mode(True)
            body.set_text(self.body)

            text_box.append(body)

        content_box.append(text_box)

        dialog.set_child(content_box)

        # --- Signal connections ---
        cancel_button.connect("clicked", lambda *_: dialog.destroy())
        ok_button.connect("clicked", lambda *_: dialog.destroy())

        dialog.present()


class CommandModalWindow(ModalWindow):
    placeholder = ""
    command = ""

    def __init__(self, title, text, placeholder, command, body=None):
        super().__init__(title=title, text=text, body=body)

        self.placeholder = placeholder
        self.command = command

    def showModal(self, parent):
        dialog, cancel_button, ok_button = self.createDialogWindow(parent)

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
