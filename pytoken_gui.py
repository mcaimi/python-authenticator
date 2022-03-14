#!/usr/bin/env python
#
#   Python TOTP Token Generator, GUI
#   v0.1 - Marco Caimi <mcaimi@redhat.com>
#
# global imports
""" Python Authenticator GUI """

import sys
try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk
except ImportError as e:
    print(f"PYOKEN-GTK3, Error importing module [{e}]")
    sys.exit(-1)

# try to load the main window class
try:
    from python_authenticator.gtk.mainwindow import TOTPMainWin
except ImportError:
    print("PYTOKEN-GTK3: Cannot import MainWindow Class")
    sys.exit(-1)

# INSTANTIATE MAIN CLASS
mWin = TOTPMainWin(window_title="PyTOTP")
# CONNECT DESTROY EVENT
mWin.connect('delete-event', Gtk.main_quit)
# SHOW WINDOW
mWin.show_all()

# start main loop
Gtk.main()

# -*- eof -*-
