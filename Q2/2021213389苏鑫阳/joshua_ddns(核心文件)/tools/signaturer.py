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


if __name__ == '__main__':
    hmacsha1 = HmacSHA1()
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    urled_timestamp = hmacsha1.encode_url(timestamp)
    accessKeyId = 'LTAI5tGWebwiu5c1ypsf614f'
    accessKey = 'bFuC8bovqACVOTYsemQHWBrTRZBXxg'
    sifnatureNone = str(int(time.time()))
    RRKeyWord = 'www'
    params = {'AccessKeyId': accessKeyId,
              'Action': 'DescribeDomainRecords',
              'DomainName': 'example.com',
              'SignatureMethod': 'HMAC-SHA1',
              'Format': 'JSON',
              'SignatureVersion': '1.0',
              'SignatureNonce': sifnatureNone,
              'Version': '2015-01-09',
              'Timestamp': urled_timestamp,
              'RRKeyWord': RRKeyWord, 'Type': 'A'}

    sorted_dict_to_str = hmacsha1.get_string_to_sign(params)
    signature = hmacsha1.signaturer(accessKey + '&', 'GET&%2F&'+hmacsha1.encode_url(sorted_dict_to_str))
   # print('GET&%2F&'+hmacsha1.url_encode(sorted_dict_to_str))
    #chongxin
    params['Timestamp'] = timestamp
    params['Signature'] = signature

    response = requests.get('https://alidns.aliyuncs.com/', params=params)

    print(response.url)
    print(response.text)
    #print(query_result)



