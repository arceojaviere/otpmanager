import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from otp.generator import OTPGenerator
from db.otpdb import OtpDatabase
from data.model import Token

import datetime

class MainWindow(Gtk.Window):
  otpGenerator = OTPGenerator()
  otpDatabase = OtpDatabase()
  
  tokenEntry = None
  otpEntry = None

  def __init__(self, title = "OTP Manager"):
    Gtk.Window.__init__(self, title = title)    
    self._addComponents()
    self._token = self.otpDatabase.getTokens()[0]
    self.tokenEntry.set_text(self._token.tokenId)
      


  def _addComponents(self):
    box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,spacing = 6)

    self.tokenEntry = Gtk.Entry(editable = False)
    self.otpEntry = Gtk.Entry(editable = False)
    button = Gtk.Button(label="Generate token")
    button.connect("clicked", self._generateToken)
    
    box.add(self.tokenEntry)
    box.add(self.otpEntry)
    box.add(button)

    self.add(box)  

  def _generateToken(self, widget):
    print "Generating token"
    secret = self._token.secret
    count = self.otpDatabase.nextCount(self._token.tokenId)
    print "Count: " + str(count)
    self.otpEntry.set_text(self.otpGenerator.newHotp(self._token.secret, count))
    

