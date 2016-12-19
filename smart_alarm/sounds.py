import pygame
import pyttsx
import time
from random import randint
import os
import RPi.GPIO as GPIO


# set button input pin
button_input_pin = 24
# set pin for amplifier switch
amp_switch_pin = 12

# turn off GPIO warnings
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
# set pin to output
GPIO.setup(amp_switch_pin, GPIO.OUT)

button_pressed = False

# Define a threaded callback function to run in another thread when events are detected
def button_callback(channel):
    global button_pressed       # put in to debounce

    if GPIO.input(button_input_pin):  # if port 24 == 1
        print "button pressed"
        button_pressed = True
        time.sleep(5)
        button_pressed = False
    return button_pressed


def play_mp3_file(mp3_file):
    # set output high in order to turn on amplifier
    GPIO.output(amp_switch_pin, 1)
    time.sleep(0.3)
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    print "now playing file: ", mp3_file
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        if button_pressed:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            print 'alarm turned off'
            break
        else:
            continue
    time.sleep(0.5)
    # set ouput low in order to turn off amplifier
    GPIO.output(amp_switch_pin, 0)
    pygame.mixer.quit()


def say(text):
    """synthesizes the given text to speech"""
    # set output high in order to turn on amplifier
    GPIO.output(amp_switch_pin, 1)
    time.sleep(0.3)
    engine = pyttsx.init()
    engine.setProperty('rate', 115)
    # remove "pass" and uncomment next line in order to enable this function
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.5)
    # set ouput low in order to turn off amplifier
    GPIO.output(amp_switch_pin, 0)


def adjust_volume(value):
    """adjusts the audio volume by the given value (0-100%)"""
    volume_command = str('amixer set PCM -- ' + str(value) + '%')
    os.system(volume_command)
    play_mp3_file('/home/pi/smart_alarm/smart_alarm/sounds/blop.mp3')


def play_wakeup_music():
    """find all mp3 files in the folder /home/pi/music
    and play one of them at random"""
    list_of_music_files = []
    for file in os.listdir("/home/pi/smart_alarm/smart_alarm/music"):
        if file.endswith(".mp3"):
            list_of_music_files.append(str("/home/pi/smart_alarm/smart_alarm/music/" + str(file)))

    # figure out random track of the found mp3 files
    random_track = randint(0, len(list_of_music_files)-1)

    play_mp3_file(list_of_music_files[random_track])


def play_online_stream():
    """plays online radio using mpc. Press button to stop. Edit mpc playlist by:
    'mpc add filename', 'mpc playlist', 'mpc clear', 'mpc play', 'mpc stop'."""
    print 'now playing internet radio'
    # set output high in order to turn on amplifier
    GPIO.output(amp_switch_pin, 1)
    time.sleep(0.3)
    os.system('mpc play')

    while True:
        if button_pressed == False:
            pass
        else:
            break

    os.system('mpc stop')
    time.sleep(0.5)
    # set ouput low in order to turn off amplifier
    GPIO.output(amp_switch_pin, 0)
    print 'alarm turned off'
