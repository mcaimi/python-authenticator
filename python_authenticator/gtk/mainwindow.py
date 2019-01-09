#!/bin/env python
#
#   GTK Main Window Implementation
#
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
    from python_authenticator.utils.ConfigParsers import ConfigParams
    # widgets
    from python_authenticator.gtk.tokenelement import TokenElement
except ImportError as e:
    print ("Cannot import library [%s]" % e)
    raise e

# WINDOW SIZE
DEF_WIDTH = 300
DEF_HEIGHT = 300
BORDER_SIZE = 5
PROGRESSBAR_TIMEOUT = 60

# MARKUP TEMPLATE
PANGO_MARKUP_TEMPLATE = "<markup><span foreground='blue' font_desc='Iosevka Term Medium 15'>%s</span>\n<span foreground='black' font_desc='Noto Sans UI 10'>%s</span></markup>"

# MAIN WINDOW
class TOTPMainWin(Gtk.Window):
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
        self.tokens_array = list()
        self.tokenResults = list()
        self.token_labels = list()

        # window appearance
        self.set_border_width(BORDER_SIZE)
        self.set_default_size(DEF_WIDTH, DEF_HEIGHT)

        # header bar
        headBar = Gtk.HeaderBar()
        headBar.set_show_close_button(True)
        headBar.set_title("Python Authenticator")
        self.set_titlebar(headBar)

        # create refresh button
        refButton = Gtk.Button()
        refIcon = Gio.ThemedIcon(name="view-refresh-symbolic")
        iconImage = Gtk.Image.new_from_gicon(refIcon, Gtk.IconSize.BUTTON)
        refButton.add(iconImage)
        refButton.connect('clicked', self.on_refresh_button_click)
        headBar.pack_start(refButton)

        # widget box.
        wBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        Gtk.StyleContext.add_class(wBox.get_style_context(), 'linked')
        wBox.set_homogeneous(False)

        # populate initial list of accounts
        self.__update_token_data()

        # Progress bar
        self.progBar = Gtk.ProgressBar()
        self.progBar.set_text("TOTP Timeout")
        self.progBar.props.show_text = True
        self.timeout_id = GObject.timeout_add(60000/(PROGRESSBAR_TIMEOUT*10), self.on_timeout_event, None)
        wBox.add(self.progBar)

        # Text Area
        self.token_labels = [TokenElement(current_totp) for current_totp in self.tokenResults]
        for label in self.token_labels:
            wBox.pack_start(label, True, True, 0)
        self.__update_label_text()

        # add to window
        self.add(wBox)

    # get a list of all registered accounts on this token server
    def __get_accounts(self):
        # cleanup cache
        self.tokenResults.clear()
        self.tokens_array.clear()
        # get accounts
        self.apiResponse = get(self.token_endpoint, headers={ "Content-Type": "application/json" })
        # generate tokens
        if self.apiResponse.status_code == 200:
            retpayload = self.apiResponse.json()['accounts']
            for account in retpayload.keys():
                postresults = post(self.token_endpoint,
                                    headers={'Content-Type': 'application/json'},
                                    data=json.dumps({
                                            'account_string': account,
                                            'token_type': retpayload[account]['type']
                                            }
                                    ))
                # update global info on tokens
                self.tokenResults.append(postresults.json()['token'])

    # timeout event handler
    def on_timeout_event(self, user_data):
        new_value = self.progBar.get_fraction() + 1/(PROGRESSBAR_TIMEOUT*10)
        if new_value > 1:
            # regenerate tokens
            self.__update_token_data()
            # reset bar
            new_value = 0
        self.progBar.set_fraction(new_value)
        return True

    # refresh button
    def on_refresh_button_click(self, widget):
        self.__update_token_data()

    # generate token data for display purposes
    def __update_token_data(self):
        # get info on accounts and tokens
        self.__get_accounts()
        # parse info and get data back
        for acct in self.tokenResults:
            self.tokens_array.append([acct['account_type'], PANGO_MARKUP_TEMPLATE % (acct['token'], acct['account_string'])])
        # update text in labels
        self.__update_label_text()

    # update token labels
    def __update_label_text(self):
        for label_pos in range(0, len(self.token_labels)):
            self.token_labels[label_pos].set_markup_text(self.tokens_array[label_pos][1])
            self.token_labels[label_pos].set_type(self.tokens_array[label_pos][0])


