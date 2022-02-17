import logging
import os
import re
os.sys.path
os.sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import requests
import exception

'''
从api接口获取当前的公网ip信息，只获取ipv4地址
'''


def get_ipv4_from_api():
    url = 'http://api.ipify.org'  # api from ip.sb, return query ip
    try:
        result = requests.request('GET', url, timeout=5)
    except Exception:
        logging.error('无法在线获取当前ipv4，请检测网络状况')
        return

    return result.text  # 返回ipv4信息


'''
从api接口获取当前的公网ipv6信息，若无ipv6IP地址，则返回None
'''

#采用柔和退出方式，考虑到网络时好时坏
def get_ipv6_from_api():
    url = 'http://api64.ipify.org'
    try:
        result = requests.request('GET', url)
    except Exception:
        logging.error('无法在线获取当前ipv6，请检测网络状况')
        return
    if '.' in result.text:
        raise exception.ipv6IsNotSupportedError
    else:
        return result.text

#从命令'ip addr'中读取ip地址，之所以用这个，因为默认支持它的系统数量比ipconfig大
def get_from_nic(mode, eth):
    command = 'ip addr'
    result = os.popen(command).read()
    if mode == 'ipv4':
        pattern = eth+r':[\s|\S]*?inet\s([\d|.]+)\/'
    else:
        pattern = eth+r':[\s|\S]*?inet6\s([\S]+)\/'
    return re.search(pattern, result).groups()[1]

#根据用户自定义命令，获取ip，从命令行的返回一定要只有ip
def get_from_self_cmdline(command):
    return os.popen(command).read().strip()

#从自定义python脚本获取IP地址，此python文件应该实现getIP(mode)方法，其中mode传入参数为ipv4、ipv6
def get_from_self_python(mode, file:str):
    import importlib
    dirname = os.path.dirname(file)
    if dirname == '':
        os.sys.path.append(os.path.abspath('.'))
    else:
        os.sys.path.append(dirname)
    filename = os.path.basename(file)
    self_python = importlib.import_module(filename)
    return self_python.getIP(mode)
if __name__ == '__main__':
    pass
