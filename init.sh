#!/bin/bash

/sbin/ip link set wlan0 down
/sbin/iw wlan0 set monitor control
/sbin/ip link set wlan0 up
