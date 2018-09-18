import gi
gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk,Gdk
#from gi.repository import AppIndicator3

from otpmanager.otp.generator import OTPGenerator
from otpmanager.otp.uri import UriParser
from otpmanager.db.otpdb import OtpDatabase
from otpmanager.data.model import Token


import datetime


class MainWindow(Gtk.Window):
  otpGenerator = OTPGenerator()
  otpDatabase = OtpDatabase()
  
  
  def __init__(self, title = "OTP Manager"):
    Gtk.Window.__init__(self, title = title)    
    self.set_default_size(250,150)
    self._addComponents(self.otpDatabase.getTokens())
    self.show_all()
    self.connect("destroy", Gtk.main_quit)

  def _addComponents(self, tokens):
    topBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 12)
        
    topBox.add(self._createPanelBox())
    
    self._mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 12)
    topBox.add(self._createTokensWindow(tokens))
        
    self.add(topBox)

    
  def _createPanelBox(self):
    panelBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL, spacing = 12)
    self._uriEntry = Gtk.Entry()
    addButton = Gtk.Button(label = "+")
    addButton.connect("clicked", self._addToken)
    panelBox.add(self._uriEntry)
    panelBox.add(addButton)
    return panelBox
    
  def _createTokensWindow(self, tokens):
    scrolledWindow = Gtk.ScrolledWindow()

    windowSize = self.get_default_size()
    scrolledWindow.set_min_content_height(windowSize.height)
    
    for token in tokens:
      self._addTokenBox(token)
    scrolledWindow.add(self._mainBox)
    scrolledWindow.set_vexpand(True)
    
    return scrolledWindow

  def _addTokenBox(self, token):
    box = TokenBox(token, self)
    self._mainBox.add(box)

  def _addToken(self, uri):
    uriParser = UriParser()
    token = uriParser.parseUri(self._uriEntry.get_text())
    self.otpDatabase.addToken(token)
    self._addTokenBox(token)
    self.show_all()


class TokenBox(Gtk.Box):
  
  _tokenEntry = None
  _otpEntry = None
  _token = None  

  _button = None

  def __init__(self, token, otpManager):
    self._token = token
    self.otpManager = otpManager
    Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 6)
    self._addComponents(self._generateToken)
  
  def _addComponents(self, buttonClickedCallback):

    self._tokenEntry = Gtk.Entry(editable = False)
    self._tokenEntry.set_text(self._token.tokenId)

    self._otpEntry = Gtk.Entry(editable = False)

    self._button = Gtk.Button(label="Generate token")
    self._button.connect("clicked", buttonClickedCallback)
    self._clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

    self.add(self._tokenEntry)
    self.add(self._otpEntry)
    self.add(self._button)

    
  def _generateToken(self, widget):
    count = self.otpManager.otpDatabase.nextCount(self._token.tokenId)
    otp = self.otpManager.otpGenerator.newHotp(self._token.secret, count)
    self._clipboard.set_text(otp, -1)
    self._otpEntry.set_text(otp)


class StatusIcon:
  def __init__(self, window):
    
    self._window = window
    
    self.status_icon = Gtk.StatusIcon()
    self.status_icon.set_from_icon_name("gcr-key-pair")

    self.status_icon.connect("activate", self.toggle_window_visibility)
    self.status_icon.connect("popup-menu", self.show_menu)

 
   # create a menu
    self.menu = Gtk.Menu()
 
    # create items for the menu - labels, checkboxes, radio buttons and images are supported:
       
    item = Gtk.MenuItem("Quit")
    item.show()
    item.connect("activate", self.quit)
    self.menu.append(item)
                   
    self.menu.show()
 
#    self.status_icon.set_menu(self.menu)

  def show_menu(self, status_icon, button, activate_time):
    self.menu.popup(None, None, None, Gtk.StatusIcon.position_menu, button, activate_time)

  def toggle_window_visibility(self, status_icon):
    if self._window.is_visible():
      self._window.hide()
    else:
      self._window.show()

  def quit(self, widget, data=None):
    Gtk.main_quit()
