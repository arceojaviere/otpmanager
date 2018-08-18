import urlparse
from otpmanager.data.model import Token

class UriParser:
  def parseUri(self, uri):
    token = Token()    

    parsedUri = urlparse.urlparse(uri)
    queryParams = urlparse.parse_qs(parsedUri.query)

    token.tokenId = parsedUri.path[1:]
    token.secret = queryParams["secret"][0]
    token.counter = queryParams["counter"][0]
    
    return token
