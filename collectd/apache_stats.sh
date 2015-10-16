#!/bin/bash
# Récupération du nombre de connexions apache

HOSTNAME="${COLLECTD_HOSTNAME:-`hostname --short`}"
INTERVAL="${COLLECTD_INTERVAL:-60}"

VALUE_SENT=$(/usr/bin/nice -n 19 /usr/bin/ionice -c3 /usr/bin/sudo netstat -tunap | grep -ic apache) 
echo "PUTVAL \"$HOSTNAME/http-in/gauge-http-in-`hostname --short`\" interval=$INTERVAL N:$VALUE_SENT"

