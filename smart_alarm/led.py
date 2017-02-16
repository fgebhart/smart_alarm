import time
import os
import sys
sys.path.append(os.path.abspath("/home/pi/APA102_Pi"))
import colorschemes
import logging


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
    LEDs class: manages the implementation of the 'wake-up'-leds.
    Makes us of tinues APA102_Pi library: https://github.com/tinue/APA102_Pi
    """

    def __init__(self):
        """init functions: set variables and start adafruit dotstar class"""
        # write to error.log file
        logger.info('-> led-module initialized')
        self.number_of_leds = 9

    def rainbow(self, brightness, duration_time):
        """colorful rainbow cycling through all leds"""
        clock = 0
        start = time.time()
        while clock < duration_time:
            rainbow = colorschemes.Rainbow(numLEDs=self.number_of_leds, pauseValue=0.05, numStepsPerCycle=255,
                                           numCycles=2, globalBrightness=brightness)
            rainbow.start()
            clock = time.time() - start

    def white_blinking(self, duration_time):
        """most bright white blinking, finally you should wake up"""
        clock = 0
        start = time.time()
        while clock < duration_time:
            blinking = colorschemes.Solid(numLEDs=self.number_of_leds, pauseValue=0.05, numStepsPerCycle=1,
                                          numCycles=1)
            blinking.start()
            time.sleep(0.05)
            clock = time.time() - start