#!/bin/bash
# -*- coding: utf-8 -*-
# 此脚本将安装DDNS脚本到Linux操作系统中
# https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/blob/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/

# 安装路径
INSTALL_PATH="/usr/local/ddns_script"
SERVICE_PATH="/etc/systemd/system/"

if [ ! -d $INSTALL_PATH ]
then mkdir $INSTALL_PATH
fi

cd $INSTALL_PATH || exit
wget https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/raw/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/DDNS_Script/install_files/requirements.txt
wget https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/raw/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/DDNS_Script/ddns
wget https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/raw/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/DDNS_Script/ddns_script.py
wget https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/raw/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/DDNS_Script/aliyun_dns_manager.py
chmod +x ddns
pip3 install -r requirements.txt || pip install -r requirements.txt

cd $SERVICE_PATH || exit
wget https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/raw/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/DDNS_Script/install_files/ddns.service
wget https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/raw/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/DDNS_Script/install_files/ddns.timer
systemctl enable ddns.timer
systemctl start ddns.timer

ddns
