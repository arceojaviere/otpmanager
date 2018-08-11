import sqlite3
import os
from otpmanager.db.otpdb import OtpDatabaseBackend, OtpDatabaseException
from otpmanager.data.model import Token

class Sqlite3Backend(OtpDatabaseBackend):

  def __init__(self, dbpath = None):
    dbpath = dbpath if dbpath is not None else os.getenv("HOME") + "/.otp-manager/sqlite3"

    if not os.path.exists(dbpath):
      os.makedirs(dbpath)
    self.connection = sqlite3.connect(dbpath + "/otp-manager.db")
    cursor = self.connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS TOKEN (TOKEN_ID VARCHAR(12) PRIMARY KEY, SECRET VARCHAR(512), SECRET_ENCODING CHAR(3), COUNT NUMERIC(10))")

  def persistCount(self, tokenId, count):
    self.connection.execute("UPDATE TOKEN SET COUNT = :count WHERE TOKEN_ID = :tokenId", {"tokenId": tokenId, "count": count})
    self.connection.commit()
  
  def retrieveCount(self, tokenId):
    print "ID: " + tokenId
    cursor = self.connection.execute("SELECT COUNT FROM TOKEN WHERE TOKEN_ID = :tokenId", {"tokenId": tokenId})
    results = cursor.fetchall()    
    print len(results)
    if len(results) != 1:
     raise Sqlite3Exception("Unexpected result set size. Expected exactly one item, got " + str(cursor.rowcount))
    return results[0][0]

  def getTokens(self):
    cursor = self.connection.execute("SELECT TOKEN_ID, SECRET, SECRET_ENCODING FROM TOKEN")
    tokens = []
    for row in cursor.fetchall():
      tokens.append(Token(tokenId = row[0], secret = row[1], secretEncoding = row[2]))
    return tokens

class Sqlite3Exception(OtpDatabaseException):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return "Sqlite3 Error: " + repr(self.value)
