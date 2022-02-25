# DDNS脚本
Author: zhangxinhui02

------

## DDNS

由于ISP分配给用户设备的IP地址并不固定，为了将设备当前的IP及时映射到域名上，使用户在任何时候都可以通过固定的地址访问到设备，产生了动态域名解析DDNS技术。

------

## 简介

本脚本可以自动获取设备的IP，并通过云服务商提供的SDK将IP解析到指定域名。

鉴于网络连接的复杂性，脚本提供多种获取IP地址的方式，确保解析成功。

脚本已支持IPv6地址的解析。

脚本在安装成功后可通过命令行快速调用。

------

## 安装

请保证操作系统中安装了python3环境和pip3工具。

运行以下命令即可安装。

```shell
wget https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/raw/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/DDNS_Script/install_files/install_ddns_script.sh
sudo chmod +x install_ddns_script.sh
sudo ./install_ddns_script.sh
```

脚本将被安装在`/usr/local/ddns_script`路径下，配置文件将会生成在`/etc/ddns_config.yaml`。此外将通过Systemd创建定时任务，每10分钟执行一次DDNS。

脚本依赖包括以下的Python模块，将会自动安装。[查看全部](https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/blob/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/DDNS_Script/install_files/requirements.txt)

- 阿里云SDK
- PyYAML
- psutil
- urllib3

------

## 运行

安装完成后会自动运行ddns脚本配置，需要配置accessKeyId，accessSecret，域名，主机记录，IP类型，获取IP方式等内容。此时可以依次设置，也可以退出脚本手动修改位于`/etc/ddns_config.yaml`的配置文件。

每一次运行DDNS脚本的时候都会检查配置文件，若配置文件不存在或配置错误，将会提示重新设置配置文件。

安装后在命令行运行`ddns`即可手动执行一次DDNS操作（即使已经存在定时任务）。

运行`ddns help`可以查看命令行帮助。

运行`ddns init`可以初始化配置文件。

运行`ddns set`可以通过脚本引导设置配置文件。

------

## 说明

`DDNS_Script`文件夹内为脚本的主程序。

`DDNS_Script/install_files`内为安装所需文件。

`DDNS_Script/aliyun_dns_manager.py`为调用阿里云SDK的模块。若需要支持其他云解析厂商，需要按照此模块中的类来编写相应的模块，并在`DDNS_Script/ddns_script.py`中导入模块。

------

此脚本仍有待改进，具体计划为：

1. 实现脚本的自动更新
2. 不使用云厂商的SDK来自行实现
3. 加密存储配置文件中的accessKeyId和accessSecret等敏感信息
4. 若设备的网卡配置发生变化则会导致设定的网卡索引发生错位，待修复
5. 增加云解析的TTL等参数的配置选项
6. 支持Windows的自动安装脚本

------

## 考核

考核完成至level3。level1未完成。

### level0

获取IP并更新解析记录详见[ddns_script.py](https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/blob/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/DDNS_Script/ddns_script.py)，设置定时器详见[install_ddns_script.sh](https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/blob/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/DDNS_Script/install_files/install_ddns_script.sh)。

### level1

因为是之前Fork的，所以没看见后面加的题。

### level2

多种方式获取IP地址详见[ddns_script.py](https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/blob/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/DDNS_Script/ddns_script.py)。

### level3

支持IPv6详见[ddns_script.py](https://github.com/zhangxinhui02/Redrock-SRE-2022-Ops-Winter-Assessment/blob/master/Q2/2021214721%E5%BC%A0%E9%91%AB%E8%BE%89/DDNS_Script/ddns_script.py)。

### level4

待完成。