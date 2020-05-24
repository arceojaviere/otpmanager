#!/usr/bin/python
from otpmanager.view.mainview import MainWindow
from otpmanager.view.mainview import StatusIcon

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from data.model import Token


window = MainWindow()
status_icon = StatusIcon(window)

window.show()

Gtk.main()
