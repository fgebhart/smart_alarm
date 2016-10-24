from Adafruit_LED_Backpack import AlphaNum4
import time


class Display(object):
    """
    asdfasdfasdf
    """

    def __init__(self):
        # init fuction
        self.display_lib = AlphaNum4.AlphaNum4()
        self.display_lib.begin()



    def scroll(self, message, number_of_iteration):
        """scrolls the given message from right to left through the display.
        Set number_f_iterations = 1, in order to display the message just once."""
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
            # Delay for half a second.
            time.sleep(0.12)
            # increase counter in order to end the loop at the end of the message
            counter += 1


    def show_time(self, time):
        """displays the given time"""
        # display actual time using adafruit library
        self.display_lib.print_number_str(time)

    def set_brightness(self, value):
        """change the displays brightness. Value is between 0 and 15"""
        # self.display_chip.begin()

        # adjust the brightness by the given value
        self.display_lib.set_brightness(value)
        print 'brightness: ', value

    def clear_class(self):
        self.display_lib.clear()
        print 'display cleared'


    def write(self):
        self.display_lib.write_display()

        print 'display written'

    def set_decimal(self, pos, decimal):
        self.display_lib.set_decimal(pos, decimal)
        print 'display decimal set!'






