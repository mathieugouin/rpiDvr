#!/usr/bin/bash

logfile=ping.log


# Loop indefinitely
while ( [ 1 ] ) do
    echo '###################################' >> $logfile
    # Date stamp
    d=$(date +"%Y-%m-%d %H:%M:%S")
    echo $d >> $logfile

    ping -c 60 -i 1 192.168.1.1 >> $logfile
done

