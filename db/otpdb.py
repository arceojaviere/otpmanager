from abc import ABCMeta, abstractmethod
from data.model import Token

class OtpDatabase:
 
  def __init__(self, module = "db.sqlite3db", clazz = "Sqlite3Backend"):
    mod = __import__(module, fromlist = [clazz])
    self._clazz = getattr(mod, clazz)
    self._backend = self._clazz()

  def nextCount(self,tokenId):
    count = self._backend.retrieveCount(tokenId)
    count += 1
    self._backend.persistCount(tokenId, count)
    return count

  def getTokens(self):
    return self._backend.getTokens()
    
  
class OtpDatabaseBackend:
  __metaclass__ = ABCMeta
  
  @abstractmethod
  def persistCount(self, tokenId, count):
    pass
  
  @abstractmethod
  def retrieveCount(self, tokenId):
    pass   

  @abstractmethod
  def getTokens(self, tokenId):
    pass   


class OtpDatabaseException(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return "OTP Database Error: " + repr(self.value)
