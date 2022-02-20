#!/bin/bash
passwd
service ssh restart
service vsftpd restart
cp -f /Documents/profile /etc/profile
cp -f /Documents/authorized_keys /root/.ssh/authorized_keys
service ssh restart
