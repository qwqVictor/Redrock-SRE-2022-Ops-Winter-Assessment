# -*- coding: utf-8 -*-
# 根据各种参数运行DDNS脚本
# https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/raw/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/

import sys
import ddns_script

help_msg = """
DDNS脚本 帮助\n
查看项目：https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/raw/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/\n
命令行参数示例：
    ddns parameter


    help : 显示帮助信息。

    init : 初始化配置文件，可以通过手动编辑配置文件来跳过脚本初始化。

    set : 通过引导设置配置文件
"""
try:
    if sys.argv[1] == 'help':
        # 显示帮助
        print(help_msg)
    elif sys.argv[1] == 'init':
        # 初始化配置文件
        ddns_script.save_local_data()
        print('配置文件路径 ' + ddns_script.config_path)
    elif sys.argv[1] == 'set':
        # 设置配置文件
        ddns_script.init_data()
        print('配置文件路径 ' + ddns_script.config_path)
    else:
        # 直接运行
        ddns_script.main()
except IndexError:
    # 直接运行
    ddns_script.main()
