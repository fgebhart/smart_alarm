import time
from Adafruit_LED_Backpack import AlphaNum4


# Create display instance on default I2C address (0x70) and bus number.
display = AlphaNum4.AlphaNum4()

# Initialize the display. Must be called once before using the display.
display.begin()

# set decimal point flag - for decimal point blinking
point = False

# introduction message
message = '   DISPLAY TIME   '
pos = 0
counter = 0
# loop to scroll through the message
while counter < len(message)-3:
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
    time.sleep(0.2)
    # increase counter in order to end the loop at the end of the message
    counter += 1

# loop displaying the actual time
while True:
    # organise time format
    now = time.strftime("%H%M")

    # reset display
    display.clear()

    # display actual time
    display.print_number_str(now)

    # manage to get the decimal point blinking
    if point:
        display.set_decimal(1, point)
        point = False
    else:
        display.set_decimal(1, point)
        point = True

    # write content to display
    display.write_display()
    # add time delay concerning the blinking
    time.sleep(1)




