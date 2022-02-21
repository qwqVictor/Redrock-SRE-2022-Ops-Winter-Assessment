FROM mysql:latest
COPY ./settings/. /Documents/settings/
COPY ./all.py /Documents/all.py
COPY ./environment_settle.sql /Documents/environment_settle.sql
COPY ./id_rsa.pub /Documents/authorized_keys
COPY ./sshd_config /Documents/sshd_config
COPY ./vsftpd.conf /Documents/vsftpd.conf
COPY ./profile /Documents/profile
COPY ./vsftpd.chroot_list /Documents/vsftpd.chroot_list
COPY ./vsftpd /Documents/vsftpd
COPY ./ftpusers /Documents/ftpusers
COPY ./run.sh /Documents/run.sh
RUN cp -r -f /Documents/settings/. /etc/apt/ && apt-get update && apt-get upgrade -y && apt-get install ssh -y && apt-get install -y locales && apt-get install nano -y && apt-get install net-tools -y && mkdir ~/.ssh && apt-get install vsftpd -y
RUN locale-gen en_US.UTF-8 && apt-get install python -y && apt-get install python3-pip -y && pip install cryptography && pip install pymysql 
RUN cp -f /Documents/sshd_config /etc/ssh/sshd_config && cp -f /Documents/vsftpd.conf /etc/vsftpd.conf && cp -f /Documents/vsftpd.chroot_list /etc/vsftpd.chroot_list && cp -f /Documents/vsftpd /etc/pam.d/vsftpd && cp -f /Documents/ftpusers /etc/ftpusers && chmod 777 /Documents/run.sh
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV service vsftpd restart && service vsftpd status 

