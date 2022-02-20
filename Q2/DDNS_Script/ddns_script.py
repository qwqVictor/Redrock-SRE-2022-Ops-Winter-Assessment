#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DDNS管理脚本

Author: zhangxinhui02

管理本机的DDNS服务运行。

安装本脚本后键入'ddns'命令以运行脚本，键入'ddns -h'命令以查看帮助。
访问 https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/blob/master/Q2/ 查看完整项目。
"""

import sys
import time
import urllib
import yaml
from typing import List
from aliyun_dns_manager import DnsClient

# DDNS脚本配置文件的默认路径，可以进行修改。
config_path = './ddns_config.yaml'
# 脚本的默认设置及本地缓存的文件结构，如需改动请直接修改配置文件，不要修改代码。
data = {'accessKeyId': '',
        'accessSecret': '',
        'domain': '',  # 域名
        'rr': '',  # 主机记录
        'record_type': '',  # 解析记录类型
        'last_ip': '',  # 缓存上次的IP
        }


def init_data() -> None:
    """初始化DDNS服务缓存"""
    time.sleep(1)
    print('即将设置DDNS各参数以建立DDNS脚本配置和缓存文件')
    print('开始初始化DDNS服务配置，请依次输入指示的内容以设置DDNS(共5项)\n')
    global data
    data['accessKeyId'] = input('accessKeyId(可在云服务商控制台获取，建议使用RAM用户以提高安全性):\n')
    data['accessSecret'] = input('accessSecret(与accessKeyId同时获取):\n')
    data['domain'] = input('域名(不含子域名，例如 baidu.com ):\n')
    data['rr'] = input('主机记录(不含域名，例如 www.baidu.com 中的 www ):\n')
    data['record_type'] = input('解析记录类型(通常解析到IPv4地址为 A):\n')
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
        print('检查配置文件……')
        try:
            open(config_path)
        except FileNotFoundError:
            print('配置文件不存在')
            init_data()
        except PermissionError:
            print('\tError! 脚本没有对配置文件的读写权限，请检查权限！\n\t配置文件路径：' + config_path)
            time.sleep(5)
            sys.exit()
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
            print('配置文件无误！')
            break

    # 判断IP是否发生变化
    dns = DnsClient(data['accessKeyId'], data['accessSecret'])
    ip = get_internet_ip()
    last_ip = data['last_ip']
    if ip == last_ip:
        print('IP未发生变化\nIP: ' + ip + '\n')
    else:
        data['last_ip'] = ip
        print('IP发生变化。\n\tOld IP: ' + last_ip + '\n\tNew IP: ' + ip + '\n')
        print('尝试云解析……')
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
            response = dns.describe_domain_record(data['domain'], data['rr'])
            record = response.body.domain_records.record[0]
            record_id = record.record_id
        finally:
            dns.update_domain_record(record_id, data['rr'], data['record_type'], ip)
        print('云解析更新完成！\n')
        save_local_data()


if __name__ == '__main__':
    main(sys.argv[1:])
