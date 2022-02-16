import json
import logging
import time
import requests

from tools import signaturer


#Notice: 由于我没有域名托管在阿里云，所以没法测试，不保证能用
#如果真想用，照这官方api https://help.aliyun.com/document_detail/29771.html改改吧
#其实大方向是对的，可能就在返回的数据处理上会有点问题
class AliYun:
    def __init__(self, option, mode):
        self.hmac_sha1 = signaturer.HmacSHA1()
        self.option = option
        self.access_key = option['way'][1]
        self.access_key_id = option['way'][2]

        self.domain = option['hostname'][0]

        if mode == 'ipv4':
            self.ip = option['ipv4_setted']
            self.manager('A', option['a'])
        else:
            self.ip = option['ipv6_setted']
            self.manager('AAAA', option['aaaa'])

    def manager(self, mode, records):
        for record in records:
            query_result = self.query_record(self.domain, record, mode)
            if query_result is not None:
                if query_result == ():
                    self.create_record(self.domain, record, mode, self.ip)
                elif query_result[0] != self.ip:
                    self.update_record(self.domain, record, mode, self.ip, query_result[1])
                else:
                    logging.info(record+'的'+mode+'记录与云端一致，本次不更新')


    # record_type支持参数'A'|'AAAA'
    def query_record(self, domain, subdomain, record_type):
        endpoint = 'alidns.aliyuncs.com'

        # api查询参数，api文档:https://help.aliyun.com/document_detail/29776.html
        private_params = {
            'Action': 'DescribeDomainRecords',
            'DomainName': domain,
            'RRKeyWord': subdomain,
            'Type': record_type,
        }
        try:
            response_txt = self.sign_and_send(endpoint, private_params, 'GET')
        except requests.exceptions.ProxyError:
            logging.error('连接本地代理失败，检查本地代理是否正确开启，获取' + subdomain + '的dns记录失败')
            return
        except requests.exceptions.ConnectionError:
            logging.error("网络异常，获取" + subdomain + "的dns记录失败，请检查本地网络是否可能,或是可能未正确开启代理")
            return
        except requests.exceptions.Timeout:
            logging.error('等待服务器响应超时，获取' + subdomain + '的dns记录失败')
            return

        mjson = json.loads(response_txt)
        response = mjson['Response']
        if 'Error' in response and 'RecordList' not in response:
            error_code = response['Error']['Code']
            if error_code == 'AuthFailure.SignatureFailure':
                logging.error('record查询阶段失败，系所给tencentCloud的secret_key或secret_key_id有误')
                return
            elif error_code == 'ResourceNotFound.NoDataOfRecord':
                logging.warning(subdomain + '在' + domain + '中的已有记录中未查询到，自动在此域名中新建' + subdomain + '记录')
                return ()
            else:
                logging.error(
                    'record查询阶段数据有误，请查阅阿里云文档的错误代码https://error-center.aliyun.com/status/product/Alidns?spm=a2c4g.11186623.0.0.25947a8cNhM4Eh，详细返回值如下：')
                logging.error(mjson)
                return
        else:
            return response['RecordList'][0]['Value'], response['RecordList'][0]['RecordId']


    def create_record(self, domain, subdomain, record_type, ip):
        endpoint = 'alidns.aliyuncs.com'

        # api查询参数，api文档:https://help.aliyun.com/document_detail/29772.html
        params = {
            'Action': 'CreateRecord',
            'Domain': domain,
            'SubDomain': subdomain,
            'RecordType': record_type,
            'RecordLine': '默认',
            'Value': ip,
            'SecretId': self.access_key_id,
        }
        try:
            response_txt = self.sign_and_send(endpoint, params, 'GET')
        except requests.exceptions.ProxyError:
            logging.error('连接本地代理失败，检查本地代理是否正确开启，创建' + subdomain + '的record记录失败')
            return

        except requests.exceptions.ConnectionError:
            logging.error("网络异常，创建" + subdomain + "的record记录失败，请检查本地网络是否可能,或是可能未正确开启代理")
            return
        except requests.exceptions.Timeout:
            logging.error('等待服务器响应超时，创建' + subdomain + '的record记录失败')
            return

        mjson = json.loads(response_txt)
        response = mjson['Response']
        if 'RecordId' not in response:
            logging.error('record创建阶段数据有误，请参阅阿里云文档https://error-center.aliyun.com/status/product/Alidns?spm=a2c4g.11186623.0.0.25947a8cNhM4Eh对错误码的描述，详细返回值如下：')
            logging.error(mjson)
            return
        else:
            logging.info(subdomain+'的'+record_type+'更新成功')
            return response


    def update_record(self, domain, subdomain, record_type, ip, domain_id):
        endpoint = 'alidns.aliyuncs.com'

        # api查询参数，api文档:https://help.aliyun.com/document_detail/29774.html
        params = {
            'Action': 'ModifyRecord',
            'Domain': domain,
            "DomainId": domain_id,
            'SubDomain': subdomain,
            'RecordType': record_type,
            'Value': ip,
        }
        try:
            response_txt = self.sign_and_send(endpoint, params, 'GET')
        except requests.exceptions.ProxyError:
            logging.error('连接本地代理失败，检查本地代理是否正确开启，更新' + subdomain + '的record记录失败')
            return
        except requests.exceptions.ConnectionError:
            logging.error("网络异常，更新" + subdomain + "的record记录失败，请检查本地网络是否可能,或是可能未正确开启代理")
            return
        except requests.exceptions.Timeout:
            logging.error('等待服务器响应超时，更新' + subdomain + '的record记录失败')
            return
        mjson = json.loads(response_txt)
        response = mjson['Response']
        if 'RecordId' not in response:
            logging.error(
                'record更新阶段数据有误，请参阅阿里云文档https://error-center.aliyun.com/status/product/Alidns?spm=a2c4g.11186623.0.0.25947a8cNhM4Eh对错误码的描述，详细返回值如下：')
            logging.error(mjson)
            return
        else:
            logging.info(subdomain+'的'+record_type+'更新成功')
            return response

    def sign_and_send(self, url, params, method: str):
        #下面添加公共参数，文档在这https://help.aliyun.com/document_detail/29745.html
        params['Format'] = 'JSON'
        params['Version'] = '2015-01-09'
        params['AccessKeyId'] = self.access_key_id
        params['SignatureMethod'] = 'HMAC-SHA1'

        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        urled_timestamp = self.hmac_sha1.encode_url(timestamp)

        params['Timestamp'] = urled_timestamp
        params['SignatureVersion'] = '1.0'
        params['SignatureNonce'] = urled_timestamp

        string_to_sign = self.hmac_sha1.get_string_to_sign(params, method, url)
        signature = self.hmac_sha1.signaturer(self.access_key, string_to_sign)
        params['Signature'] = signature
        params['TimeStamp'] = timestamp

        url = 'https://' + url

        response = requests.request(method, url, params=params)
        return response.text
