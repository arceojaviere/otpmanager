import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from otpmanager.otp.generator import OTPGenerator
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

  def _addComponents(self, tokens):
    scrolledWindow = Gtk.ScrolledWindow()
    mainBox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 12)
    for token in tokens:
      box = TokenBox(token, self._generateToken)
      mainBox.add(box)
    scrolledWindow.add(mainBox)
    self.add(scrolledWindow)

  def _generateToken(self, widget):
    print "Generating token"
    box = widget.get_parent()
    token = box.getToken()
    count = self.otpDatabase.nextCount(token.tokenId)
    print "Count: " + str(count)
    box.setOtp(self.otpGenerator.newHotp(token.secret, count))
    

class TokenBox(Gtk.Box):
  
  _tokenEntry = None
  _otpEntry = None
  _token = None  

  _button = None

  def __init__(self, token, buttonClickedCallback):
    self._token = token
    Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL, spacing = 6)
    self._addComponents(buttonClickedCallback)
  
  def _addComponents(self, buttonClickedCallback):

    self._tokenEntry = Gtk.Entry(editable = False)
    self._tokenEntry.set_text(self._token.tokenId)

    self._otpEntry = Gtk.Entry(editable = False)

    self._button = Gtk.Button(label="Generate token")
    self._button.connect("clicked", buttonClickedCallback)

    self.add(self._tokenEntry)
    self.add(self._otpEntry)
    self.add(self._button)

  def getToken(self):
    return self._token

  def setOtp(self, otp):
    self._otpEntry.set_text(otp)
    
