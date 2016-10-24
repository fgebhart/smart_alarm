#import display_class
from Adafruit_LED_Backpack import AlphaNum4, HT16K33

display = AlphaNum4.AlphaNum4()


display.clear()

display.print_number_str('1200')

# display.write()

