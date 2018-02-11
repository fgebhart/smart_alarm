import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


def read_photocell():
    """reads the surrounding brightness using the
    connected photocell and transforms the values to
    a scale of 0 - 15 in order to adjust the displays
    brightness"""

    photocell_input_pin = 20
    upper_limit = 400
    lower_limit = 1
    counter = 0
    summed_up_brightness = 0
    max_iterations = 5

    while counter < max_iterations:
        brightness = 0
        # needs to be put low first, so the capacitor is empty
        GPIO.setup(photocell_input_pin, GPIO.OUT)
        GPIO.output(photocell_input_pin, GPIO.LOW)

        time.sleep(0.1)

        # set to input to read out
        GPIO.setup(photocell_input_pin, GPIO.IN)
        # increases the brightness variable depending on the charge
        # of the capacitor (400 = dark; 0 = bright)
        while GPIO.input(photocell_input_pin) == GPIO.LOW:
            brightness += 1

        summed_up_brightness = summed_up_brightness + brightness
        counter += 1

    # calculate the mean of the last 'max_iterations' measurements:
    brightness = summed_up_brightness / max_iterations

    # turn values up-side down: dark-to-bright
    brightness = upper_limit - brightness

    # limit the value of measured brightness
    if brightness > upper_limit:
        brightness = brightness - (brightness - upper_limit)
    elif brightness < lower_limit:
        brightness = brightness - brightness + lower_limit

    # scale brightness to the scale of 0 - 15
    brightness = brightness / (upper_limit / 15)

    return brightness


while True:
    print read_photocell()
