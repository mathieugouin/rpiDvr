#/usr/bin/bash

logfile=cpu_usage.log

echo '###################################' >> $logfile
date >> $logfile

echo DATE,TimeOnly,CPU,%usr,%nice,%sys,%iowait,%irq,%soft,%steal,%guest,%idle >> $logfile

# Loop indefinitely
while ( [ 1 ] ) do
    d=$(date +"%Y-%m-%d %H:%M:%S")
    c=$(mpstat 1 1 | grep -w all | grep -v Average | tr -s ' ' | tr ' ' ',')
    printf "%s,%s\n" "$d" "$c" >> $logfile
done

