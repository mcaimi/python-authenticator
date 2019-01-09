#!/bin/env python
#
#   TOTP Token GUI widget element
#

try:
    from rfc6238 import totp
    import qrcode
    import gi
    import os
    gi.require_version("Gtk", "3.0")
    gi.require_version("GdkPixbuf", "2.0")
    from gi.repository import Gtk, GdkPixbuf
except ImportError as e:
    raise e

ACCOUNT_TYPES = ['google', 'github', 'amazon', 'protonmail', 'mega']
ASSET_ICONS_PATHS = {
            "relative": "./assets/icons/",
            "system_wide": "/usr/share/python-authenticator/assets/icons/"
        }

# Custom TOTP widget.
class TokenElement(Gtk.EventBox):
    def __init__(self, current_totp):
        # setup token provisioning uri
        self.current_totp = current_totp
        self.provisioning_uri = self.current_totp['provisioning_uri']
        self.qrcode_object = qrcode.QRCode()
        self.qrcode_object.add_data(self.provisioning_uri)

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

        # connect handlers to events
        self.connect('button-press-event', self.__on_regenerate_qrcode_click)

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

    def __on_regenerate_qrcode_click(self, widget, event):
        # compile qrcode
        qrcode_image = self.qrcode_object.make_image()
        # get dimensions
        w, h = qrcode_image.size
        # convert to rgb
        if qrcode_image.mode != 'RGB':
            qrcode_image = qrcode_image.convert('RGB')

        # build a GdkPixbuf object from the qrcode byte data...
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(qrcode_image.tobytes(), GdkPixbuf.Colorspace.RGB, False, 8, w, h, w * 3)
        # create a Gtk Image object and load the pixbuf inside it...
        qrImage = Gtk.Image()
        qrImage.set_from_pixbuf(pixbuf)
        qrImage.show()

        # create a small label...
        label = Gtk.Label()
        label.set_use_markup(False)
        label.set_justify(Gtk.Justification.CENTER)
        label.set_text("TOTP Code for account %s: %s" % (self.current_totp['issuer'], self.current_totp['account']))
        label.show()

        # create a Popug Gtk.Window and display the image to the user.
        popup_win = Gtk.Dialog()
        popup_win.vbox.pack_start(label, False, False, 0)
        popup_win.vbox.pack_start(qrImage, False, False, 0)
        popup_win.add_buttons(Gtk.STOCK_YES,1)
        popup_win.run()
        popup_win.destroy()
