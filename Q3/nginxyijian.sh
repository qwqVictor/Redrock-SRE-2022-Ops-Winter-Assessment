#!/bin/bash

#-----------------------------------------------------------------------------------------------------------------------
echo "Preparing environment"
sudo apt install build-essential automake pcre pcre-devel zlib zlib-devel open openssl-devel -y
useradd -s /sbin/nologin nginx
echo "Environment is done"
#-----------------------------------------------------------------------------------------------------------------------
echo "Input install version: [default=1.20.2]"
read -r version < /dev/tty
if [ -z "$version" ]; then
    version=1.20.2
fi
wget http://nginx.org/download/nginx-$version.tar.gz
tar -zxvf nginx-$version.tar.gz
cd nginx-$version
#-----------------------------------------------------------------------------------------------------------------------
echo "Input install parameter"
echo "The path to install [default /usr/local/nginx]"
read -r ipath < /dev/tty
if [ -z "$ipath" ]; then
    ipath=/usr/local/nginx
fi
echo "The path of error log [default /var/log/nginx/error.log]"
read -r epath < /dev/tty
if [ -z "$epath" ]; then
    epath=/var/log/nginx/error.log
fi
echo "The path of assess log [default /var/log/nginx/assess.log]"
read -r apath < /dev/tty
if [ -z "$apath" ]; then
    apath=/var/log/nginx/assess.log
fi
echo "Installing"
./configure --prefix=$ipath \
--conf-path=/etc/nginx/nginx.conf \
--user=nginx \
--group=nginx \
--error-log-path=$epath \
--http-log-path=$apath \
--pid-path=/var/run/nginx/nginx.pid \
--lock-path=/var/lock/nginx.lock \
--with-http_ssl_module \
--with-http_stub_status_module \
--with-http_gzip_static_module \
--with-http_flv_module \
--with-http_mp4_module \
--http-client-body-temp-path=/var/tmp/nginx/client \
--http-proxy-temp-path=/var/tmp/nginx/proxy \
--http-fastcgi-temp-path=/var/tmp/nginx/fastcgi \
--with-debug
make && make install
echo "Finish"
