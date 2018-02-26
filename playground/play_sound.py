import pygame
import RPi.GPIO as GPIO

# set pin for amplifier switch
amp_switch_pin = 5

GPIO.setwarnings(False)
# configure RPI GPIO
GPIO.setmode(GPIO.BCM)
# set pin to output
GPIO.setup(amp_switch_pin, GPIO.OUT)


def play_mp3_file(mp3_file):
    # set output high in order to turn on amplifier
    GPIO.output(amp_switch_pin, 1)
    """using pygame lib in order to play mp3 sound files"""
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    print "now playing file: ", mp3_file
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    # set ouput low in order to turn off amplifier


play_mp3_file("example.mp3")

GPIO.output(amp_switch_pin, 0)
