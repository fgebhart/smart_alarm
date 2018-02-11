"""
short script for testing functionality of button
"""

import time
import RPi.GPIO as GPIO

# configure GPIO setup BCM / BOARD
GPIO.setmode(GPIO.BCM)

# set GPIO24 to input with internal pull down resistor
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


while True:
    print "button is: ", GPIO.input(24)
    time.sleep(0.4)
