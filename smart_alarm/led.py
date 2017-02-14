import time
import colorsys
from neopixel import *
import logging
import os


# read environmental variable for project path
project_path = os.environ['smart_alarm_path']

# enable python logging module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create a file handler
handler = logging.FileHandler(str(project_path) + '/error.log')
handler.setLevel(logging.DEBUG)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)


class LEDs(object):
    """
    LEDs class: manages the implementation of the 'wake-up'-leds
    """

    def __init__(self):
        """init functions: set variables and start adafruit neopixles class"""
        # write to error.log file
        logger.info('-> led-module initialized')
        # initialize start variables
        self.LED_COUNT = 1              # Number of LED pixels.
        self.LED_PIN = 12               # GPIO pin connected to the pixels (must support PWM!).
        self.LED_FREQ_HZ = 800000       # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA = 5                # DMA channel to use for generating signal (try 5)
        self.LED_BRIGHTNESS = 255       # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT = False         # True to invert the signal (when using NPN transistor level shift)
        # start adafruit neopixles class
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS)
        # Intialize the library (must be called once before other functions).
        self.strip.begin()


    # Define functions which animate LEDs in various ways.
    def color_wipe(self, color, wait_ms):
        """Wipe color across display a pixel at a time.
        Use wait_ms=50 for nice visible effect."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()
            time.sleep(wait_ms/1000.0)

    def increase_brightness(self, maximum, wait_ms):
        """slightly increases the brightness of all LEDs"""
        for i in range(maximum):
            self.color_wipe(Color(0,i,0), 0)
            time.sleep(wait_ms/1000.0)

    def theater_chase(self, color, wait_ms=50, iterations=10):
        """Movie theater light style chaser animation."""
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, color)
                    self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    def wheel(self, pos):
        """Generate rainbow colors across 0-255 positions."""
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)

    def rainbow(self, wait_ms=20, iterations=1):
        print 'now running rainbow'
        """Draw rainbow that fades across all pixels at once."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((i+j) & 255))
                self.strip.show()
            time.sleep(wait_ms/1000.0)

    def rainbow_cycle(self, wait_ms=20, iterations=5):
        """Draw rainbow that uniformly distributes itself across all pixels."""
        for j in range(256*iterations):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, self.wheel((int(i * 256 / self.strip.numPixels()) + j) & 255))
                self.strip.show()
            time.sleep(wait_ms/1000.0)

    def theater_chase_rainbow(self, wait_ms=50):
        """Rainbow movie theater light style chaser animation."""
        for j in range(256):
            for q in range(3):
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, self.wheel((i+j) % 255))
                self.strip.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, self.strip.numPixels(), 3):
                    self.strip.setPixelColor(i+q, 0)

    def wake_up(self, duration_time):
        """5 minutes of colorful light show in order to wake up"""
        clock = 0
        start = time.time()
        self.color_wipe(Color(0, 1, 0), 400)
        self.color_wipe(Color(0, 50, 0), 400)
        self.color_wipe(Color(0, 255, 0), 400)
        while clock < duration_time * 0.50:
            print 'clock: ', clock
            self.rainbow_cycle(iterations=1)
            clock = time.time() - start
        while clock < duration_time:
            print 'clock: ', clock
            self.theater_chase(Color(255, 255, 255), wait_ms=100, iterations=5)
            clock = time.time() - start
        # turn off all leds
        self.color_wipe(Color(0,0,0), 0)

    def soft_wake_up(self, duration_time):
        """softly wakes you up"""
        clock = 0
        # do something here
        self.increase_brightness(20, 200)
        self.increase_brightness(50, 100)
        self.increase_brightness(255, 50)

        start = time.time()
        while clock < duration_time * 0.50:
            print 'clock: ', clock
            self.rainbow_cycle(iterations=1)
            clock = time.time() - start
        while clock < duration_time:
            print 'clock: ', clock
            self.theater_chase(Color(255, 255, 255), wait_ms=100, iterations=5)
            clock = time.time() - start
        # turn off all leds
        self.color_wipe(Color(0,0,0), 0)

    def hsv2rgb(self, h, s, v):
        return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


