import time
from Adafruit_LED_Backpack import AlphaNum4, HT16K33



# Create display instance on default I2C address (0x70) and bus number.
display = AlphaNum4.AlphaNum4()

# Initialize the display. Must be called once before using the display.
display.begin()



def display_scroll(message, number_of_iteration):
    """scrolls the given message from right to left through the display.
    Set number_f_iterations = 1, in order to display the message just once."""
    pos = 0
    counter = 0
    message = "   " + message + "   "
    # loop to scroll through the message
    while counter < (len(message)-3)*number_of_iteration:
        # Clear the display buffer.
        display.clear()
        # Print a 4 character string to the display buffer.
        display.print_str(message[pos:pos+4])
        # Write the display buffer to the hardware.  This must be called to
        # update the actual display LEDs.
        display.write_display()
        # Increment position. Wrap back to 0 when the end is reached.
        pos += 1
        if pos > len(message)-4:
            pos = 0
        # Delay for half a second.
        time.sleep(0.12)
        # increase counter in order to end the loop at the end of the message
        counter += 1


def display_show_time(time):
    """displays the given time"""
    # display actual time using adafruit library
    display.print_number_str(time)


def set_display_brightness(value):
    """change the displays brightness. Value is between 0 and 15"""
    driver_chip = HT16K33.HT16K33()
    driver_chip.begin()


    # adjust the brightness by the given value
    driver_chip.set_brightness(value)
