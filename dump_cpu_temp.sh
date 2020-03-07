#!/usr/bin/bash

logfile=cpu_temp.log

echo '###################################' >> $logfile
date >> $logfile
echo DATE, TEMP >> $logfile

# Loop indefinitely
while true
do
    d=$(date +"%Y-%m-%d %H:%M:%S")
    t=$(vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*')
    printf "%s, %s\n" "$d" "$t" >> $logfile
    sleep 1
done
