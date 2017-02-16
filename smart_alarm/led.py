import time
import colorsys
from dotstar import Adafruit_DotStar
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
        """init functions: set variables and start adafruit dotstar class"""
        # write to error.log file
        logger.info('-> led-module initialized')
        # initialize start variables
        self.numpixels = 18
        self.datapin   = 10
        self.clockpin  = 11
        self.strip     = Adafruit_DotStar(self.numpixels, self.datapin, self.clockpin)
        # Initialize the library (must be called once before other functions).
        self.strip.begin()
        self.strip.setBrightness(64) # Limit brightness to ~1/4 duty cycle


    def loop_rgb(self, duration_time):
        """runs 10 leds with red, then green and then blue in a loop"""
        clock = 0
        start = time.time()
        head = 0  # Index of first 'on' pixel
        tail = -10  # Index of last 'off' pixel
        color = 0xFF0000  # 'On' color (starts red)

        while clock < duration_time:  # Loop forever
            self.strip.setPixelColor(head, color)  # Turn on 'head' pixel
            self.strip.setPixelColor(tail, 0)  # Turn off 'tail'
            self.strip.show()  # Refresh strip
            time.sleep(1.0 / 50)  # Pause 20 milliseconds (~50 fps)

            head += 1  # Advance head position
            if (head >= self.numpixels):  # Off end of strip?
                head = 0  # Reset to start
                color >>= 8  # Red->green->blue->black
                if (color == 0): color = 0xFF0000  # If black, reset to red

                tail += 1  # Advance tail position
            if (tail >= self.numpixels): tail = 0  # Off end? Reset
            clock = time.time() - start