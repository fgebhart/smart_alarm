import time
import urllib2
import pygame
import pyttsx
import RPi.GPIO as GPIO
from xml.dom import minidom
from xml.dom.minidom import Node
from Adafruit_LED_Backpack import AlphaNum4


# configure RPI GPIO. Make sure to use 1k ohms resistor to protect input pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Create display instance on default I2C address (0x70) and bus number.
display = AlphaNum4.AlphaNum4()

# Initialize the display. Must be called once before using the display.
display.begin()

# set decimal point flag - for decimal point blinking
point = False


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
        time.sleep(0.2)
        # increase counter in order to end the loop at the end of the message
        counter += 1


def display_show_time(time):
    """displays the given time"""
    # display actual time using adafruit library
    display.print_number_str(time)


def download_file(link_to_file):
    """function for downloading files"""
    file_name = link_to_file.split('/')[-1]
    u = urllib2.urlopen(link_to_file)
    f = open(file_name, 'wb')
    print "Downloading: %s" % file_name

    # buffer the file in order to download it
    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)

    f.close()
    # XML file now is saved (to the same directory like this file)
    print "download done"
    return file_name


def find_most_recent_news_url_in_xml_file(xml_file):
    """parse the xml file in order to find the url in the first item,
    corresponding to the most_recent_news_url"""
    # run XML parser and create a list with all 'enclosure' item urls
    xmldoc = minidom.parse(xml_file)
    itemlist = xmldoc.getElementsByTagName('enclosure')

    # search for 'url' and take the first list element
    most_recent_news_url = itemlist[0].attributes['url'].value

    return most_recent_news_url


def play_mp3_file(mp3_file):
    """using pygame lib in order to play mp3 sound files"""
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_file)
    print "now playing file: ", mp3_file
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
        if button_pressed():
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            print 'alarm turned off'
            display_scroll('*GOOD MORNING*', 1)
            break
        else:
            continue
    pygame.mixer.quit()


def say(text):
    """synthesizes the given text to speech"""
    engine = pyttsx.init()
    engine.setProperty('rate', 150)
    # remove "pass" and uncomment next line in order to enable this function
    engine.say(text)
    engine.runAndWait()


def read_xml_file(xml_file):
    """reads the xml file, parse it and save the fetched data to the list
    called 'xml_data'."""
    xmldoc = minidom.parse(xml_file)
    xml_data = []

    for elem in xmldoc.getElementsByTagName('data'):
        for x in elem.childNodes:
            if x.nodeType == Node.ELEMENT_NODE:
                xml_data.append(str(x.childNodes[0].data))

    return xml_data


def button_pressed():
    """check if button is pressed. If so return True, if not False"""
    counter = 0
    activated = False
    while counter < 20:
        if GPIO.input(11) == 1:
            activated = True
        else:
            pass
        time.sleep(0.05)
        counter += 1
    return activated


def get_time_difference(time_now, alarm_time):
    """calculate the time difference between the two given times
    and return the result in format hours and minutes"""
    t1h = time_now[:2]
    t1m = time_now[2:]
    t2h = alarm_time[:2]
    t2m = alarm_time[2:]

    diff = (int(t2m) + 60 * int(t2h)) - (int(t1m) + 60 * int(t1h))
    hours = diff//60
    minutes = diff%60
    if hours < 0:
        hours += 24
    return hours, minutes


# start smart alarm:
# display_scroll('*WELCOME*', 1)

new_xml_data = read_xml_file('xml_dummy.xml')
alarm_time = None


while True:
    # organise time format
    now = time.strftime("%H%M")

    # reset display
    display.clear()

    # read xml file and store data to xml_data
    xml_data = read_xml_file('xml_dummy.xml')

    # check if alarm time was edited:
    if xml_data[0] == new_xml_data[0]:
        pass    # since the file did non change
    else:
        alarm_time = xml_data[0]
        print 'alarm time changed-set it now'

        hours, minutes = get_time_difference(now, alarm_time)

        display_message = str('* TIME TO ALARM ' + str(hours) + 'h' + str(minutes) + 'm * ')
        display_scroll(display_message, 1)
        print('time to alarm: %sh %sm' % (hours, minutes))
        text_to_say = str('t minus ' + str(hours) + ' hours and ' + str(minutes) + ' minutes till alarm')
        say(text_to_say)

    if alarm_time is not None:
        time_to_alarm = int(alarm_time) - int(now)
        if time_to_alarm == 0:
            play_mp3_file('cartoon001.mp3')
            alarm_time = None

    display_show_time(now)

    # manage to get the decimal point blinking
    if point:
        display.set_decimal(1, point)
        point = False
    else:
        display.set_decimal(1, point)
        point = True

    # write content to display
    display.write_display()

    # update xml file in order to find differences in next loop
    new_xml_data = xml_data

    # check if button is pressed, which takes 1 second
    if button_pressed():
        print 'button pressed - have some action here'
