#!/bin/bash
passwd
service ssh restart
service vsftpd restart
cp -f ./profile /etc/profile
