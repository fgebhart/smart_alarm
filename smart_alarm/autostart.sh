#!/bin/bash

# set envirmonetal variable for apache path 
export smart_alarm_path=/home/pi/smart_alarm/smart_alarm

# activate alternative GIPO functions in order to enable zero-audio
gpio_alt -p 13 -f 0
gpio_alt -p 18 -f 5

# run smart_alarm main script
sudo python $smart_alarm_path/smart_alarm0.9.py &
