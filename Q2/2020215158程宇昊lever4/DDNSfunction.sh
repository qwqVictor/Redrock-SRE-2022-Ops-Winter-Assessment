#!/bin/bash

function sendRequest(){
	local args="AccessKeyId=$AccessKeyID&Action=$1&Format=json&$2&Version=2015-01-09"
    	local hash=$(echo -n "GET&%2F&$(enc "$args")" | openssl dgst -sha1 -hmac "$AccessKeySecret&" -binary | openssl base64)
    	curl -s "http://alidns.aliyuncs.com/?$args&Signature=$(enc "$hash")"
}

function addRecordId(){
	sendRequest "AddDomainRecord&DomainName=$DomainName" "RR=$SubDomainName&SignatureMethod=HMAC-SHA1&SignatureNonce=$timestamp&SignatureVersion=1.0&TTL=$TTL&Timestamp=$timestamp&Type=$2&Value=$1"
}

function newRecordId(){
	sendRequest "UpdateDomainRecord" "RR=$SubDomainName&RecordId=$1&SignatureMethod=HMAC-SHA1&SignatureNonce=$timestamp&SignatureVersion=1.0&TTL=$TTL&Timestamp=$timestamp&Type=$3&Value=$2"
	
}

function askRecordId(){
	sendRequest "DescribeSubDomainRecords" "SignatureMethod=HMAC-SHA1&SignatureNonce=$timestamp&SignatureVersion=1.0&SubDomain=$WholeDomainName&Timestamp=$timestamp&Type=$1"

}

function receiveRecordId(){
	grep -Eo '"RecordId":"[0-9]+"' | cut -d':' -f2 | tr -d '"'
}

function getIpv4Firth(){
	curl -s 4.ipw.cn
}

function getIpv6Firth(){
	curl -s 6.ipw.cn
}

function getIPv4Sec(){
	ip addr show docker0 | grep "inet" | awk '{print $2}' | awk -F"/" '{print $1}'
}

function getIPv6Sec(){
	ip addr show docker0 | grep "inet" | awk '{print $2}' | awk -F"/" '{print $1}'
}
