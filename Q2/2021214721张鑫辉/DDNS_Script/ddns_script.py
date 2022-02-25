# -*- coding: utf-8 -*-
"""
DDNS管理脚本

Author: zhangxinhui02

管理本机的DDNS服务运行。

安装本脚本后键入'ddns'命令以运行脚本，键入'ddns help'命令以查看帮助。
访问 https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/blob/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/ 查看完整项目。
"""

import os
import sys
import time
import yaml
from Tea.exceptions import TeaException
from aliyun_dns_manager import DnsClient

# DDNS脚本配置文件的默认路径，可以进行修改。
config_path = '/etc/ddns_config.yaml'
# DDNS脚本配置文件的说明信息
config_description = '# 这是DDNS脚本的配置文件。手动配置此文件可以跳过脚本的初始化。\n' \
                     '# 访问 https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/blob/master/Q2/' \
                     '2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/ 以查看项目。\n\n' \
                     '# 以cache开头的值无需配置。\n' \
                     '# 以user开头的值必需配置。\n' \
                     '# 其他值可以保持默认。\n\n'
# 脚本的默认设置及本地缓存的文件结构，如需改动请直接修改配置文件，不要修改代码。
data = {'cache_ip': '',  # 缓存上次的IP
        'domain_record_type': 'A',  # 解析记录类型
        'host_need_ipv6': False,  # 是否支持ipv6
        'host_ip_command': 'ifconfig',  # 用户定义的查询IP的命令
        'host_get_ip_way': 0,  # 获取IP地址的方式，详见get_internet_ip函数
        'host_index': 0,  # 要使用的网卡或IP的索引
        'user_accessKeyId': '',
        'user_accessSecret': '',
        'user_domain': '',  # 域名
        'user_rr': '',  # 主机记录
        }
# 匹配不同类型IP地址的正则表达式
ipv4_pattern = r'([0,1]?\d{1,2}|2([0-4][0-9]|5[0-5]))(\.([0,1]?\d{1,2}|2([0-4][0-9]|5[0-5]))){3}'
ipv6_pattern = "^\\s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1," \
               "4}|((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3})|:)" \
               ")|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\" \
               "d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f" \
               "]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0" \
               "-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:" \
               "[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\" \
               "d|[1-9]?\\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1" \
               ",4}){0,3}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d))" \
               "{3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((2" \
               "5[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:))|(:(" \
               "((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d" \
               ")(\\.(25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)){3}))|:)))(%.+)?\\s*$"


def init_data() -> None:
    """初始化DDNS配置文件"""
    time.sleep(1)
    print('即将设置DDNS各参数以建立DDNS脚本配置和缓存文件')
    print('开始初始化DDNS服务配置，请依次输入屏幕提示的内容以设置DDNS'
          '(根据你的选择，需要设置6~8项参数)\n')
    global data
    data['user_accessKeyId'] = input('accessKeyId(可在云服务商控制台获取，建议使用RAM用户以提高安全性):\n')
    data['user_accessSecret'] = input('accessSecret(与accessKeyId同时获取):\n')
    data['user_domain'] = input('域名(不含子域名，例如 baidu.com ):\n')
    data['user_rr'] = input('主机记录(不含域名，例如 www.baidu.com 中的 www ):\n')
    # 设置是否使用IPv6
    while True:
        need_ipv6 = input('是否使用IPv6(默认为n) (y/n):\n')
        if need_ipv6.strip() in 'Yy':
            data['host_need_ipv6'] = True
            data['domain_record_type'] = 'AAAA'
            break
        elif need_ipv6.strip() in 'Nn':
            data['host_need_ipv6'] = False
            data['domain_record_type'] = 'A'
            break
        else:
            print('输入错误！\n')
    # 根据不同情况设置获取IP地址的方式
    while True:
        print('本脚本获取IP有以下方式，请选择一种方式(默认为0)：\n\t'
              '0. 从第三方API获取\n\t'
              '1. 从本机网卡配置获取\n\t'
              '2. 通过socket获取\n\t'
              '3. 通过用户自定义命令来从系统的命令行获取\n')
        data['host_get_ip_way'] = int(input('请选择IP地址的获取方式:\n(若使用IPv6则只能选择1和3模式)\n'))
        if data['host_need_ipv6']:
            if data['host_get_ip_way'] in [1, 3]:
                break
            else:
                print('输入错误！(使用IPv6时只能选择1和3模式)\n')
        else:
            if data['host_get_ip_way'] in [0, 1, 2, 3]:
                break
            else:
                print('输入错误！\n')
    # 根据获取IP的方式确定额外参数
    if data['host_get_ip_way'] == 1:
        # 网卡模式，设置指定网卡
        while True:
            print('接下来将列出本机的所有网卡及其IP地址，请输入你要使用的网卡的序号(默认为0):\n')
            net_cards_list = _get_net_cards_list()
            for net_card in net_cards_list:
                if data['host_need_ipv6']:
                    print('\t' + str(net_cards_list.index(net_card)) + ' - ' + net_card['name'] + ' : ' + net_card[
                        'ipv6'])
                else:
                    print('\t' + str(net_cards_list.index(net_card)) + ' : ' + net_card['name'] + ' : ' + net_card[
                        'ipv4'])
            index = int(input('\n请选择:\n'))
            try:
                a = net_cards_list[index]
            except IndexError:
                print('输入错误！\n')
            else:
                data['host_index'] = index
                break
    elif data['host_get_ip_way'] == 3:
        # 用户自定义命令模式，设置命令
        print('你需要为本脚本设置一条能够在本操作系统上输出IP地址的命令，脚本会提取命令的返回值中的有效IP地址。\n'
              '本脚本预设的默认命令为:\n\tifconfig\n'
              '支持Linux系统中执行。如需在Windows系统中执行可以设置为\'ipconfig\'\n'
              '如果要使用默认值，请按回车；要自定义命令，请输入命令。\n')
        command = input('请输入:\n')
        if command.strip() == '':
            data['host_ip_command'] = 'ifconfig'
        else:
            data['host_ip_command'] = command
        # 设置命令后再设置默认使用的IP的索引
        while True:
            print('接下来将列出从命令行提取的本机的所有IP地址，请输入你要使用的IP地址的序号(默认为0):\n')
            ip_list = _get_ip_list_by_command()
            ipv4_list = ip_list['ipv4']
            ipv6_list = ip_list['ipv6']
            if data['host_need_ipv6']:
                for ip in ipv6_list:
                    print('\t' + str(ipv6_list.index(ip)) + ' - ' + ip)
            else:
                for ip in ipv4_list:
                    print('\t' + str(ipv4_list.index(ip)) + ' - ' + ip)
            index = int(input('\n请选择:\n'))
            try:
                if data['host_need_ipv6']:
                    a = ipv6_list[index]
                else:
                    a = ipv4_list[index]
            except IndexError:
                print('输入错误！\n')
            else:
                data['host_index'] = index
                break

    save_local_data()
    print('\n脚本所需参数设置完成。\n')
    time.sleep(3)


def read_local_data() -> None:
    """读取本地缓存的DDNS信息"""
    with open(config_path, 'r', encoding='utf-8') as f:
        global data
        data = yaml.safe_load(f)


def save_local_data() -> None:
    """将DDNS信息缓存在本地"""
    with open(config_path, 'w', encoding='utf-8') as f:
        global data
        yaml.dump(data, f)
    # 添加配置文件的注释
    with open(config_path, 'r', encoding='utf-8') as f:
        str_data = f.read()
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(config_description + str_data)


def _get_net_cards_list() -> 'list 包含了网卡名称和IP地址的列表':
    """获取网卡信息"""
    import psutil
    import re
    net_cards_list = []
    ip_list = []
    # 对每一个网卡的原始信息进行提取
    a = psutil.net_if_addrs().items()
    for k, v in a:
        for o in v:
            ip_list.append(o.address)
        net_cards_list.append({'name': k, 'ips': ip_list[:], 'ipv4': '', 'ipv6': ''})
        ip_list = []
    # 对每一个网卡
    for net_card in net_cards_list:
        # 对该网卡的每一个ip
        for ip in net_card['ips']:
            ipv4_checker = len(re.findall(pattern=ipv4_pattern, string=ip))
            ipv6_checker = len(re.findall(pattern=ipv6_pattern, string=ip))
            if ipv4_checker == 1:
                # 判断为ipv4
                net_card['ipv4'] = ip
            elif ipv6_checker == 1:
                # 判断为ipv6
                net_card['ipv6'] = ip
    return net_cards_list


def _get_ip_list_by_command() -> 'dict 包含了IPv4和IPv6地址的字典':
    """执行设定的系统命令并获取IP地址字典"""
    ipv4_list = []
    ipv6_list = []
    import re
    with os.popen(data['host_ip_command'], 'r') as f:
        time.sleep(1)
        os_str_list = f.readlines()
        for os_str in os_str_list:
            ipv4_match = re.search(ipv4_pattern, os_str)
            if ipv4_match is not None:
                ipv4_list.append(ipv4_match.group().strip())
            else:
                # IPv6较难匹配，需要剔除其他干扰字符
                for s in os_str.split(' '):
                    ipv6_match = re.search(ipv6_pattern, s)
                    if ipv6_match is not None:
                        ipv6_str = ipv6_match.group().strip()
                        ipv6_list.append(ipv6_str.split('%')[0])
    for ip in ipv4_list:
        if str(ip).startswith('255.'):
            # 判断为子网掩码，删除
            ipv4_list.remove(ip)
    return {'ipv4': ipv4_list, 'ipv6': ipv6_list}


def get_internet_ip(
        way: 'int 获取IP的方法。0:在线API 1:网卡 2:socket 3:从用户定义的命令中提取。IPv6模式仅支持1和3。' = 0,
        index: 'int 要使用的索引，仅在网卡模式和自定义命令模式下有效' = 0,
        need_ipv6: 'bool 是否使用ipv6地址，仅在网卡和自定义命令模式下有效' = False
) -> 'str 获取到的IP地址':
    """获取本机的IP地址"""
    ip = ''

    if way == 0:
        # 通过第三方API获取
        import urllib
        with urllib.request.urlopen('http://www.3322.org/dyndns/getip') as response:
            html = response.read()
            ip = str(html, encoding='utf-8').replace("\n", "")

    elif way == 1:
        # 通过网卡获取
        net_cards_list = _get_net_cards_list()
        ip_dict = net_cards_list[index]
        if need_ipv6:
            ip = ip_dict['ipv6']
        else:
            ip = ip_dict['ipv4']

    elif way == 2:
        # 通过socket获取
        import socket
        ip = socket.gethostbyname(socket.gethostname())

    elif way == 3:
        # 通过执行用户定义的命令来提取IP
        ip_dict = _get_ip_list_by_command()
        ipv4_list = ip_dict['ipv4']
        ipv6_list = ip_dict['ipv6']
        if need_ipv6:
            ip = ipv6_list[index]
        else:
            ip = ipv4_list[index]
    return ip


def main() -> None:
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
        try:
            if data['user_accessKeyId'] == '' \
                    or data['user_accessSecret'] == '' \
                    or data['user_domain'] == '' \
                    or data['user_rr'] == '' \
                    or data['domain_record_type'] == '' \
                    or data['host_get_ip_way'] == '' \
                    or data['host_need_ipv6'] == '':
                print('配置文件出现错误！')
                init_data()
        except Exception:
            print('配置文件出现错误！')
            init_data()
        else:
            break
    # 判断IP是否发生变化
    dns = DnsClient(data['user_accessKeyId'], data['user_accessSecret'])
    ip = get_internet_ip(data['host_get_ip_way'], data['host_index'], data['host_need_ipv6'])
    last_ip = data['cache_ip']
    if ip == last_ip:
        print('IP未发生变化\n\tIP: ' + ip + '\n\t解析地址: ' + data['user_rr'] + '.' + data['user_domain'] + '\n')
    else:
        print('IP发生变化。\n\tOld IP: ' + last_ip + '\tNew IP: ' + ip)
        data['cache_ip'] = ip
        save_local_data()
        print('尝试更新云解析……')
        # 尝试获取主机记录对应的解析记录的Record ID
        response = dns.describe_domain_record(data['user_domain'], data['user_rr'])
        try:
            record = response.body.domain_records.record[0]
            record_id = record.record_id
        except IndexError:
            # 主机记录没有对应任何解析记录，即没有创建，无法获取ID
            # 新建解析记录并重新获取Record ID
            dns.add_domain_record(data['user_domain'], data['user_rr'], data['domain_record_type'], ip)
            print('云解析更新完成！\n\t解析地址: ' + data['user_rr'] + '.' + data['user_domain'] + '\n')
        else:
            # 存在主机记录对应的解析记录
            try:
                dns.update_domain_record(record_id, data['user_rr'], data['domain_record_type'], ip)
                print('云解析更新完成！\n\t解析地址: ' + data['user_rr'] + '.' + data['user_domain'] + '\n')
            except TeaException:
                # 若本地IP缓存被意外修改，脚本会认为IP已发生变化，从而以同样的解析值再次更新解析记录，导致报错。
                # 一般忽略即可，下次运行会自动修正。
                print('本地IP缓存出现错误，本次未修改云解析记录。')
