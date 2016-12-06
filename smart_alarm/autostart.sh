#!/bin/bash


# activate alternative GIPO functions in order to enable zero-audio
gpio_alt -p 13 -f 0
gpio_alt -p 18 -f 5


cd smart_alarm/smart_alarm/

# run python web-server
python python_server.py &


# run smart_alarm main script
sudo python smart_alarm0.8.py &
