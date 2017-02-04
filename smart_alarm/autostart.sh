#!/bin/bash

# set envirmonetal variable for apache path 
export smart_alarm_path=/home/pi/smart_alarm/smart_alarm

# activate alternative GIPO function ALT5 for gpio18 which
# is pwm1 and enables rpi-zero audio
gpio_alt -p 18 -f 5
#gpio_alt -p 13 -f 0

# activate pwm for gpio 12 with ALT0 which is pwm0
#gpio_alt -p 12 -f 0

# run smart_alarm main script
python $smart_alarm_path/smart_alarm.py &

sudo chmod o+w $smart_alarm_path/data.xml
