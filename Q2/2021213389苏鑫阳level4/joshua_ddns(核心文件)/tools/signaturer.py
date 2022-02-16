import base64
import hmac
import hashlib
import time
from urllib import parse
import requests

class HmacSHA1:

    def get_string_to_sign(self, params:dict, method:str, endpoint:str) -> str:
        s = method + endpoint + "/?"
        query_str = "&".join("%s=%s" % (k, params[k]) for k in sorted(params))
        return s+query_str

    def signaturer(self, key: str, code: str) -> str:
        hash = hmac.new(key.encode('utf-8'), code.encode('utf-8'), hashlib.sha1).digest()
        return base64.b64encode(hash).decode('utf-8')

    def encode_url(self, url_str: str):
        return parse.quote(url_str, safe='')



