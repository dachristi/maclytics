#!/bin/bash

d=$(date +%Y-%m-%d_%H:%M:%S)

wifi_status=$(/sbin/iw dev | grep monitor | sed 's/^[\s\t]\+//g')
if [ "$wifi_status" = "type monitor" ];
  then
    echo $d "Wi-Fi status is ok"
else
  echo $d "Changing Wi-Fi mode to monitor" 
  /opt/maclytics/init.sh
  d=$(date +%Y-%m-%d_%H:%M:%S)
  echo $d "Wi-Fi mode successfully changed"
fi

wifi_status=$(/sbin/iw dev | grep monitor)
