#!/bin/bash
cd /usr/local 

if wget http://sunshin.club/file/joshua_ddns.tar.gz
then
   tar -zxvf joshua_ddns.tar.gz
   chmod +x joshua_ddns
   rm -f joshua_ddns.tar.gz
   echo "脚本已安装在/usr/loacl/joshua_ddns目录下"
   ln -s /usr/local/joshua_ddns/joshua_ddns /usr/bin
   echo 完成软链接至bin
else
   echo 安装失败,自动退出
   exit 1
fi

cd joshua_ddns 
if wget http://sunshin.club/file/ddns.conf
then
   echo "配置文件模板已下载至/usr/loacl/joshua_ddns目录下"
else
   echo 安装失败,自动退出
   exit 1
fi
