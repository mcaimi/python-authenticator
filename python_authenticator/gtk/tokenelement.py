#!/bin/env python
#
#   TOTP Token GUI widget element
#

try:
    import gi
    import os
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except ImportError as e:
    raise e

ACCOUNT_TYPES = ['google', 'github', 'amazon']
ASSET_ICONS_PATHS = {
            "relative": "./assets/icons/",
            "system_wide": "/usr/share/python-authenticator/assets/icons/"
        }

# Custom TOTP widget.
class TokenElement(Gtk.EventBox):
    def __init__(self):
        super().__init__()
        # build custom widget
        self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.asset_dir = ASSET_ICONS_PATHS['relative'] if os.path.isdir(ASSET_ICONS_PATHS['relative']) else ASSET_ICONS_PATHS['system_wide']

        # Token Label
        self.token_label = Gtk.Label()
        self.token_label.set_use_markup(True)
        self.token_label.set_justify(Gtk.Justification.LEFT)
        self.token_label.set_xalign(0.0)
        self.hbox.pack_start(self.token_label, False, False, 0)

        # add box to widget
        self.add(self.hbox)

    def set_type(self, account_type):
        # load account icon
        if account_type in ACCOUNT_TYPES: # we have custom icon
            self.icon_pixmap = Gtk.Image.new_from_file(self.asset_dir + account_type + ".png")
        else: # load default icon
            self.icon_pixmap = Gtk.Image.new_from_file(self.asset_dir + "default.png")

        self.hbox.pack_end(self.icon_pixmap, False, False, 0)

    def set_markup_text(self, text):
        self.token_label.set_markup(text)

    def get_markup_text(self):
        return self.token_label.get_markup()
