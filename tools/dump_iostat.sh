#/usr/bin/bash

logfile=iostat.log

echo '###################################' >> $logfile
date >> $logfile

# 5 days = 432000 seconds
iostat -d 1 432000 >> $logfile

