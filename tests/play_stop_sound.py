import pygame
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def button_pressed():
    """check if button is pressed. If so return True, if not False"""
    counter = 0
    activated = False
    while counter < 20:
        if GPIO.input(11) == 1:
            activated = True
        else:
            pass
        time.sleep(0.05)
        counter += 1
    return activated


def play_mp3_file(mp3_file):
    """using pygame lib in order to play mp3 sound files"""
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    print "now playing file: ", mp3_file
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        if button_pressed():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            break
        else:
            continue


play_mp3_file("cartoon001.mp3")






