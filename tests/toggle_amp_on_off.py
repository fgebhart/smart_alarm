import pygame
import RPi.GPIO as GPIO

# set pin for amplifier switch
amp_switch_pin = 5

GPIO.setwarnings(False)
# configure RPI GPIO
GPIO.setmode(GPIO.BCM)
# set pin to output
GPIO.setup(amp_switch_pin, GPIO.OUT)


if GPIO.input(amp_switch_pin) == 0:
    print 'turning amp on'
    GPIO.output(amp_switch_pin, 1)
else:
    print 'turning amp off'
    GPIO.output(amp_switch_pin, 0)
