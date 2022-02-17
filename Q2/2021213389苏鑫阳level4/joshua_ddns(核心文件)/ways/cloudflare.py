import json
import logging
import requests


class Cloudflare:
    def __init__(self, option, mode):
        self.option = option
        self.key = option['way'][1]
        self.zone_id = option['way'][2]
        self.key = r'Bearer ' + self.key
        self.headers = {'Authorization': self.key}

        self.hostname = option['hostname'][0]

        if mode == 'ipv4':
            self.ip = option['ipv4_setted']
            self.manager('A', option['a'])
        else:
            self.ip = option['ipv6_setted']
            self.manager('AAAA', option['aaaa'])

    def manager(self, mode, records):
        for record in records:
            hostname = record + '.' + self.hostname
            query_result = self.query_record(hostname, mode)
            if query_result is not None:
                if query_result == ():
                    self.create_record(hostname, self.ip, mode)
                elif query_result[1] != self.ip:
                    self.update_record(hostname, self.ip, mode, query_result[0])

    # 这里的hostname需要包括记录， mode的值为A或AAAA
    def query_record(self, hostname, mode):
        url = 'https://api.cloudflare.com/client/v4/zones/' + self.zone_id + '/dns_records?type=' + mode + '&name=' + hostname + '&order=type&match=all'
        try:
            result = requests.request('GET', url, headers=self.headers, timeout=5)
        except requests.exceptions.ProxyError:
            logging.error('连接本地代理失败，检查本地代理是否正确开启，获取' + hostname + '的dns记录失败')
            return
        except requests.exceptions.ConnectionError:
            logging.error("网络异常，获取" + hostname + "的dns记录失败，请检查本地网络是否可能,或是可能未正确开启代理")
            return
        except requests.exceptions.Timeout:
            logging.error('等待服务器响应超时，获取' + hostname + '的dns记录失败')
            return


        mjson = json.loads(result.text)
        if mjson['success'] == False:
            logging.error('record查询阶段数据有误，可能是所给cloudflare api令牌或zone id输入有误或服务器故障，详细返回值如下：')
            logging.error(mjson)
            return
        elif len(mjson['result']) == 0:
            return ()
        else:
            return mjson['result'][0]['id'], mjson['result'][0]['content']

    # mode A或AAAA hostname包括域名加记录
    def create_record(self, hostname, ip, mode):
        url = r'https://api.cloudflare.com/client/v4/zones/' + self.zone_id + '/dns_records'
        payload = '{"type":"' + mode + '","name":"' + hostname + '","content":"' + ip + '","ttl":1,"proxied":false}'

        try:
            result = requests.request('POST', url, data=payload, headers=self.headers, timeout=5)
        except requests.exceptions.ProxyError:
            logging.error('连接本地代理失败，检查本地代理是否正确开启，创建' + hostname + '的dns记录失败')
            return
        except requests.exceptions.ConnectionError:
            logging.error("网络异常，创建" + hostname + "的dns记录失败，请检查本地网络是否可能,或是可能未正确开启代理")
            return
        except requests.exceptions.Timeout:
            logging.error('等待服务器响应超时，创建' + hostname + '的dns记录失败')
            return


        mjson = json.loads(result.text)
        if mjson['success'] == False:
            print('创建dns记录阶段数据有误，可能是重复创建了dns记录或服务器故障，详细返回值如下：')
            print(mjson)
            return
        else:
            return mjson

    # dns_id表示对那个dns记录进行更改， mode接收A或AAAA参数，hostname包括记录
    def update_record(self, hostname, ip, mode, dns_id):
        url = r'https://api.cloudflare.com/client/v4/zones/' + self.zone_id + '/dns_records/' + dns_id
        payload = '{"type":"' + mode + '","name":"' + hostname + '","content":"' + ip + '","ttl":1,"proxied":false}'
        try:
            result = requests.request('PUT', url, data=payload, headers=self.headers, timeout=5)
        except requests.exceptions.ProxyError:
            logging.error('连接本地代理失败，检查本地代理是否正确开启，更新' + hostname + '的dns记录失败')
            return
        except requests.exceptions.ConnectionError:
            logging.error("网络异常，更新" + hostname + "的dns记录失败，请检查本地网络是否可能,或是可能未正确开启代理")
            return
        except requests.exceptions.Timeout:
            logging.error('等待服务器响应超时，更新' + hostname + '的dns记录失败')
            return


        mjson = json.loads(result.text)
        if mjson['success'] == False:
            print('更新dns记录阶段数据有误，可能是重复创建了dns记录或服务器故障，详细返回值如下：')
            print(mjson)
            return
        else:
            return mjson
