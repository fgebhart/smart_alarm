import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    print "button is: ", GPIO.input(11)
    time.sleep(0.4)

#hallo
