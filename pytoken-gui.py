#!/usr/bin/env python
#
#   Python TOTP Token Generator, GUI
#   v0.1 - Marco Caimi <marco.caimi@fastweb.it>
#
# global imports
import sys
try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except ImportError as e:
    print("PTOKEN-GTK3, Error importing module [%s]" % e)
    sys.exit(-1)

from python_authenticator.gtk.mainwindow import TOTPMainWin

# INSTANTIATE MAIN CLASS
mWin = TOTPMainWin(window_title="PyTOTP")
# CONNECT DESTROY EVENT
mWin.connect('delete-event', Gtk.main_quit)
# SHOW WINDOW
mWin.show_all()

# start main loop
Gtk.main()

# -*- eof -*-
