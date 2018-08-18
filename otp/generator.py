import base64
import hmac
import hashlib
import array
import time
import binascii

class OTPGenerator:

# TODO: Move these to a more general namespace
  ENCODING_BASE32 = 'b32'
  ENCODING_HEX = 'hex'
  ENCODING_RAW = 'raw'

  digits = None
  window = None

  def __init__(self, digits = 6, window = 30):
    self.digits = digits
    self.window = window
  
  def newHotp(self, secret, count, secretEncoding = ENCODING_BASE32, digits = None):

    digits = digits if digits is not None else self.digits

    if secretEncoding == OTPGenerator.ENCODING_BASE32:
      secretBytes = secret + ('=' * (8 - len(secret) % 8))
      secretBytes = base64.b32decode(secretBytes)
    elif secretEncoding == OTPGenerator.ENCODING_HEX:
      secretBytes = binascii.unhexlify(secret)
    elif secretEncoding == OTPGenerator.ENCODING_RAW:
      secretBytes = secret
    else:
      raise "Unrecognized encoding for secret: " + secretEncoding
      
    countBytes = self._longToByteArray(count)
    hmacHash = hmac.new(key = secretBytes, msg = countBytes, digestmod=hashlib.sha1).hexdigest()

    offset = int(hmacHash[-1],16)
    return self._hotpTruncate(hmacHash)[-digits:]
 
  def newTotp(self, secret, secretEncoding = ENCODING_BASE32, digits = None, window = None):
    
    digits = digits if digits is not None else self.digits
    window = window if window is not None else self.window
    
    count = long(time.time() / window)
    return self.newHotp(secret, count, secretEncoding = secretEncoding, digits=digits)
 
 
  def _hotpTruncate(self, hmacHash):
    offset = int(hmacHash[-1], 16)
    binary = int(hmacHash[(offset * 2):((offset * 2) + 8)], 16) & 0x7fffffff
    return str(binary)
 
  def _longToByteArray(self, long_num):
    byte_array = array.array('B')
    for i in reversed(range(0, 8)):
        byte_array.insert(0, long_num & 0xff)
        long_num >>= 8
    return byte_array

