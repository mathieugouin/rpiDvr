#!/usr/bin/bash

nohup ./dump_all.sh &
nohup ./dump_iostat.sh &
nohup ./dump_ping.sh &

