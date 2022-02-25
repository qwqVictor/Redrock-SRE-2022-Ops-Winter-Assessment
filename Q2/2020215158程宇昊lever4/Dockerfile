FROM ubuntu:20.04

MAINTAINER chengyuhao

ADD DDNSformal.sh /usr/locl/DDNSshell/
ADD DDNSfunction.sh /usr/locl/
ADD DDNSapi.sh /usr/locl/
ADD DDNS.conf /usr/locl/
ADD start.sh /usr/locl/
ADD crontabfile /usr/locl/

RUN apt-get update; \
    apt install -y curl sudo cron rsyslog; \
    cp /usr/locl/crontabfile /etc/crontab; \
    touch /var/log/cron.log; \
    chmod 777 /usr/locl/DDNSshell/DDNSformal.sh; \
    chmod 777 /usr/locl/start.sh 
    
WORKDIR /usr/locl/

CMD /usr/locl/start.sh

