#!/usr/bin/bash

logfile=mem_usage.log

echo '###################################' >> $logfile
date >> $logfile

free >> $logfile
free -w | tr -s ' ' | cut -d ' ' -f 8 | head -n 1 >> $logfile

echo 'DATE,FREE' >> $logfile

# Loop indefinitely
while true
do
    d=$(date +"%Y-%m-%d %H:%M:%S")
    m=$(free -w | tr -s ' ' | cut -d ' ' -f 8 | head -n 2 | tail -n 1)
    printf "%s, %s\n" "$d" "$m" >> $logfile
    sleep 1
done
