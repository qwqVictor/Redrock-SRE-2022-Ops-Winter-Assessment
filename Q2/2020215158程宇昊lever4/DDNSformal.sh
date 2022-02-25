#!/bin/bash

source /usr/locl/DDNS.conf
source /usr/locl/DDNSapi.sh
source /usr/locl/DDNSfunction.sh

[ "$AccessKeyID" = "" ] && echo "Please input AccessKeyID!" 
[ "$AccessKeySecret" = "" ] && echo "Please input AccessKeySecret!" 
[ "$DomainName" = "" ] && echo "Please input DomainName!" 

SubDomainName=${SubDomainName:-"www"}
TTL=${TTL:-600}
GetPublicIpWay=${GetPublicIpWay:-"1"}
DomainServerIp=${DomainServerIp:-"223.5.5.5"}

if [ "$SubDomainName" = "@" ]
then
	WholeDomainName="$DomainName"
else
	WholeDomainName="$SubDomainName.$DomainName"
fi


case $GetPublicIpWay in 
	1)
		LocalIpv4=`getIpv4Firth 2>&1`
		LocalIpv6=`getIpv6Firth 2>&1`
		;;
	2)
		LocalIpv4=`getIPv4Sec 2>&1`
		LocalIpv6=`getIPv6Sec 2>&1`
		;;
	*)
		LocalIpv4=`getIPv4Zero 2>&1` || echo "error" 
		LocalIpv6=`getIPv4Zero 2>&1` || echo "error" 
		;;
esac

for loop in 1
do

	DomainIpv4=`nslookup -qt=A $WholeDomainName $DomainServerIp 2>&1`
	
	if [ "$?" = "0" ]
	then
	DomainIpv4=`echo "$DomainIpv4" | grep "Address:" | tail -n +2 | head -n1 | awk '{print $NF}'` 
		if [ "$DomainIpv4" = "$LocalIpv4" ]
		then 
			echo "[$(date "+%G/%m/%d %H:%M:%S")] Ipv4 is all right."
			continue
		fi
	fi

	timestamp=`date -u "+%Y-%m-%dT%H%%3A%M%%3A%SZ"`

	if [ "$RecordIdIpv4" = "" ]
	then
		RecordIdIpv4=`askRecordId "A" | receiveRecordId`
	fi

	if [ "$RecordIdIPv4" = "" ]
	then 
		RecordIdIpv4=`addRecordId $LocalIpv4 "A" | receiveRecordId`
		echo "[$(date "+%G/%m/%d %H:%M:%S")] $RecordIdIpv4"
	else
		newRecordId $RecordIdIpv4 $LocalIpv4 "A"
	fi

	if [ "$RecordIdIpv4" = "" ]
	then
		echo "[$(date "+%G/%m/%d %H:%M:%S")] IPv4 Error!"
	else
        	echo "[$(date "+%G/%m/%d %H:%M:%S")] IPv4 Success!"
	fi
done

for loop in 1
do
	DomainIpv6=`nslookup -qt=AAAA $WholeDomainName $DomainServerIp 2>&1`

	if [ "$?" = "0" ]
	then
        	DomainIpv6=`echo "$DomainIpv6" | grep "Address:" | tail -n1 |  awk '{print $NF}'`
        	if [ "$DomainIpv6" = "$LocalIpv6" ]
        	then
                	echo "[$(date "+%G/%m/%d %H:%M:%S")] Ipv6 is all right!"
                	continue
        	fi
	fi


	timestamp=`date -u "+%Y-%m-%dT%H%%3A%M%%3A%SZ"`
	
	LocalIpv6=`echo "$LocalIpv6" | sed 's/:/%3A/g'`


	if [ "$RecordIdIpv6" = "" ]
	then
        	RecordIdIpv6=`askRecordId "AAAA" | receiveRecordId`
	fi

	if [ "$RecordIdIPv6" = "" ]
	then
        	RecordIdIpv6=`addRecordId $LocalIpv6 "AAAA" | receiveRecordId`
		echo "[$(date "+%G/%m/%d %H:%M:%S")] $RecordIdIpv6"
	else
        	newRecordId $RecordIdIpv6 $LocalIpv6 "AAAA"
	fi

	if [ "$RecordIdIpv6" = "" ]
	then
        	echo "[$(date "+%G/%m/%d %H:%M:%S")] IPv6 Error!"
	else
        	echo "[$(date "+%G/%m/%d %H:%M:%S")] IPv6 Success!"
	fi
done
