
import logging
import re
import exception
from tools import config_reader


class Option(dict):
    def __init__(self):
        super().__init__()


class OptionManager:

    def __init__(self, **kwargs):
        self._option = Option()
        self.kwargs = kwargs

    def get_option(self):
        self.parse_configfile()
        self._add_ip_get_way_config()
        self._set_dns_mode()
        self._add_hostname()
        self._add_dns_way()
        return self._option

    def _check_kwargs(self, name):
        if name in self.kwargs:
            if self.kwargs[name] is not None:
                return True
        return False

    def _set_param(self, name, content):
        self._option[name] = content

    # 判断要启用的dns模式，是ipv4还是ipv6还是同时启用
    def _set_dns_mode(self):
        # 判断输入是否包含以下字段
        # 这三个字段比较特殊，因为使用了action=‘store_ture’,所以即使不输入这几个参数，返回的也是false，所以直接读取就好
        ipv4_mode = self.kwargs['ipv4']
        ipv6_mode = self.kwargs['ipv6']
        ipv46_mode = self.kwargs['ipv46']

        is_ip_setted = self._check_kwargs('ip')
        a = self._check_kwargs('a')
        aaaa = self._check_kwargs('aaaa')

        if ipv4_mode and ipv6_mode:
            ipv4_mode = False
            ipv6_mode = False
            ipv46_mode = True

        if not ipv4_mode and not ipv6_mode and not ipv46_mode or ipv4_mode:
            if not a:
                raise exception.AError
            else:
                if is_ip_setted:
                    self._add_ipv4_only(self.kwargs['ip'][0])
                else:
                    self._add_ipv4_only('')
        elif ipv6_mode:
            if not aaaa and a:
                self.kwargs['aaaa'] = self.kwargs['a']
                logging.error('未输入AAAA记录，已自动将值设置为与A记录相同')
            elif not aaaa and not a:
                raise exception.AAAAError
            if is_ip_setted:
                self._add_ipv6_only(self._option['ip'][0])
            else:
                self._add_ipv6_only('')
        else:
            if not aaaa and a:
                self.kwargs['aaaa'] = self.kwargs['a']
                logging.error('未输入AAAA记录，已自动将值设置为与A记录相同')
            elif aaaa and not a:
                self.kwargs['a'] = self.kwargs['aaaa']
                logging.error('未输入A记录，已自动将值设置为与AAAA记录相同')
            elif not aaaa and not a:
                raise exception.AError
            self._add_ipv46()

    # 如果ip参数为空，则自动获取，否则按照指定ip，进行dns功能
    def _add_ipv4_only(self, ip):
        if not ip == '':
            pattern = r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$'
            if re.match(pattern, ip) is None:
                raise exception.ipv4InputError
            else:
                self._add_ipv4_setted(ip)
        self._set_param('ipv4_mode', True)
        self._add_a_name()

    # 如果ip参数为空，则自动获取，否则按照指定ip，进行dns功能
    def _add_ipv6_only(self, ip):
        if not ip == '':
            pattern = '^([\da-fA-F]{1,4}:){6}((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$|^::([' \
                      '\da-fA-F]{1,4}:){0,4}((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$|^([' \
                      '\da-fA-F]{1,4}:):([\da-fA-F]{1,4}:){0,3}((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[' \
                      '0-4]\d|[01]?\d\d?)$|^([\da-fA-F]{1,4}:){2}:([\da-fA-F]{1,4}:){0,2}((25[0-5]|2[0-4]\d|[' \
                      '01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$|^([\da-fA-F]{1,4}:){3}:([\da-fA-F]{1,4}:){0,' \
                      '1}((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$|^([\da-fA-F]{1,' \
                      '4}:){4}:((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$|^([\da-fA-F]{1,' \
                      '4}:){7}[\da-fA-F]{1,4}$|^:((:[\da-fA-F]{1,4}){1,6}|:)$|^[\da-fA-F]{1,4}:((:[\da-fA-F]{1,4}){1,' \
                      '5}|:)$|^([\da-fA-F]{1,4}:){2}((:[\da-fA-F]{1,4}){1,4}|:)$|^([\da-fA-F]{1,4}:){3}((:[\da-fA-F]{' \
                      '1,4}){1,3}|:)$|^([\da-fA-F]{1,4}:){4}((:[\da-fA-F]{1,4}){1,2}|:)$|^([\da-fA-F]{1,' \
                      '4}:){5}:([\da-fA-F]{1,4})?$|^([\da-fA-F]{1,4}:){6}:$ '
            if re.match(pattern, ip) is None:
                raise exception.ipv6InputError
            else:
                self._add_ipv6_setted(ip)
        self._set_param('ipv6_mode', True)
        self._add_aaaa_name()

    def _add_ipv46(self):
        if self._check_kwargs('ip'):
            ip = self._option['ip']
            if len(ip) == 2:
                self._add_ipv4_only(ip[0])
                self._add_ipv6_only(ip[1])
            else:
                raise exception.ipInputError
        else:
            self._add_ipv4_only('')
            self._add_ipv6_only('')

    def _add_a_name(self):
        self._set_param("a", self.kwargs["a"])

    def _add_aaaa_name(self):
        self._set_param("aaaa", self.kwargs["aaaa"])

    def _add_cloudflare(self):
        config = self.kwargs['cloudflare']
        if len(config) != 2:
            raise exception.dnsConfigError
        content = ['cloudflare', *config]
        self._set_param('way', content)

    def _add_tencentCloud(self):
        config = self.kwargs['tencentCloud']
        if len(config) != 2:
            raise exception.dnsConfigError
        content = ['TencentCloud', *config]
        self._set_param('way', content)

    def _add_aliYun(self):
        config = self.kwargs['aliYun']
        if len(config) != 2:
            raise exception.dnsConfigError
        content = ['AliYun', *config]
        self._set_param('way', content)

    def _add_dns_way(self):
        if self._check_kwargs('cloudflare'):
            self._add_cloudflare()
        elif self._check_kwargs('tencentCloud'):
            self._add_tencentCloud()
        elif self._check_kwargs('aliYun'):
            self._add_aliYun()
        else:
            # 没有指定dns厂商
            raise exception.dnsConfigError

    def _add_ipv4_setted(self, ipv4):
        self._set_param('ipv4_setted', ipv4)

    def _add_ipv6_setted(self, ipv6):
        self._set_param('ipv6_setted', ipv6)

    # hostname
    def _add_hostname(self):
        if self._check_kwargs('hostname'):
            pattern = r".+\..+"
            for hostname in self.kwargs['hostname']:
                if re.match(pattern, hostname) is None:
                    raise exception.HostnameError
            self._option['hostname'] = self.kwargs['hostname']

#判断ip获取的方式
    def _add_ip_get_way_config(self):
        if self._check_kwargs('ip_get_way_config'):
            way = self.kwargs['ip_get_way_config'][0]
            if way == 'api':
                self._option['ip_get_way_config'] = ['api']
                return
            elif way == 'setted':
                self.kwargs['ip'] = self.kwargs['ip_get_way_config'][1:]
                return
            elif way == 'nic':
                if len(self.kwargs['ip_get_way_config']) == 1:
                    self._option['ip_get_way_config'] = ['nic', 'eth0']
                else:
                    self._option['ip_get_way_config'] = self.kwargs['ip_get_way_config']
                return
            elif way == 'cmd':
                self._option['ip_get_way_config'] = self.kwargs['ip_get_way_config']
                return
            elif way == 'python':
                self._option['ip_get_way_config'] = self.kwargs['ip_get_way_config']
                return
            else:
                raise exception.ipGetWayConfigError
        else:
            self._option['ip_get_way_config'] = ['api']

#读取配置文件
    def parse_configfile(self):
        if self._check_kwargs('configfile'):
            try:
                self.kwargs.update(config_reader.ConfigReader(self.kwargs['configfile']).get_dict())
            except Exception:
                raise exception.configReadFail




