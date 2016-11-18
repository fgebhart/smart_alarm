#!/usr/bin/python

"""
in order to make this script run after each boot edit '.bashrc' file with: 'sudo nano .bashrc' and add the following
line at the end:
python run_on_boot.py
"""

import os


# activate alternative GIPO functions in order to enable zero-audio
os.system('gpio_alt -p 13 -f 0')
os.system('gpio_alt -p 18 -f 5')


# run python web-server
os.system('python /home/pi/smart_alarm/smart_alarm/python_server.py &')


# run smart_alarm main script
# os.system('sudo python smart_alarm0.6.py &')


