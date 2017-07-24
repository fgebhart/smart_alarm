import pyttsx
import time
import RPi.GPIO as GPIO


# set pin for amplifier switch
amp_switch_pin = 5

# turn off GPIO warnings
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
# set pin to output
GPIO.setup(amp_switch_pin, GPIO.OUT)

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


while True:
    print 'please enter your text message'
    text = raw_input('\n->')

    say(text)
    time.sleep(1)