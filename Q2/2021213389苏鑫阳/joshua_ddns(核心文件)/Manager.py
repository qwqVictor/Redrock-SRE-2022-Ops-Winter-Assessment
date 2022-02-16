import logging
import Option
from tools import GetIP
from ways.cloudflare import Cloudflare
from ways.tencnetCloud import TencentCloud
from ways.aliyun import AliYun

import exception


class Manager:

    def __init__(self, option: Option):
        self.option = option
        if 'ipv4_mode' in option:
            self.ipv4_mode()
        if 'ipv6_mode' in option:
            self.ipv6_mode()

    def ipv4_mode(self):
        if 'ipv4_setted' not in self.option:
            ip = self.get_ip('ipv4')
            if ip is not None :
                self.option['ipv4_setted'] = ip
                logging.info('ipv4获取成功')
            else:
                logging.error('由于网络或配置不正确等原因，获取ipv4地址失败')
                return
        way = self.option['way'][0]
        eval(way + "(self.option, 'ipv4')")

    def ipv6_mode(self):
        if 'ipv6_setted' not in self.option:
                ip = self.get_ip('ipv6')
                if ip is not None:
                    self.option['ipv6_setted'] = self.get_ip('ipv6')
                    logging.info('ipv6获取成功')
                else:
                    logging.error('由于网络或配置不正确等原因，获取ipv6地址失败')
                    return
        way = self.option['way'][0]
        eval(way + "(self.option, 'ipv6')")


#根据option参数的获取ip方式获取ip
    def get_ip(self, mode) -> str:
        ip_get_way_config = self.option['ip_get_way_config']
        ip_get_way = ip_get_way_config[0]
        if mode == 'ipv4':
            if ip_get_way == 'api':
                return GetIP.get_ipv4_from_api()
            if ip_get_way == 'nic':
                return GetIP.get_from_nic('ipv4', ip_get_way_config[1])
            if ip_get_way == 'cmd':
                return  GetIP.get_from_self_cmdline(ip_get_way_config[1])
            if ip_get_way == 'python':
                return  GetIP.get_from_self_python('ipv4', ip_get_way_config[1])
        else:
            if ip_get_way == 'api':
                return GetIP.get_ipv6_from_api()
            if ip_get_way == 'nic':
                return GetIP.get_from_nic('ipv6', ip_get_way_config[1])
            if ip_get_way == 'cmd':
                return  GetIP.get_from_self_cmdline(ip_get_way_config[1])
            if ip_get_way == 'python':
                return  GetIP.get_from_self_python('ipv6', ip_get_way_config[1])

