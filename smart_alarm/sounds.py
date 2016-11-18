import pygame
import pyttsx
import time
from random import randint
import os
import RPi.GPIO as GPIO





def play_mp3_file(mp3_file):
    """using pygame lib in order to play mp3 sound files"""
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    print "now playing file: ", mp3_file
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        if GPIO.input(24) == 1:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            print 'alarm turned off'
            break
        else:
            continue
    pygame.mixer.quit()


def say(text):
    """synthesizes the given text to speech"""
    engine = pyttsx.init()
    engine.setProperty('rate', 115)
    # remove "pass" and uncomment next line in order to enable this function
    engine.say(text)
    engine.runAndWait()


def adjust_volume(value):
    """adjusts the audio volume by the given value (0-100%)"""
    volume_command = str('amixer set PCM -- ' + str(value) + '%')
    os.system(volume_command)
    url_to_adjust_volume_sound = str(str(os.path.dirname(__file__)) + '/music/blop.mp3')
    play_mp3_file(url_to_adjust_volume_sound)


def play_wakeup_music():
    """find all mp3 files in the folder /home/pi/music
    and play one of them at random"""
    list_of_music_files = []
    for file in os.listdir("/home/pi/"):
        if file.endswith(".mp3"):
            list_of_music_files.append(file)

    # figure out random track of the found mp3 files
    random_track = randint(0, len(list_of_music_files)-1)

    play_mp3_file(list_of_music_files[random_track])


def play_online_stream():
    """plays online radio using mpc. Press button to stop. Edit mpc playlist by:
    'mpc add filename', 'mpc playlist', 'mpc clear', 'mpc play', 'mpc stop'."""
    print 'now playing internet radio'
    os.system('mpc play')

    while True:
        if button_pressed() == False:
            pass
        else:
            break

    os.system('mpc stop')
    print 'alarm turned off'
