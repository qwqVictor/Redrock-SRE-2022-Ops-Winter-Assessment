#!/bin/bash
#自动更新nginx版本
#2022年2月20日19点07分
#######################################################################################
#安装依赖库：
nginx_address=http://nginx.org/download #下载地址
path=$(pwd) #安装目录
function pre() #此函数用于安装nginx的准备工作,在自动更新nginx时会自动跳过这一步。
{
echo 安装gcc,g++
apt-get install build-essential
apt-get install libtool
echo 安装pcre依赖库............
apt-get install libpcre3 libpcre3-dev
echo 安装zlib依赖库............
#apt-get update
apt-get install libpcre3 libpcre3-dev
echo 安装ssl依赖库..............
apt-get install openssl
}
function Downloadnginx() #下载nginx压缩包并解压,跟据原有的nginx编译配置完成编译安装
{
    cd "$path" || exit
    wget -P "$path" "$nginx_address"/nginx-"$var".tar.gz
    tar -zxvf nginx-"$var".tar.gz
    cd "$path"/nginx-"$var" || exit
    ./configure
    make
    make install
    cd /usr/local/nginx/sbin || exit
    ./nginx
    ln -s /usr/local/nginx/sbin/* /usr/local/sbin
    nginx -V
}
function New_nginx() #获取最新版本的nginx版本号
{
    wget -c http://nginx.org/download/
    grep "\"nginx-.*tar.gz\"" -o index.html >>nginxmax1.txt
    grep "[0-9*\.[0-9]*\.[0-9]" nginxmax1.txt -o | sort -V >>nginxmax2.txt
    new_nginx=$(awk 'END {print}' nginxmax2.txt)
    echo "$new_nginx"
    rm index.html nginxmax1.txt nginxmax2.txt
}
function Now_nginx() #获取客户机上的nginx的版本号
{
    nginx -v &>nownginx.txt
    now_nginx=$(grep "[0-9]*\.[0-9]*\.[0-9]" -o nownginx.txt)
    echo "$now_nginx"
   rm nownginx.txt
}
function Juge() #判断网站上的最新版本号与现在的版本号的大小关系
{
     [ "$now_nginx" \> "$new_nginx" ] && var="$now_nginx" || var="$new_nginx"
}
function UpGrade()
{
    cd /opt || exit
    wget -c $nginx_address/nginx-"$var".tar.gz
    tar -zxvf nginx-"$var".tar.gz
    cd /opt/nginx-"$var" || exit
    Old_configure
    ./configure
    make
    mv /usr/local/nginx/sbin/nginx /usr/local/nginx/sbin/nginx.old
    cp -r /opt/nginx-"$var"/objs/nginx /usr/local/nginx/sbin/
    cd /usr/local/nginx/sbin || exit
    ./nginx
    /usr/local/nginx/sbin/nginx -V

}
    read -r "请输入你想下载的版本号(在本机没有安装nginx的情况下),若为空,则自动安装升级最新版本nginx(请在已安装nginx的情况下直接按enter)" var
    if [ -z  "$var" ];then
        echo 将停用本机nginx服务,并安装最新版本的nginx 
        nginx -s stop
        New_nginx
        Now_nginx
        Juge
        UpGrade
    else
        echo 将要安装nginx-"$var"
        pre
        Downloadnginx
    fi

