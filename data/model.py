class Token:
  def __init__(self, tokenId = None, secret = None, secretEncoding = None, counter = None):
    self.tokenId = tokenId
    self.secret = secret
    self.secretEncoding = secretEncoding
    self.counter = counter
