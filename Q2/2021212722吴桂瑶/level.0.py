#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
import re
import socket
import subprocess
import json
from threading import Timer
import datetime

def internetip():
    child = subprocess.Popen("nslookup jwzx.cqupy.edu.cn", shell=True, stdout=subprocess.PIPE)
    out = child.communicate()  
    ipv4_pattern = '((?:[0-9]{1,3}\.){3}[0-9]{1,3})'
    m = re.findall(ipv4_pattern, str(out))
    address1 = m[0][0]
    return address1

def localip():
    address2 = socket.gethostbyname(socket.gethostname())
     

def recordid(client):
     request = DescribeDomainRecordsRequest()
     request.set_accept_format('json')
     request.set_DomainName("jwzx.cqpy.edu.cn")
     res = client.do_action_with_exception(request)
     res = str(res, encoding='utf-8')
     result = json.loads(res)
     recordid = result["DomainRecords"]["Record"][0]["RecordId"] 


def update_record(client, priority, ttl, record_type, value, rr, record_id):
     request = UpdateDomainRecordRequest()
     request.set_accept_format('json')
     request.set_Priority(priority)
     request.set_TTL(ttl)
     request.set_Value(value)
     request.set_Type(record_type)
     request.set_RR(rr)
     request.set_RecordId(record_id)
     response = client.do_action_with_exception(request)
     response = str(response, encoding='utf-8')
     return response
 
 

def run_result(client, priority, ttl, record_type, value, rr, record_id):
     if localip() == internetip():
         pass
     else:
         result = update_record(client, priority, ttl, record_type, value, rr, record_id)
         result = json.loads(result)
         print("%s" % result["RecordId"])
 

if __name__ == '__main__':
     client = AcsClient('youraccessKeyId', 'youraccessSecret', 'cn-chengdu')
     record_id = recordid(client)
     ip = localip()
     tt = Timer(3600,run_result)
     tt.start()

