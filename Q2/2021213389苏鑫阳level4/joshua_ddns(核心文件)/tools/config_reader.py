import os

os.sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import configparser
import exception


# 解析配置文件，输出成optionmanager能识别的dict
# 配置文件的优先度小于命令行输入参数，即配置文件和命令行都输入的参数，将会优先命令行
class ConfigReader:
    def __init__(self, file):
        self.config = configparser.ConfigParser()
        filename = file[0].name
        if not self.config.read(filename, 'utf-8'):
            raise exception.configReadFail
        self.section = self.config.sections()
        # 将所有参数整合成命令行，已满足optionmanager要求的输入格式
        self.dict = {}

    # 调用此参数返回解析好的dict
    def get_dict(self):
        self._reader()
        return self.dict

    # 读取开始
    def _reader(self):
        if 'BASIC' not in self.section:
            raise exception.configSectionError('BASIC')
        basic_config_options = self.config.options('BASIC')

        if 'hostname' in basic_config_options:
            # 预计在未来版本实现同时对多个域名进行解析，但实际上开两个脚本就可以完成这样的任务，所以暂时不急
            self.dict['hostname'] = self._mutiple_values_to_list(self.config.get('BASIC', 'hostname'))
        else:
            raise exception.HostnameError
        #判断ddns的模式是ipv4 ipv6 or ipv46
        if 'ip_mode' in basic_config_options:
            ip_mode = self.config.get('BASIC', 'ip_mode')
            if ip_mode == 'ipv4':
                self.dict['ipv4'] = True
                self.dict['ipv6'] = False
                self.dict['ipv46'] = False
                if 'a' in basic_config_options:
                    self.dict['a'] = self._mutiple_values_to_list(self.config.get('BASIC', 'a'))
                else:
                    raise exception.configValueIllegal('BAISC中A')
            elif ip_mode == 'ipv6':
                self.dict['ipv4'] = False
                self.dict['ipv6'] = True
                self.dict['ipv46'] = False
                if 'aaaa' in basic_config_options:
                    self.dict['aaaa'] = self._mutiple_values_to_list(self.config.get('BASIC', 'aaaa'))
                else:
                    raise exception.configValueIllegal('BAISC中AAAA')
            elif ip_mode == 'ipv46':
                self.dict['ipv4'] = False
                self.dict['ipv6'] = False
                self.dict['ipv46'] = True
                a = 'a' in basic_config_options
                aaaa = 'aaaa' in basic_config_options
                if a and aaaa:
                    self.dict['a'] = self._mutiple_values_to_list(self.config.get('BASIC', 'a'))
                    self.dict['aaaa'] = self._mutiple_values_to_list(self.config.get('BASIC', 'aaaa'))
                elif a and not aaaa:
                    self.dict['a'] = self._mutiple_values_to_list(self.config.get('BASIC', 'A'))
                    self.dict['aaaa'] = self._mutiple_values_to_list(self.config.get('BASIC', 'A'))
                elif not a and aaaa:
                    self.dict['a'] = self._mutiple_values_to_list(self.config.get('BASIC', 'aaaa'))
                    self.dict['aaaa'] = self._mutiple_values_to_list(self.config.get('BASIC', 'aaaa'))
                else:
                    raise exception.configValueIllegal('A或AAAA(选择ipv46模式后至少在此两参数中填写一个)')
        else:
            raise exception.configValueIllegal('ip_mode')

        #如果每天ip_get_way则默认模式api
        if 'ip_get_way' in basic_config_options:
            ip_get_way = self.config.get('BASIC', 'ip_get_way')
        else:
            ip_get_way = 'api'

        #判断用户输入模式，并据此进行读取对应配置
        if ip_get_way == 'api':
            self.dict['ip_get_way_config'] = ['api']
        elif ip_get_way == 'setted':
            self.dict['ip_get_way_config'] = ['setted', *self._ip_get_way_config_setted_reader()]
        elif ip_get_way == 'nic':
            self.dict['ip_get_way_config'] = ['nic', self._ip_get_way_config_nic_reader()]
        elif ip_get_way == 'python':
            self.dict['ip_get_way_config'] = ['python', self._ip_get_way_config_python_reader()]
        elif ip_get_way == 'cmd':
            self.dict['ip_get_way_config'] = ['cmd', self._ip_get_way_config_cmd_reader()]
        else:
            raise exception.configValueIllegal('BASIC中的ip_get_way')

        # 判断是否存在dns_api选项，不存在则报错提示
        if 'dns_api' not in basic_config_options:
            raise exception.configValueIllegal('BASIC中的dns_api')
        else:
            dns_api = self.config.get('BASIC', 'dns_api')

        #判断调用哪家的api
        if dns_api == 'cloudflare':
            self.dict['cloudflare'] = self._ip_dns_api_config_cloudflare_reader()
        elif dns_api == 'tencentCloud':
            self.dict['tencentCloud'] = self._ip_dns_api_config_tencentCloud_reader()
        elif dns_api == 'aliYun':
            self.dict['aliYun'] = self._ip_dns_api_config_aliYun_reader()
        else:
            raise exception.configValueIllegal('BASIC中的dns_api')

#读取用户自定义的的ip
    def _ip_get_way_config_setted_reader(self) -> list:
        if 'IP_WAY_CONFIG' not in self.section:
            raise exception.configSectionError('IP_WAY_CONFIG')
        else:
            ip_way_config = self.config.options('IP_WAY_CONFIG')
        if 'ip' in ip_way_config:
            return self._mutiple_values_to_list(self.config.get('IP_WAY_CONFIG', 'ip'))
        else:
            raise exception.configValueIllegal('ip(ip_get_way设置setted后,应该在IP_WAY_CONFIG中的ip填写参数)')

#读取cloudflare key 和 id zone
    def _ip_dns_api_config_cloudflare_reader(self) -> list:
        if 'DNS_API_CONFIG' not in self.section:
            raise exception.configSectionError('DNS_API_CONFIG')
        else:
            dns_api_config_option = self.config.options('DNS_API_CONFIG')

        if 'cloudflare_key' not in dns_api_config_option:
            raise exception.configValueIllegal('DNS_API_CONFIG中的cloudflare_key(dns_api设置cloudflare后,应该填写此参数)')
        elif 'cloudflare_zone_id' not in dns_api_config_option:
            raise exception.configValueIllegal('DNS_API_CONFIG中的cloudflare_zone_id(dns_api设置cloudflare后,应该填写此参数)')

        return [self.config.get('DNS_API_CONFIG', 'cloudflare_key'),
                self.config.get('DNS_API_CONFIG', 'cloudflare_zone_id')]

#读取腾讯云的secret key 和 secret_key_id
    def _ip_dns_api_config_tencentCloud_reader(self) -> list:
        if 'DNS_API_CONFIG' not in self.section:
            raise exception.configSectionError('DNS_API_CONFIG')
        else:
            dns_api_config_option = self.config.options('DNS_API_CONFIG')


#config parse 无视大小写 传进来全小写
        if 'tencentcloud_secret_key_id' not in dns_api_config_option:
            raise exception.configValueIllegal(
                'DNS_API_CONFIG中的tencentCloud_secret_key_id(dns_api设置tencentCloud后,应该填写此参数)')
        elif 'tencentcloud_secret_key' not in dns_api_config_option:
            raise exception.configValueIllegal(
                'DNS_API_CONFIG中的tencentCloud_secret_key(dns_api设置tencentCloud后,应该填写此参数)')

        return [self.config.get('DNS_API_CONFIG', 'tencentCloud_secret_key_id'),
                self.config.get('DNS_API_CONFIG', 'tencentCloud_secret_key')]

#获取阿里云的aliYun_access_key和aliYun_access_key_id
    def _ip_dns_api_config_aliYun_reader(self) -> list:
        if 'DNS_API_CONFIG' not in self.section:
            raise exception.configSectionError('DNS_API_CONFIG')
        else:
            dns_api_config_option = self.config.options('DNS_API_CONFIG')

        if 'aliyun_access_key_id' not in dns_api_config_option:
            raise exception.configValueIllegal(
                'DNS_API_CONFIG中的aliYun_access_key_id(dns_api设置aliiYun后,应该填写此参数)')
        elif 'alyun_access_key' not in dns_api_config_option:
            raise exception.configValueIllegal(
                'DNS_API_CONFIG中的aliYun_access_key(dns_api设置aliYun后,应该填写此参数)')

        return [self.config.get('DNS_API_CONFIG', 'aliYun_access_key_id'),
                self.config.get('DNS_API_CONFIG', 'aliYun_access_key')]

    def _mutiple_values_to_list(self, value: str):
        return value.split(',')

    def _ip_get_way_config_nic_reader(self):
        if 'IP_WAY_CONFIG' not in self.section:
            raise exception.configSectionError('IP_WAY_CONFIG')
        else:
            ip_way_config = self.config.options('IP_WAY_CONFIG')
        if 'nic' in ip_way_config:
            return self.config.get('IP_WAY_CONFIG', 'nic')
        else:
            return 'eth0'

    def _ip_get_way_config_cmd_reader(self):
        if 'IP_WAY_CONFIG' not in self.section:
            raise exception.configSectionError('IP_WAY_CONFIG')
        else:
            ip_way_config = self.config.options('IP_WAY_CONFIG')
        if 'cmd' in ip_way_config:
            return self.config.get('IP_WAY_CONFIG', 'cmd')
        else:
            raise exception.configValueIllegal('cmd(ip_get_way设置cmd后,应该在IP_WAY_CONFIG中的cmd填写参数)')

    def _ip_get_way_config_python_reader(self):
        if 'IP_WAY_CONFIG' not in self.section:
            raise exception.configSectionError('IP_WAY_CONFIG')
        else:
            ip_way_config = self.config.options('IP_WAY_CONFIG')
        if 'python_file' in ip_way_config:
            return self.config.get('IP_WAY_CONFIG', 'python_file')
        else:
            raise exception.configValueIllegal('python_file(ip_get_way设置cmd后,应该在IP_WAY_CONFIG中的python_file填写参数)')
