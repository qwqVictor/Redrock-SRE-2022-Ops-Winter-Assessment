#!/bin/bash

# Check if user is root
if [ $(id -u) != "0" ]; then
    echo "Error: You must be root to run this script."
    exit 1
fi

# Prepare environment
echo "Preparing environment"
apt install build-essential wget curl automake pcre pcre-devel zlib zlib-devel open openssl-devel -y
useradd -s /sbin/nologin nginx
echo "Environment is done"
flag=`nginx -v`
latest=`curl https://nginx.org/en/download.html|grep 'nginx-.*gz'|awk -F '-' '{print $2}'|sed 's/.tar.gz">nginx//g'`
current=`nginx -v 2>&1 |sed 's/nginx version: nginx\///g'`
if [-z $flag];then
	echo "You didn't install nginx"
else
	if [$current == $latest]; then
        	echo Your version is latest
		else
			echo "The lateset version is $latest, your version is $current"
	fi
fi

echo "Input install version: [default=$latest]"
while true
do
	read -r version < /dev/tty
	flag=`curl https://nginx.org/download/|grep $version.tar`
	if [ -z "$flag" ]; then
    	echo "Wrong version, input again"
	elif [-z $version ];then
		version=$latest
	fi
done

wget http://nginx.org/download/nginx-$version.tar.gz
tar -zxvf nginx-$version.tar.gz
cd nginx-$version

inst(){
	echo "Input install parameter"
	ipath=`nginx -V 2>&1|grep configure|sed "s/configure arguments://g"|tr ' ' '\n'|grep prefix=|awk -F '=' '{print $2}'`
	if [ -z $ipath ]; then
		echo "The path to install [default /usr/local/nginx]"
		read -r ipath < /dev/tty
		if [ -z "$ipath" ]; then
   		 	ipath=/usr/local/nginx
		fi
	else
		echo "The path to install [default $ipath]"
		read -r ipatha < /dev/tty
		if [ -z "$ipatha" ]; then
	   	continue
		else
			ipath=$ipatha
		fi
	fi

	epath=`nginx -V 2>&1|grep configure|sed "s/configure arguments://g"|tr ' ' '\n'|grep error.log|awk -F '=' '{print $2}'`
	if [ -z $epath ]; then
    		echo "The path of error log [default /var/log/nginx/error.log]"
		read -r epath < /dev/tty
		if [ -z "$epath" ]; then
			epath=/var/log/nginx/error.log
		fi
	else
		echo "The path to install [default $epath]"
		read -r epatha < /dev/tty
			if [ -z "$epatha" ]; then
				continue
			else
				epath=$epatha
			fi
	fi

	apath=`nginx -V 2>&1|grep configure|sed "s/configure arguments://g"|tr ' ' '\n'|grep http.log|awk -F '=' '{print $2}'`
	if [ -z $apath ]; then
		echo "The path of assess log [default /var/log/nginx/assess.log]"
		read -r apath < /dev/tty
		if [ -z "$apath" ]; then
	    		apath=/var/log/nginx/assess.log
		fi
	else
		echo "The path to install [default $apath]"
		read -r apatha < /dev/tty
		if [ -z "$apatha" ]; then
   			continue
		else
			apath=$apatha
		fi
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
}
argu=`nginx -V 2>&1|grep configure|sed "s/configure arguments://g"`
if [ -n $argu ]; then
	echo "Find exist parameters, use it?[Y/n]"
	read -r use < /dev/tty
	if [ $use == N] || [ $use == n ]; then
		inst	
	else
		echo "Installing"
		./configure $argu
		make&&make install
		echo "Finish"
else
	inst

