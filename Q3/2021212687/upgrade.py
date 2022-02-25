import requests
import re
import os

if(os.system("id -u") !="0"):
    print( "Error: You must be root to run this script")
    exit()

def update():
    latest=str(re.search(r"nginx-\d.\d{1,2}.\d{1,2}",str(htmlstr.text)).group())
    print("Latest version is "+latest+".")
    select=str(input("Do you want to continue?(y/n)"))
    if select=="y":
        dir=str(input("Please select path to install.(default /usr/local/nginx)"))
        match=re.match("/",dir)
        if match is None:
            dir="/usr/local/nginx"
        durl=downloadurl+latest
        os.system("mkdir %s&&cd %s && wget %s && tar -zxvf %s.tar.gz && make && make install" % (dir,dir,durl,latest))
    else:
        exit()
    
def com():
    select=str(input("Do you want to continue?(y/n)"))
    if select=="y":
        dir=str(input("Please select path to install.(default /usr/local/nginx)"))
        match=re.match("/",dir)
        if match is None:
            dir="/usr/local/nginx"
        os.system("mkdir %s" % (dir))
        os.system("cd %s" % (dir))
        wget.download(downloadurl+latest+".tar.gz")
        os.system("tar -zxvf %s.tar.gz" % (latest))
        os.system("cd nginx-%s" % (latest))
        os.system("make && make install")
    else:
        exit()
        
R=requests
url="https://nginx.org/en/download.html"
downloadurl="https://nginx.org/download/"
htmlstr=R.get(url)
print("Preparing environment")
os.system("apt install build-essential automake pcre pcre-devel zlib zlib-devel open openssl-devel wget -y")
os.system("useradd -s /sbin/nologin nginx")
print("Environment is done")

print("Welcome! Please input a number")
print("1. Download, compile and install specific version")
print("2. Update to latest version")
print("3. Exit")
select=int(input("Please input"))
if select==1:
    com()
elif select==2:
    update()
else:
    exit()




    
    
    