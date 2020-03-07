#!/usr/bin/bash

logfile=all.log

echo '###################################' >> $logfile
date >> $logfile

echo DATE,TimeOnly,CPU,%usr,%nice,%sys,%iowait,%irq,%soft,%steal,%guest,%idle,FREE,TEMP >> $logfile

# Loop indefinitely
while ( [ 1 ] ) do
    # Date stamp
    d=$(date +"%Y-%m-%d %H:%M:%S")

    # Mem (free)
    m=$(free -w | tr -s ' ' | cut -d ' ' -f 8 | head -n 2 | tail -n 1)

    # Temp
    t=$(vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*')

    # CPU (last because it includes the pause)
    c=$(mpstat 1 1 | grep -w all | grep -v Average | tr -s ' ' | tr ' ' ',')

    printf "%s,%s,%s,%s\n" "$d" "$c" "$m" "$t" >> $logfile
done

