FROM ubuntu:18.04

MAINTAINER joshua "1787548456@qq.com"

RUN apt-get update

#instaall pip3 
RUN apt-get install -y python3 && apt-get install -y python3-pip 

#pip install requests
RUN pip3 install requests 

#install wget 
RUN apt-get install -y wget 

#install crontab
RUN apt-get install -y cron 

#安装中文支持，防止python报错
RUN /bin/bash -c "apt-get install -y language-pack-zh-hans && locale-gen zh_CN.UTF-8"
RUN echo "export LANG=zh_CN.UTF-8" >> /etc/profile 
RUN /bin/bash -c "source /etc/profile"
ENV PYTHONIOENCODING=utf-8

#copy file needed to install 
COPY install_ddns_docker.sh /tmp
COPY crond /etc/cron.d/joshua_ddns_crond
 
# Apply cron job
RUN crontab /etc/cron.d/joshua_ddns_crond
 
# Create the log file to be able to run tail
RUN touch /var/log/cron.log

#install joshua_ddns
RUN  cd /tmp && ./install_ddns_docker.sh

#prevent be killed at once 
ENTRYPOINT cron && tail -f /var/log/cron.log
 



