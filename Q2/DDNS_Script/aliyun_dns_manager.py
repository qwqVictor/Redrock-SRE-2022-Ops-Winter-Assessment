# -*- coding: utf-8 -*-
"""
阿里云云解析管理模块

Author: zhangxinhui02

引入此模块以简单管理域名解析
"""

from alibabacloud_alidns20150109.client import Client as Alidns20150109Client
from alibabacloud_alidns20150109.models import AddDomainRecordResponse, UpdateDomainRecordResponse, \
    DeleteDomainRecordResponse, DescribeDomainRecordsResponse
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_tea_openapi import models as open_api_models


class DnsClient:
    """
    阿里云域名解析管理器

    调用阿里云SDK执行简易的域名解析操作

    Attributes:
        client (Alidns20150109Client): 用于域名操作的阿里云账号Client

    """

    def __init__(
            self,
            access_key_id: str,
            access_key_secret: str
    ) -> None:
        """使用AK&SK初始化账号Client"""
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'alidns.cn-shanghai.aliyuncs.com'
        self.client = Alidns20150109Client(config)

    def add_domain_record(
            self,
            domain_name: 'str 域名',
            rr: 'str 主机记录',
            record_type: 'str 解析记录类型',
            value: 'str 记录值'
    ) -> AddDomainRecordResponse:
        """添加解析记录"""
        request = alidns_20150109_models.AddDomainRecordRequest(
            domain_name=domain_name,
            rr=rr,
            type=record_type,
            value=value)
        response = self.client.add_domain_record(request)
        return response

    def update_domain_record(
            self,
            record_id: 'str Record ID',
            rr: 'str 主机记录',
            record_type: 'str 解析记录类型',
            value: 'str 记录值'
    ) -> UpdateDomainRecordResponse:
        """修改解析记录"""
        request = alidns_20150109_models.UpdateDomainRecordRequest(
            record_id=record_id,
            rr=rr,
            type=record_type,
            value=value)
        response = self.client.update_domain_record(request)
        return response

    def delete_domain_record(
            self,
            record_id: 'str Record ID'
    ) -> DeleteDomainRecordResponse:
        """删除解析记录"""
        request = alidns_20150109_models.DeleteDomainRecordRequest(record_id=record_id)
        response = self.client.delete_domain_record(request)
        return response

    def describe_domain_record(
            self,
            domain_name: 'str 域名',
            rr: 'str 主机记录'
    ) -> DescribeDomainRecordsResponse:
        """查询解析记录"""
        request = alidns_20150109_models.DescribeDomainRecordsRequest(domain_name=domain_name, rrkey_word=rr)
        response = self.client.describe_domain_records(request)
        return response
