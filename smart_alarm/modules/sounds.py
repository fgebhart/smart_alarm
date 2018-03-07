import pygame
import pyttsx
import time
from random import randint
import os
import RPi.GPIO as GPIO
import logging


# set button input pin
button_input_pin = 24
# set pin for amplifier switch
amp_switch_pin = 5

# turn off GPIO warnings
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
# set pin to output
GPIO.setup(amp_switch_pin, GPIO.OUT)

# read environmental variable for project path
project_path = os.environ['smart_alarm_path']
logger = logging.getLogger(__name__)


class Sound(object):
    """sound class manages smart alarm audio"""

    def __init__(self):
        """initialize variables"""
        # write to error.log file
        logger.info('sound-module initialized')
        self.sound_active = False
        self.stop_sound = False

    def stopping_sound(self):
        """stops alarm when button is pressed"""
        logger.warning('current sound play is being stopped')
        self.stop_sound = True

    def toggle_amp_pin(self, toggle):
        # set pwm audio pin one or zero, depending on the current state
        logger.debug("setting amp switch pin to: {}".format(toggle))
        if toggle == 0:
            GPIO.output(amp_switch_pin, 0)
        elif toggle == 1:
            GPIO.output(amp_switch_pin, 1)
        else:
            raise TypeError("got wrong value for toggle variable, should be 1 or 0.")

    def play_mp3_file(self, mp3_file, force=False):
        if self.sound_active:
            if force:
                self.stopping_sound()
            else:
                while self.sound_active:
                    logging.debug("waiting until sound play is finish")
                    time.sleep(1)
        logger.warning("sound play done - now playing next")

        self.sound_active = True
        # set output high in order to turn on amplifier
        self.toggle_amp_pin(1)
        time.sleep(0.3)
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_file)
        logger.debug("now playing file: {}".format(mp3_file))
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            if self.stop_sound:
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                logger.debug('mp3 alarm turned off via button pressed')
                break
            else:
                continue
        time.sleep(0.5)
        # set output low in order to turn off amplifier
        self.toggle_amp_pin(0)
        pygame.mixer.quit()
        self.sound_active = False
        self.stop_sound = False

    def say(self, text, force=False):
        """synthesizes the given text to speech"""
        if self.sound_active:
            if force:
                self.stopping_sound()
            else:
                while self.sound_active:
                    logging.debug("waiting until sound play is finish")
                    time.sleep(1)
        logger.warning("sound play done - now playing next")

        self.sound_active = True
        # set output high in order to turn on amplifier
        self.toggle_amp_pin(1)
        time.sleep(0.3)
        engine = pyttsx.init()
        engine.setProperty('rate', 125)
        # remove "pass" and uncomment next line in order to enable this function
        engine.say(text)
        engine.runAndWait()
        time.sleep(0.2)
        # set output low in order to turn off amplifier
        self.toggle_amp_pin(0)
        self.sound_active = False

    def adjust_volume(self, value):
        """adjusts the audio volume by the given value (0-100%)"""
        logger.debug('adjusting volume')
        volume_command = str('amixer set PCM -- ' + str(value) + '%')
        os.system(volume_command)

    def play_wakeup_music(self):
        """find all mp3 files in the folder /home/pi/music
        and play one of them at random"""
        list_of_music_files = []
        for track in os.listdir(project_path + '/music'):
            if track.endswith(".mp3"):
                list_of_music_files.append(str(project_path + '/music/' + str(track)))

        # figure out random track of the found mp3 files
        random_track = randint(0, len(list_of_music_files)-1)

        self.play_mp3_file(list_of_music_files[random_track])

    def play_online_stream(self, force=False):
        """plays online radio using mpc. Press button to stop. Edit mpc playlist by:
        'mpc add filename', 'mpc playlist', 'mpc clear', 'mpc play', 'mpc stop'."""
        if self.sound_active:
            if force:
                self.stopping_sound()
            else:
                while self.sound_active:
                    logging.debug("waiting until sound play is finish")
                    time.sleep(1)
        logger.warning("sound play done - now playing next")

        self.sound_active = True

        logger.debug('now playing internet radio')
        # set output high in order to turn on amplifier
        self.toggle_amp_pin(1)
        time.sleep(0.3)
        os.system('mpc play')

        while True:
            if self.stop_sound is False:
                pass
            else:
                break

        os.system('mpc stop')
        time.sleep(0.5)
        # set output low in order to turn off amplifier
        self.toggle_amp_pin(0)
        logger.debug('internet radio alarm turned off')
        self.sound_active = False
        self.stop_sound = False
