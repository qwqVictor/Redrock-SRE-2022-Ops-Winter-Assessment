#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DDNS管理脚本

Author: zhangxinhui02

管理本机的DDNS服务运行。

安装本脚本后键入'ddns'命令以运行脚本，键入'ddns -h'命令以查看帮助。
访问 https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/blob/master/Q2/2021214721/ 查看完整项目。
"""

# todo: 1.自动更新 2.部署安装脚本（包括各种依赖库） 3.多种获取IP的方法 4.IPv6 5.不用SDK自己实现 6.参数调用

import sys
import time
import urllib
import yaml
from typing import List

from Tea.exceptions import TeaException

from aliyun_dns_manager import DnsClient

# DDNS脚本配置文件的默认路径，可以进行修改。
config_path = './config.yaml'
# 脚本的默认设置及本地缓存的文件结构，如需改动请直接修改配置文件，不要修改代码。
data = {'a_description': 'This is the configuration file of ddns script. '
                         'You can edit this file directly to skip the initialization of the script. '
                         'There is no need to change last_ip value. '
                         'More information in https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment'
                         '/blob/master/Q2/2021214721/',
        'accessKeyId': '',
        'accessSecret': '',
        'domain': '',       # 域名
        'rr': '',           # 主机记录
        'record_type': '',  # 解析记录类型
        'last_ip': '',      # 缓存上次的IP
        'delay_min': 10     # 执行间隔(单位：分钟)
        }


def init_data() -> None:
    """初始化DDNS配置文件"""
    time.sleep(1)
    print('即将设置DDNS各参数以建立DDNS脚本配置和缓存文件')
    print('开始初始化DDNS服务配置，请依次输入屏幕提示的内容以设置DDNS(共6项)\n')
    global data
    data['accessKeyId'] = input('accessKeyId(可在云服务商控制台获取，建议使用RAM用户以提高安全性):\n')
    data['accessSecret'] = input('accessSecret(与accessKeyId同时获取):\n')
    data['domain'] = input('域名(不含子域名，例如 baidu.com ):\n')
    data['rr'] = input('主机记录(不含域名，例如 www.baidu.com 中的 www ):\n')
    data['record_type'] = input('解析记录类型(通常解析到IPv4地址为 A):\n')
    data['delay_min'] = int(input('DDNS脚本执行的间隔时间(单位：分钟，建议设置 10):\n'))
    save_local_data()
    print('设置完成')


def read_local_data() -> None:
    """读取本地缓存的DDNS信息"""
    with open(config_path, 'r') as f:
        global data
        data = yaml.safe_load(f)


def save_local_data() -> None:
    """将DDNS信息缓存在本地"""
    with open(config_path, 'w') as f:
        global data
        yaml.dump(data, f)


def get_internet_ip(way: 'int 获取IP的方法' = 1) -> 'str 获取到的IP地址':
    """获取本机的IP地址"""
    with urllib.request.urlopen('http://www.3322.org/dyndns/getip') as response:
        html = response.read()
        ip = str(html, encoding='utf-8').replace("\n", "")
    return ip


def main(
        args: List[str],
) -> None:
    # 测试配置文件是否存在及读写权限
    while True:
        try:
            open(config_path)
        except FileNotFoundError:
            # 判断为首次运行，打印脚本基本信息并初始化配置文件
            print('\nDDNS管理脚本\nAuthor: zhangxinhui02\n')
            print('键入\'ddns\'命令以启动脚本，键入\'ddns -h\'命令以查看帮助信息。')
            print('项目地址：https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment'
                  '/blob/master/Q2/2021214721/\n')
            init_data()
        except PermissionError:
            # 权限问题
            print('\tError! 脚本没有对配置文件的读写权限，请检查权限！\n配置文件路径：' + config_path + '\n')
            time.sleep(5)
            sys.exit()
        # 配置文件存在，读取配置
        read_local_data()

        # 检查配置项是否正确
        if data['accessKeyId'] == "" \
                or data['accessSecret'] == "" \
                or data['domain'] == "" \
                or data['rr'] == "" \
                or data['record_type'] == "":
            print('配置文件出现错误！')
            init_data()
        else:
            break

    # 判断IP是否发生变化
    dns = DnsClient(data['accessKeyId'], data['accessSecret'])
    ip = get_internet_ip()
    last_ip = data['last_ip']
    if ip == last_ip:
        print('IP未发生变化\n\tIP: ' + ip + '\n\t解析地址: ' + data['rr'] + '.' + data['domain'] + '\n')
    else:
        print('IP发生变化。\n\tOld IP: ' + last_ip + '\tNew IP: ' + ip)
        data['last_ip'] = ip
        save_local_data()
        print('尝试更新云解析……')
        # 尝试获取主机记录对应的解析记录的Record ID
        response = dns.describe_domain_record(data['domain'], data['rr'])
        record_id = ''
        try:
            record = response.body.domain_records.record[0]
            record_id = record.record_id
        except IndexError:
            # 主机记录没有对应任何解析记录，即没有创建，无法获取ID
            # 新建解析记录并重新获取Record ID
            dns.add_domain_record(data['domain'], data['rr'], data['record_type'], ip)
            print('云解析更新完成！\n\t解析地址: ' + data['rr'] + '.' + data['domain'] + '\n')
        else:
            # 存在主机记录对应的解析记录
            try:
                dns.update_domain_record(record_id, data['rr'], data['record_type'], ip)
                print('云解析更新完成！\n\t解析地址: ' + data['rr'] + '.' + data['domain'] + '\n')
            except TeaException:
                # 若本地IP缓存被意外修改，脚本会认为IP已发生变化，从而以同样的解析值再次更新解析记录，导致报错。
                # 一般忽略即可，下次运行会自动修正。
                print('本地IP缓存出现错误，本次未修改云解析记录。')


if __name__ == '__main__':
    main(sys.argv[1:])
