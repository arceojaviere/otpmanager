from view.main import MainWindow
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from data.model import Token

window = MainWindow()

window.show()
window.show_all()
window.connect("destroy", Gtk.main_quit)
Gtk.main()
