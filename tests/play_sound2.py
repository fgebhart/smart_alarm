import pygame
import RPi.GPIO as GPIO
import time

# set button input pin
button_input_pin = 24
# set pin for amplifier switch
amp_switch_pin = 12

# configure RPI GPIO
GPIO.setmode(GPIO.BCM)
# set pin to output
GPIO.setup(amp_switch_pin, GPIO.OUT)
GPIO.setup(button_input_pin, GPIO.IN)


button_pressed = False

# Define a threaded callback function to run in another thread when events are detected
def button_callback(channel):
    global  button_pressed       # put in to debounce

    if GPIO.input(button_input_pin):  # if port 24 == 1
        print "button pressed"
        button_pressed = True
        time.sleep(5)
        button_pressed = False

GPIO.add_event_detect(button_input_pin, GPIO.BOTH, callback=button_callback)


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
        if button_pressed == True:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            print 'alarm turned off'
            break
        else:
            continue
    # set ouput low in order to turn off amplifier
    time.sleep(0.5)
    GPIO.output(amp_switch_pin, 0)
    pygame.mixer.quit()
    print 'quit play function'


try:
    print 'start try'

    play_mp3_file("/home/pi/smart_alarm/smart_alarm/sounds/blop.mp3")

    print 'end try'

finally:
    print '\nturning off amp'
    #GPIO.output(amp_switch_pin, 0)


