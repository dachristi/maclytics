#!/bin/bash

while true
do

d=$(date +%Y-%m-%d_%H:%M:%S)
echo "Starting tcpdump" $d

/usr/sbin/tcpdump -c 100000 -i  wlan0 -e -s 256 | grep --line-buffered "Probe Request" >> /opt/maclytics/captured_requests/data_$d.txt

mv /opt/maclytics/captured_requests/* /opt/maclytics/queue

done
