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
- enabled internet radio / music streaming as possible wake-up sound
- button interrupt instead of waiting
- turn off and on amplifier in order to suppress background noise
-

Todo:
- find internet radio station without commercials and too much talk
- enable function to run when button is pressed without alarm running
    * for example 'say time left till alarm'
- Fix Error: 'socket.error: [Errno 98] Address already in use' in python_server.py



Possible internet radio station (working witch MPC):
- http://streaming.radionomy.com/The-Smooth-Lounge?lang=en-US%2cen%3bq%3d0.8%2cde%3bq%3d0.6
-

"""


import urllib2
import RPi.GPIO as GPIO
import threading
# from read_xml import read_xml_file_list, read_xml_file_namedtuple
from display_class import Display
from sounds import *
from xml_belongings import *
from settings import *
import time
import os


# import dispay_class
display = Display()

# set button input pin
button_input_pin = 24
# set pin for amplifier switch
amp_switch_pin = 12

# turn off GPIO warnings
GPIO.setwarnings(False)
# configure RPI GPIO. Make sure to use 1k ohms resistor to protect input pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_input_pin, GPIO.IN)
# set pin to output
GPIO.setup(amp_switch_pin, GPIO.OUT)
# set output low in order to turn off amplifier and nullify noise
GPIO.output(amp_switch_pin, 0)


# dlf podcast link to XML file. Correct if modified!
dlf_news_url = "http://www.deutschlandfunk.de/podcast-nachrichten.1257.de.podcast.xml"


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
    for file in os.listdir('/home/pi/smart_alarm/smart_alarm'):
        if file.startswith('nachrichten'):
            list_of_mp3_files.append('/home/pi/smart_alarm/smart_alarm/' + str(file))

    # either if the time_to_alarm is 10 minutes away from going off, or if it is deactivated
    if time_to_alarm < -10 or time_to_alarm > 10 or alarm_active == '0':
        for file in range(len(list_of_mp3_files)):
            os.remove(list_of_mp3_files[file])


def read_photocell():
    """reads the surrounding brightness using the
    connected photocell and transforms the values to
    a scale of 0 - 15 in order to adjust the displays
    brightness"""

    photocell_input_pin = 20
    upper_limit = 400
    lower_limit = 1
    counter = 0
    summed_up_brightness = 0
    max_iterations = 5

    while counter < max_iterations:
        brightness = 0
        # needs to be put low first, so the capacitor is empty
        GPIO.setup(photocell_input_pin, GPIO.OUT)
        GPIO.output(photocell_input_pin, GPIO.LOW)

        time.sleep(0.1)

        # set to input to read out
        GPIO.setup(photocell_input_pin, GPIO.IN)
        # increases the brightness variable depending on the charge
        # of the capacitor (400 = dark; 0 = bright)
        while GPIO.input(photocell_input_pin) == GPIO.LOW:
            brightness += 1

        summed_up_brightness = summed_up_brightness + brightness
        counter += 1

    # calculate the mean of the last 'max_iterations' measurements:
    brightness = summed_up_brightness / max_iterations

    # turn values up-side down: dark-to-bright
    brightness = upper_limit - brightness

    # limit the value of measured brightness
    if brightness > upper_limit:
        brightness = brightness - (brightness - upper_limit)
    elif brightness < lower_limit:
        brightness = brightness - brightness + lower_limit

    # scale brightness to the scale of 0 - 15
    brightness = brightness / (upper_limit / 15)

    return brightness


def tell_when_button_pressed(alarm_days, alarm_time, button_status):
    """when button is pressed and alarm is not acitve
    tell the user some information, defined here"""

    today_nr = time.strftime('%w')

    now = time.strftime("%H%M")
    time_to_alarm = (int(alarm_time[:2]) * 60 + int(alarm_time[3:])) - (int(now[:2]) * 60 + int(now[2:]))

    hours_left = time_to_alarm / 60
    minutes_left = time_to_alarm % 60

    if today_nr in alarm_days and time_to_alarm > 0:
        # next alarm is today
        day = 'today'
        info_message = 'The next alarm will go off %s at %s. Which is %s hours and %s minutes'\
                       % (day, alarm_time, hours_left, minutes_left)
    """
    while just_played_alarm == False:
        # check if button is being pressed
        if button_callback() == True:
            print 'button is pressed without alarm'
            say(info_message)
    """


# start the the button interrupt thread
GPIO.add_event_detect(button_input_pin, GPIO.BOTH, callback=button_callback)

# read out the settings in 'data.xml' from the same folder
xml_data = update_settings('/home/pi/smart_alarm/smart_alarm/data.xml')

# assign the xml data to the corresponding variables
alarm_active, alarm_time, content, alarm_days, individual_msg_active, individual_message, volume \
    = update_settings('/home/pi/smart_alarm/smart_alarm/data.xml')

# set flag for just played the news
just_played_alarm = False

# say welcome message
welcome_message = 'What is my purpose?'
d = threading.Thread(target=say, args=(welcome_message,))
d.start()

# start smart alarm:
display.scroll(' *WELCOME* ', 1)

# set loop counter to one (needed to calculate mean of 10 iterations for the display brightness controll)
loop_counter = 1

# set brightness_data to zero in order to initialize the variable
brightness_data = 0

# set the number of iterations to go through for the mean of brightness value
# 5 looks pretty stable, but does not act to fast on sharp changes. Increase value for more stability,
# decrease it for faster response time
number_of_iterations = 5

# set decimal point flag - for decimal point blinking
point = False


try:
    while True:
        # organise time format
        now = time.strftime("%H%M")

        # reset display
        display.clear_class()

        # read xml file and store data to xml_data
        new_xml_data = update_settings('/home/pi/smart_alarm/smart_alarm/data.xml')

        # check if xml file was updated. If so, update the variables
        if xml_data != new_xml_data:
            print 'file changed - update settings'
            # set the updated variables
            alarm_active, alarm_time, content, alarm_days, individual_msg_active, individual_message, volume = update_settings('data.xml')

            adjust_volume(volume)

        time_to_alarm = int(int(str(alarm_time[:2]) + str(alarm_time[3:]))) - int(now)

        # check if alarm is activated
        if alarm_active == '1' and just_played_alarm == False:     # alarm is activated start managing to go off
            # find the actual day of the week in format of a number in order to compare to the xml days variable
            today_nr = time.strftime('%w')

            if today_nr in alarm_days:      # check if current day is programmed to alarm
                # alarm is set to go off today, calculate the remaining time to alarm

                if time_to_alarm == 0:

                    # check if news or audio (offline mp3) is programmed
                    if content == 'podcast':

                        # display the current time
                        display.show_time(now)
                        # write content to display
                        display.write()

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


                    elif content == 'mp3':
                        # since music is preferred, play the offline mp3 files

                        # display the current time
                        display.show_time(now)
                        # write content to display
                        display.write()

                        # set the updated individual wake-up message in order to play it
                        individual_message = set_ind_msg(individual_msg_active, individual_message)

                        # wake up with individual message
                        say(individual_message)

                        b = threading.Thread(target=play_wakeup_music, args=())
                        b.start()

                        # set flag for just played alarm
                        just_played_alarm = True


                    elif content == 'stream':
                        # since internet-radio is preferred, play the online stream
                        # display the current time
                        display.show_time(now)
                        # write content to display
                        display.write()

                        # set the updated individual wake-up message in order to play it
                        individual_message = set_ind_msg(individual_msg_active, individual_message)

                        # wake up with individual message
                        say(individual_message)

                        c = threading.Thread(target=play_online_stream, args=())
                        c.start()

                        # set flag for just played alarm
                        just_played_alarm = True

        if time_to_alarm != 0:
            # set just_played_alarm back to False in order to not miss the next alarm
            just_played_alarm = False

        # display the current time
        display.show_time(now)

        # check if alarm is active and set third decimal point
        if alarm_active == '1':
            display.set_decimal(3, True)
        else:
            # else if alarm is deactivated, turn last decimal point off
            display.set_decimal(3, False)

        if point:
            display.set_decimal(1, point)
            point = False
            # write content to display
            display.write()
            time.sleep(0.5)
        else:
            display.set_decimal(1, point)
            point = True
            # write content to display
            display.write()
            time.sleep(0.5)

        # delete old and unneeded mp3 files
        delete_old_files(time_to_alarm, alarm_active)

        # update xml file in order to find differences in next loop
        xml_data = new_xml_data

        # read area brightness with photocell, save the data to current_brightness and add it the brightness_data
        # in order to calculate the mean of an set of measurements
        current_brightness = read_photocell()
        brightness_data += current_brightness

        print 'loop_counter: %s \t current_brightness: %s \t brightness_data: %s ' % (loop_counter, current_brightness, brightness_data)

        # increase loop counter +1 since loop is about to start again
        loop_counter += 1
        if loop_counter > number_of_iterations:
            display.set_brightness(int(brightness_data) / number_of_iterations)
            loop_counter = 1
            brightness_data = 0


finally:  # this block will run no matter how the try block exits
    say('Goodbye')
    GPIO.output(amp_switch_pin, 0)  # switch amp off
    print '\nbye!'
