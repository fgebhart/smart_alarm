__author__ = 'Fabian Gebhart'


"""
SMART ALARM

Features of this python script so far:
- displaying the actual time on the alphanumeric display
- scrolling text messages through the display
- figuring out the most recent dlf news
- download the news
- play the news
- stop the news play with a tactile button connected to the GPIOs
- talk to you, using text to speech synthesis
- reading the user settings from a xml file (created over html server)
- accept individual wake-up message, if there is none use default
    wake-up message
- delete the unneeded old news file
- display if alarm is activated by turning last decimal point on
- using multithreading in order to:
    * enable decimal point blinking while news are played
    * download news file while saying individual wake-up message
- choose between "news" and "music"
- offline mp3 wake-up music enabled
- dim display brightness, since default value is too damn bright for sleeping
- enabled volume adjustment
-

Todo:
- enable internet radio / music streaming as possible wake-up sound
-
"""


import time
import urllib2
import pygame
import pyttsx
import RPi.GPIO as GPIO
from xml.dom import minidom
from Adafruit_LED_Backpack import AlphaNum4, HT16K33
import threading
from read_xml import read_xml_file_list, read_xml_file_namedtuple
import os
from random import randint


# configure RPI GPIO. Make sure to use 1k ohms resistor to protect input pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Create display instance on default I2C address (0x70) and bus number.
display = AlphaNum4.AlphaNum4()

# Initialize the display. Must be called once before using the display.
display.begin()

# set decimal point flag - for decimal point blinking
point = False

# dlf podcast link to XML file. Correct if modified!
dlf_news_url = "http://www.deutschlandfunk.de/podcast-nachrichten.1257.de.podcast.xml"


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
        if GPIO.input(11) == 1:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            print 'alarm turned off'
            break
        else:
            continue
    pygame.mixer.quit()


def say(text):
    """synthesizes the given text to speech"""
    engine = pyttsx.init()
    engine.setProperty('rate', 115)
    # remove "pass" and uncomment next line in order to enable this function
    engine.say(text)
    engine.runAndWait()


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


def update_settings(xml_file):
    """fetches the recent settings via read_xml.py and stores the
    new content of the xml file to the corresponding variables"""
    settings = read_xml_file_namedtuple(xml_file)

    alarm_active = settings.alarm_active
    alarm_time = settings.time
    content = settings.content
    alarm_days = settings.days
    individual_msg_active = settings.individual_message
    individual_message = settings.text
    volume = settings.volume

    return alarm_active, alarm_time, content, alarm_days, individual_msg_active, individual_message, volume


def set_ind_msg(ind_msg_active, ind_msg_text):
    """takes and checks the to two arguments and sets the
    individual message"""
    if ind_msg_active == '0':
        # ind msg is deactivated, therefore create default message
        print 'ind msg deactivated - construct default msg'
        sayable_time = str(time.strftime("%H %M"))
        today = time.strftime('%A')
        standard_message = 'good morning. It is ' + today + '  ' + sayable_time
        individual_message = standard_message
    else:
        individual_message = ind_msg_text

    return individual_message


def delete_old_files(time_to_alarm, alarm_active):
    """checks for old mp3 files and deletes them"""
    # find all mp3 files and append them to a list
    list_of_mp3_files = []
    for file in os.listdir("/home/pi"):
        if file.startswith("nachrichten"):
            list_of_mp3_files.append(file)

    # either if the time_to_alarm is 10 minutes away from going offf, or if it is deactivated
    if time_to_alarm < -10 or time_to_alarm > 10 or alarm_active == '0':
        for file in range(len(list_of_mp3_files)):
            os.remove(list_of_mp3_files[file])


def play_wakeup_music():
    """find all mp3 files in the folder /home/pi/music
    and play one of them at random"""
    list_of_music_files = []
    for file in os.listdir("/home/pi/"):
        if file.endswith(".mp3"):
            list_of_music_files.append(file)

    # figure out random track of the found mp3 files
    random_track = randint(0, len(list_of_music_files)-1)

    play_mp3_file(list_of_music_files[random_track])


def set_display_brightness(value):
    """change the displays brightness. Value is between 0 and 15"""
    driver_chip = HT16K33.HT16K33()
    driver_chip.begin()

    # adjust the brightness by the given value
    driver_chip.set_brightness(value)


def adjust_volume(value):
    """adjusts the audio volume by the given value (0-100%)"""
    volume_command = str('amixer set PCM -- ' + str(value) + '%')
    os.system(volume_command)
    play_mp3_file('/home/pi/music/blop.mp3')


# read out the settings in 'xml_dummy_xml' from the same folder
xml_data = read_xml_file_list('xml_dummy.xml')

# assign the xml data to the corresponding variables
alarm_active, alarm_time, content, alarm_days, individual_msg_active, individual_message, volume = update_settings('xml_dummy.xml')

# set flag for just played the news
just_played_alarm = False

# start smart alarm:
display_scroll('*WELCOME*', 1)

# change display brightness
set_display_brightness(0)

while True:
    # organise time format
    now = time.strftime("%H%M")

    # reset display
    display.clear()

    # read xml file and store data to xml_data
    new_xml_data = read_xml_file_list('xml_dummy.xml')

    # check if xml file was updated. If so, update the variables
    if xml_data != new_xml_data:
        print 'file changed - update settings'
        # set the updated variables
        alarm_active, alarm_time, content, alarm_days, individual_msg_active, individual_message, volume = update_settings('xml_dummy.xml')

        adjust_volume(volume)


    time_to_alarm = int(int(str(alarm_time[:2]) + str(alarm_time[3:]))) - int(now)

    #print 'time to alarm =', time_to_alarm

    # check if alarm is activated
    if alarm_active == '1' and just_played_alarm == False:     # alarm is activated start managing to go off
        # find the actual day of the weel in format of a number in order to compare to the xml days variable
        today_nr = time.strftime('%w')

        if today_nr in alarm_days:      # check if current day is programmed to alarm
            # alarm is set to go off today, calculate the remaining time to alarm

            if time_to_alarm == 0:

                # check if news or audio (offline mp3) is programmed
                if content == 'news':

                    # display the current time
                    display_show_time(now)
                    # write content to display
                    display.write_display()

                    # set the updated individual wake-up message in order to play it
                    individual_message = set_ind_msg(individual_msg_active, individual_message)

                    # wake up with individual message
                    z = threading.Thread(target=say, args=(individual_message,))
                    z.start()

                    # download dlf_xml_file according to the dlf_news_url
                    dlf_xml_file = download_file(dlf_news_url)

                    # now parse the dlf_xml_file in order to find the most_recent_news_url
                    most_recent_news_url = find_most_recent_news_url_in_xml_file(dlf_xml_file)

                    # download the most recent news_mp3_file according to the most_recent_news_url
                    news_mp3_file = download_file(most_recent_news_url)

                    # wait untill thread z (say) is done
                    while z.isAlive() == True:
                        time.sleep(0.5)

                    # play the most recent news_mp3_file
                    a = threading.Thread(target=play_mp3_file, args=(news_mp3_file,))
                    a.start()

                    # set flag for just played alarm
                    just_played_alarm = True


                elif content == 'music':
                    # since music is preferred, play the offline mp3 files

                    print 'now playing music'

                    # display the current time
                    display_show_time(now)
                    # write content to display
                    display.write_display()

                    # set the updated individual wake-up message in order to play it
                    individual_message = set_ind_msg(individual_msg_active, individual_message)

                    # wake up with individual message
                    say(individual_message)

                    play_wakeup_music()

                    # set flag for just played alarm
                    just_played_alarm = True


                elif content == 'internet-radio':
                    # since internet-radio is preferred, play the online stream
                    print 'here comes the internet radio'
                    # display the current time
                    display_show_time(now)
                    # write content to display
                    display.write_display()

                    # NOTHING HERE YET!

                else:
                    pass


    if time_to_alarm != 0:
        # set just_played_alarm back to False in order to not miss the next alarm
        just_played_alarm = False

    #print 'just_played_alarm = ', just_played_alarm

    # display the current time
    display_show_time(now)

    # manage to get the decimal point blinking
    if point:
        display.set_decimal(1, point)
        point = False
    else:
        display.set_decimal(1, point)
        point = True

    # check if alarm is active and set third decimal point
    if alarm_active == '1':
        display.set_decimal(3, True)
    else:
        # else if alarm is deactivated, turn last decimal point off
        display.set_decimal(3, False)

    # write content to display
    display.write_display()

    # delete old and unneeded mp3 files
    delete_old_files(time_to_alarm, alarm_active)

    # update xml file in order to find differences in next loop
    xml_data = new_xml_data

    time.sleep(1)
