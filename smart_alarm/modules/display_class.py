from Adafruit_LED_Backpack import AlphaNum4
import time
import logging
import os


# read environmental variable for project path
project_path = os.environ['smart_alarm_path']
logger = logging.getLogger(__name__)


class Display(object):
    """
    Display class: manages all methods concerning the alphanumeric display.
    """

    def __init__(self):
        """init function: imports adafruit alphanumeric display class and begins"""
        # write to error.log file
        self.display_lib = AlphaNum4.AlphaNum4()
        self.display_lib.begin()
        self.display_in_use = False
        logger.info('display-module initialized')

    def scroll(self, message, number_of_iteration):
        """scrolls the given message from right to left through the display.
        Set number_f_iterations = 1, in order to display the message just once."""
        self.display_in_use = True
        pos = 0
        counter = 0
        message = "   " + message + "   "
        # loop to scroll through the message
        while counter < (len(message) - 3) * number_of_iteration:
            # Clear the display buffer.
            self.display_lib.clear()
            # Print a 4 character string to the display buffer.
            self.display_lib.print_str(message[pos:pos + 4])
            # Write the display buffer to the hardware.  This must be called to
            # update the actual display LEDs.
            self.display_lib.write_display()
            # Increment position. Wrap back to 0 when the end is reached.
            pos += 1
            if pos > len(message) - 4:
                pos = 0
            # Delay for half a second
            time.sleep(0.12)
            # increase counter in order to end the loop at the end of the message
            counter += 1
        self.display_in_use = False

    def show_time(self, time):
        """displays the given time using adafruit library"""
        if self.display_in_use:
            return
        self.display_lib.print_number_str(time)

    def set_brightness(self, value):
        """change the displays brightness. Value is between 0 and 15"""
        self.display_lib.set_brightness(value)

    def clear_class(self):
        """clears the display, in order to accept new content
        (note that it needs to be called different to -pythonic- 'clear')"""
        self.display_lib.clear()

    def write(self):
        """writes all the earlier given content to the display,
        needs to be done at every end of the loop"""
        self.display_lib.write_display()

    def set_decimal(self, pos, decimal):
        """activates the decimal point. First argument is the poosition
        from 0 to 3, second is True or False."""
        if self.display_in_use:
            return
        self.display_lib.set_decimal(pos, decimal)

    def set_segment(self, led, value):
        """Sets specified LED (value of 0 to 127) to the specified value, 0/False
        for off and 1 (or any True/non-zero value) for on."""
        self.display_lib.set_led(led, value)

    # The following functions are not mandatory, because they just contain little display games

    def shutdown(self, number_of_iterations):
        """goes from top segments to bottom segments"""
        self.display_in_use = True
        delay = 0.1
        sequence1 = [0, 8, 9, 12, 11, 3]
        sequence2 = [0, 10, 9, 12, 13, 3]
        counter = 0
        while counter < number_of_iterations:
            for a in range(len(sequence1)):
                self.clear_class()
                for i in range(4):
                    self.set_segment(sequence1[a] + (i * 16), 1)
                    self.set_segment(sequence2[a] + (i * 16), 1)
                self.write()
                time.sleep(delay)
            counter += 1
        self.display_in_use = False

    def snake(self, number_of_iterations):
        """runs a snake through the display from left to right"""
        self.display_in_use = True
        counter = 0
        delay = 0.02
        loop = [3, 2, 1, 0, 5, 4, 3, 14]
        while counter < number_of_iterations:
            for z in range(4):
                for i in range(len(loop)):
                    self.clear_class()
                    self.set_segment(loop[i] + (z * 16), 1)
                    self.write()
                    time.sleep(delay)
            counter += 1
        self.display_in_use = False

    def big_stars(self, number_of_iterations):
        """big stars circling in each digit"""
        self.display_in_use = True
        delay = 0.03
        counter = 0
        segment1 = [6, 8, 9, 10, 7, 13, 12, 11]
        segment2 = [7, 13, 12, 11, 6, 8, 9, 10]
        while counter < number_of_iterations:
            for a in range(len(segment1)):
                self.clear_class()
                for i in range(4):
                    self.set_segment(segment1[a] + (i * 16), 1)
                    self.set_segment(segment2[a] + (i * 16), 1)
                self.write()
                time.sleep(delay)
            counter += 1
        self.display_in_use = False


