#!/bin/sh
# 最严格规则，只允许指定ip的指定端口(incomming和outgoing)的开放
# My system IP/set ip address of server
SERVER_IP="xxx.xx.xx.xx"
# Flushing all rules
iptables -F
iptables -X

# Setting default filter policy
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

# Allow unlimited traffic on loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
 
# Allow incoming ssh only
iptables -A INPUT -p tcp -s 0/0 -d $SERVER_IP --sport 513:65535 --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -s $SERVER_IP -d 0/0 --sport 22 --dport 513:65535 -m state --state ESTABLISHED -j ACCEPT

# Allow app ports
PORTS="19395 29295 29395 39395"
for port in $PORTS
do
iptables -A INPUT -p tcp -s 0/0 -d $SERVER_IP --sport 513:65535  --dport $port -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -s $SERVER_IP -d 0/0  --sport $port --dport 513:65535 -m state --state ESTABLISHED -j ACCEPT
done


# Allow incoming ssh only from IP in IPS
IPS="xxx.xxx.xxx.xxx xxx.xx.xxx.xx xxx.xx.xxx.xxx"
for ip in $IPS
do
iptables -A INPUT -p tcp -s $ip -d $SERVER_IP --sport 513:65535 --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -s $SERVER_IP -d $ip --sport 22 --dport 513:65535 -m state --state ESTABLISHED -j ACCEPT
done

# Allow outgoing http request to 58.215.137.243
iptables -A OUTPUT -p tcp -s $SERVER_IP -d 58.215.137.243 --sport 513:65535 --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -p tcp -s 58.215.137.243 -d $SERVER_IP --sport 80 --dport 513:65535 -m state --state ESTABLISHED -j ACCEPT

# Allow all http incoming requests
iptables -A OUTPUT -p tcp -s $SERVER_IP --sport 513:65535 --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -p tcp -d $SERVER_IP --sport 80 --dport 513:65535 -m state --state ESTABLISHED -j ACCEPT

# DNS
iptables -A OUTPUT -p udp -s $SERVER_IP --sport 1024:65535 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -p udp --sport 53 -d $SERVER_IP --dport 1024:65535 -m state --state ESTABLISHED -j ACCEPT
iptables -A OUTPUT -p tcp -s $SERVER_IP --sport 1024:65535 --dport 53 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -p tcp --sport 53 -d $SERVER_IP --dport 1024:65535 -m state --state ESTABLISHED -j ACCEPT

# Allow http port
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 80 -j ACCEPT

iptables -A INPUT -p tcp --dport 8080 -j ACCEPT
iptables -A OUTPUT -p tcp --sport 8080 -j ACCEPT


# make sure nothing comes or goes out of this box
iptables -A INPUT -j DROP
iptables -A OUTPUT -j DROP
