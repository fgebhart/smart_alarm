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
-

Todo:
- find internet radio station without commercials and too much talk
- button interrupt instead of waiting

Possible internet radio station (working witch MPC):
- http://streaming.radionomy.com/The-Smooth-Lounge?lang=en-US%2cen%3bq%3d0.8%2cde%3bq%3d0.6
-

"""


import urllib2
import RPi.GPIO as GPIO
import threading
from read_xml import read_xml_file_list, read_xml_file_namedtuple
from display_class import Display
from sounds import *
from xml_belongings import *
import time


# import dispay_class
display = Display()

# configure RPI GPIO. Make sure to use 1k ohms resistor to protect input pin
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# set decimal point flag - for decimal point blinking
point = False

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


def button_pressed():
    """check if button is pressed. If so return True, if not False"""
    counter = 0
    activated = False
    while counter < 20:
        if GPIO.input(11) == 1:
            activated = True
        else:
            pass
        time.sleep(0.1)
        counter += 1
    return activated


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


# read out the settings in 'xml_dummy_xml' from the same folder
xml_data = read_xml_file_list('xml_dummy.xml')

# assign the xml data to the corresponding variables
alarm_active, alarm_time, content, alarm_days, individual_msg_active, individual_message, volume = update_settings('xml_dummy.xml')

# set flag for just played the news
just_played_alarm = False

# change display brightness
# display.set_brightness(15)

# start smart alarm:
display.scroll('*WELCOME*', 1)

# change display brightness
display.set_brightness(0)

try:
    while True:
        # organise time format
        now = time.strftime("%H%M")

        # reset display
        display.clear_class()

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


                    elif content == 'music':
                        # since music is preferred, play the offline mp3 files

                        print 'now playing music'

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


                    elif content == 'internet-radio':
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

                    else:
                        pass


        if time_to_alarm != 0:
            # set just_played_alarm back to False in order to not miss the next alarm
            just_played_alarm = False

        # display the current time
        display.show_time(now)

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
        display.write()

        # delete old and unneeded mp3 files
        delete_old_files(time_to_alarm, alarm_active)

        # update xml file in order to find differences in next loop
        xml_data = new_xml_data

        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    print "\nBye"
