#!/bin/env python
#
#   GTK Main Window Implementation
#
""" TOTP GTK Client: Main Window """

import json
# import GTK+, requests and local libraries
try:
    # GTK
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, Gio, GObject
    # REQUESTS
    from requests import get, post
    # LOCALS
    from python_authenticator.utils.config_parsers import ConfigParams
    # widgets
    from python_authenticator.gtk.tokenelement import TokenElement
except ImportError as missing_imports:
    raise ImportError(f'Missing imports [{missing_imports.__str__}]') from missing_imports

# WINDOW SIZE
DEF_WIDTH = 300
DEF_HEIGHT = 300
BORDER_SIZE = 5
PROGRESSBAR_TIMEOUT = 30

# MARKUP TEMPLATE
PANGO_MARKUP_TEMPLATE = "<markup><span foreground='blue' font_desc='Iosevka Term Medium 15'>%s</span>\n<span foreground='black' font_desc='Noto Sans UI 10'>%s</span></markup>"


class TOTPMainWin(Gtk.Window):
    ''' Main Window Implementation '''

    API_ENDPOINT_TEMPLATE = "http://%s:%s/%s/"

    def __init__(self, window_title="MainWindow"):
        # open configuration
        self.globalconfig = ConfigParams()
        self.globalconfig.parse()
        self.token_endpoint = TOTPMainWin.API_ENDPOINT_TEMPLATE % (self.globalconfig.apiserver.listen_address,
                                                                   self.globalconfig.apiserver.listen_port,
                                                                   "token")

        # Initialize GTK+ Window Base Class
        Gtk.Window.__init__(self, title=window_title)
        self.tokens_array = []
        self.token_results = []
        self.token_labels = []

        # window appearance
        self.set_border_width(BORDER_SIZE)
        self.set_default_size(DEF_WIDTH, DEF_HEIGHT)

        # header bar
        head_bar = Gtk.HeaderBar()
        head_bar.set_show_close_button(True)
        head_bar.set_title("Python Authenticator")
        self.set_titlebar(head_bar)

        # create refresh button
        refresh_button = Gtk.Button()
        refresh_icon = Gio.ThemedIcon(name="view-refresh-symbolic")
        icon_image = Gtk.Image.new_from_gicon(refresh_icon, Gtk.IconSize.BUTTON)
        refresh_button.add(icon_image)
        refresh_button.connect('clicked', self.on_refresh_button_click)
        head_bar.pack_start(refresh_button)

        # widget box.
        widget_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        Gtk.StyleContext.add_class(widget_box.get_style_context(), 'linked')
        widget_box.set_homogeneous(False)

        # populate initial list of accounts
        self.__update_token_data()

        # Progress bar
        self.progress_bar = Gtk.ProgressBar()
        self.progress_bar.set_text("TOTP Timeout")
        self.progress_bar.props.show_text = True
        self.timeout_id = GObject.timeout_add(30000 / (PROGRESSBAR_TIMEOUT * 10), self.on_timeout_event, None)
        widget_box.add(self.progress_bar)

        # Text Area
        self.token_labels = [TokenElement(current_totp) for current_totp in self.token_results]
        for label in self.token_labels:
            widget_box.pack_start(label, True, True, 0)
        self.__update_label_text()

        # add to window
        self.add(widget_box)

    # get a list of all registered accounts on this token server
    def __get_accounts(self):
        # cleanup cache
        self.token_results.clear()
        self.tokens_array.clear()
        # get accounts
        self.api_response = get(self.token_endpoint, headers={"Content-Type": "application/json"})
        # generate tokens
        if self.api_response.status_code == 200:
            retpayload = self.api_response.json()['accounts']
            for account in retpayload.keys():
                postresults = post(self.token_endpoint,
                                   headers={'Content-Type': 'application/json'},
                                   data=json.dumps({'account_string': account,
                                                    'token_type': retpayload[account]['type']}))
                # update global info on tokens
                if "token" in postresults.json().keys():
                    self.token_results.append(postresults.json().get("token"))

    # timeout event handler
    def on_timeout_event(self, user_data):
        new_value = self.progress_bar.get_fraction() + 1 / (PROGRESSBAR_TIMEOUT * 10)
        if new_value > 1:
            # regenerate tokens
            self.__update_token_data()
            # reset bar
            new_value = 0
        self.progress_bar.set_fraction(new_value)
        return True

    # refresh button
    def on_refresh_button_click(self, widget):
        self.__update_token_data()

    # generate token data for display purposes
    def __update_token_data(self):
        # get info on accounts and tokens
        self.__get_accounts()
        # parse info and get data back
        for acct in self.token_results:
            self.tokens_array.append([acct['account_type'], PANGO_MARKUP_TEMPLATE % (acct['token'], acct['account_string'])])
        # update text in labels
        self.__update_label_text()

    # update token labels
    def __update_label_text(self):
        for label_pos in range(0, len(self.token_labels)):
            self.token_labels[label_pos].set_markup_text(self.tokens_array[label_pos][1])
            self.token_labels[label_pos].set_type(self.tokens_array[label_pos][0])
