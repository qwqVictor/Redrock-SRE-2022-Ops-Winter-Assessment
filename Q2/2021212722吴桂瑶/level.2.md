#### 获取本地ip地址：

1.打开cmd命令界面   输入—ipconfig查看当前ip地址

2.使用python socket模块

import socket

address = socket.gethostbyname(socket.gethostname())

3.subproces模块（域名ip也可以

subprocess.Popen("ipconfig", shell=True, stdout=subprocess.PIPE)

#### 获取域名ip地址：

1.cmd命令界面

​			—使用ping命令

​			—nslookup查询