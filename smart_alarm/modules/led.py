import time
import os
import sys
sys.path.append(os.path.abspath("/home/pi/APA102_Pi"))
import colorschemes
import logging


# read environmental variable for project path
project_path = os.environ['smart_alarm_path']
logger = logging.getLogger(__name__)


class LEDs(object):
    """
    LEDs class: manages the implementation of the 'wake-up'-leds.
    Makes us of tinues APA102_Pi library: https://github.com/tinue/APA102_Pi
    """

    def __init__(self):
        """init functions: set variables and start adafruit dotstar class"""
        # write to error.log file
        logger.info('led-module initialized')
        self.number_of_leds = 9
        self.stop_led = False
        self.leds_active = False

    def stopping_leds(self):
        """stops leds when button is pressed"""
        logger.debug('leds are being stopped')
        logger.debug('now stopping leds')
        self.stop_led = True

    def rainbow(self, brightness, duration_time):
        """colorful rainbow cycling through all leds"""
        if self.stop_led:
            logger.debug('skipping led rainbow, since button was pressed')
            return
        logger.debug('running led rainbow with brightness {}/10 for {}sec'.format(brightness, duration_time))
        self.leds_active = True
        clock = 0
        start = time.time()
        while clock < duration_time and self.stop_led is False:
            rainbow = colorschemes.Rainbow(numLEDs=self.number_of_leds, pauseValue=0.02, numStepsPerCycle=255,
                                           numCycles=1, globalBrightness=brightness)
            rainbow.start()
            clock = time.time() - start
        self.leds_active = False

    def white_blinking(self, duration_time):
        """most bright white blinking, finally you should wake up"""
        if self.stop_led:
            logger.debug('skipping led white blinking, since button was pressed')
            return
        logger.debug('running led white blinking')
        self.leds_active = True
        clock = 0
        start = time.time()
        while clock < duration_time and self.stop_led is False:
            blinking = colorschemes.Solid(numLEDs=self.number_of_leds, pauseValue=0.05, numStepsPerCycle=1,
                                          numCycles=1)
            blinking.start()
            time.sleep(0.05)
            clock = time.time() - start
        self.leds_active = False

    def wake_up_light_show(self, duration_time):
        """combination of earlier functions, adjust when needed"""
        self.rainbow(1, duration_time/4)
        self.rainbow(3, duration_time/4)
        self.rainbow(10, duration_time/4)
        self.white_blinking(duration_time/4)
