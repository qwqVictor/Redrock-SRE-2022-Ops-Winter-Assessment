#!/bin/bash
cron
rsyslogd
touch /var/log/cron.log
tail -F /var/log/syslog /var/log/cron.log

