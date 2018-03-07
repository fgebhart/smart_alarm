#!/usr/bin/python
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
- checks provided podcast + stream url if they are ok, if not play default url
- possibility to press button without any alarm going: informs you about the next alarm
- writing error log to 'error.log' file
- checks for internet connection 2mins before alarm, since the connection sometimes
    get lost during the night
- flashy RBG LEDs
- enable uploading and organizing mp3 files via webinterface
- enable Spotify interface using mopidy

mpc stations:
OrangeFM                http://orange-01.live.sil.at:8000
SmoothLounge with Ads:  http://streaming.radionomy.com/The-Smooth-Lounge?lang=en-US%2cen%3bq%3d0.8%2cde%3bq%3d0.6

potential podcast stations:
BBC News: http://www.bbc.co.uk/programmes/p02nq0gn/episodes/downloads.rss
DLF News: http://www.deutschlandfunk.de/podcast-nachrichten.1257.de.podcast.xml

"""

import urllib2
import RPi.GPIO as GPIO
import threading
import logging.config
import log_config
from xml.dom import minidom
import time
import os
import coloredlogs
import difflib

# configure logger before importing other modules
logging.config.dictConfig(log_config.logging_dict)
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')

from modules.display_class import Display
from modules.sounds import Sound
from modules.xml_data import Xml_data
from modules.led import LEDs


def button_callback(channel):
    """define a threaded callback function to run when events are detected"""
    start_timer = time.time()
    timer = 0

    logger.debug("button pressed")

    if GPIO.input(button_input_pin) and sound.sound_active is False and led.leds_active is False:  # if port 24 == 1
        while GPIO.input(button_input_pin) and timer < 3:
            loop_timer = time.time()
            timer = loop_timer - start_timer
            time.sleep(0.1)

        if timer < 3:
            logger.info('button pressed for < 3 sec')
            tell_when_button_pressed(xml_data.alarm_active(), xml_data.alarm_days(), xml_data.alarm_time())
        if timer >= 3:
            logger.info('button pressed for > 3 sec')
            shutdown_pi()

    elif GPIO.input(button_input_pin):
        if sound.sound_active is True:
            sound.stopping_sound()
        elif led.leds_active is True:
            led.stopping_leds()


def download_file(link_to_file):
    """function for downloading files"""
    file_name = link_to_file.split('/')[-1]
    u = urllib2.urlopen(link_to_file)
    f = open(file_name, 'wb')
    logger.debug("downloading file: %s" % file_name)

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
    logger.debug('download of {} done'.format(file_name))
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


def set_ind_msg(ind_msg_active, ind_msg_text):
    """takes and checks the to two arguments and sets the
    individual message"""
    if ind_msg_active == '0':
        # ind msg is deactivated, therefore create default message
        logger.debug('-> individual message deactivated - constructing default message')
        sayable_time = str(time.strftime("%H %M"))
        today = time.strftime('%A')
        standard_message = 'good morning. It is ' + today + '  ' + sayable_time
        individual_message = standard_message
    else:
        individual_message = ind_msg_text

    return individual_message


def delete_old_files(time_to_alarm):
    """checks for old mp3 files and deletes them"""
    list_of_mp3_files = []
    # check the projects directory
    for mp3_file in os.listdir(project_path):
        if mp3_file.endswith('.mp3'):
            list_of_mp3_files.append(project_path + '/' + str(mp3_file))

    # as well check the home folder
    for mp3_file in os.listdir('/home/pi'):
        if mp3_file.endswith('.mp3'):
            list_of_mp3_files.append('/home/pi/' + str(mp3_file))

    # delete old files, either 12h before or after alarm
    if time_to_alarm == 720 or time_to_alarm == -720:
        logger.warning("...checking for old mp3 files to delete...")
        for mp3_file in range(len(list_of_mp3_files)):
            logger.debug('deleting old mp3 files: {}'.format(list_of_mp3_files))
            os.remove(list_of_mp3_files[mp3_file])


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


def tell_when_button_pressed(alarm_active, alarm_days, alarm_time):
    """when button is pressed and alarm is not active
    tell the user some information about the upcoming alarms"""

    next_alarm_day_found = None
    info_message = 'shit. didnt work'

    # figure out the weekdays:
    weekdays = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

    # fetch date and time information and convert it to the needed format
    today_as_number = time.strftime('%w')
    now = time.strftime("%H%M")
    time_to_alarm = (int(alarm_time[:2]) * 60 + int(alarm_time[3:])) - (int(now[:2]) * 60 + int(now[2:]))

    # check if alarm is active, then distinguish the four possibilities
    if alarm_active == '1':
        # P1: alarm today + tta > 0
        if str(today_as_number) in alarm_days and time_to_alarm > 0:
            hours_left = time_to_alarm / 60
            minutes_left = time_to_alarm % 60
            info_message = 'The next alarm is today, at %s, which is in %s hours and %s minutes.' % (str(alarm_time), str(hours_left), str(minutes_left))
            if hours_left == 0:
                info_message = 'The next alarm is today, at %s, which is in %s minutes.' % (str(alarm_time), str(minutes_left))

        # P2: tta < 0
        elif time_to_alarm <= 0 or str(today_as_number) not in alarm_days:

            days_to_alarm = 0
            next_alarm_day = int(today_as_number)
            # start loop to findout the up next day which is set to alarm
            while next_alarm_day_found is None:
                days_to_alarm += 1
                next_alarm_day += 1
                if next_alarm_day > 6:
                    next_alarm_day = 0
                if str(next_alarm_day) in alarm_days:
                    next_alarm_day_found = True

            # P3: tta < 0 + not today
            if time_to_alarm <= 0:
                time_left_in_minutes = 1440 + int(time_to_alarm)
                hours_left = time_left_in_minutes / 60
                minutes_left = time_left_in_minutes % 60
                days_to_alarm -= 1
                next_alarm_day = weekdays[next_alarm_day]
                info_message = 'The next alarm is on %s at %s, which is in %s days, %s hours and %s minutes.'\
                               % (str(next_alarm_day), str(alarm_time), str(days_to_alarm), str(hours_left), str(minutes_left))
                if days_to_alarm == 0:
                    info_message = 'The next alarm is tomorrow at %s, which is in %s hours and %s minutes.' \
                                   % (str(alarm_time), str(hours_left), str(minutes_left))
            # P4: tta > 0 + not today
            elif time_to_alarm > 0:
                hours_left = time_to_alarm / 60
                minutes_left = time_to_alarm % 60
                next_alarm_day = weekdays[next_alarm_day]
                info_message = 'The next alarm is on %s at %s, which is in %s days, %s hours and %s minutes.' \
                               % (str(next_alarm_day), str(alarm_time), str(days_to_alarm), str(hours_left), str(minutes_left))
                if days_to_alarm == 1:
                    info_message = 'The next alarm is tomorrow at %s, which is in one day %s hours and %s minutes.' \
                                   % (str(alarm_time), str(hours_left), str(minutes_left))
    elif alarm_active == '0':
        info_message = 'No alarm set.'

    sound.say(info_message)


def run_alarm_light():
    """runs the desired light show for wake up"""
    # display the current time
    display.show_time(now)
    # write content to display
    display.write()

    if check_if_smartalarm_is_running_leds():
        # starts led light show
        led.wake_up_light_show(time_for_leds)


def run_alarm_sound():
    """main function to run the alarm, based
    on the configured settings in data.xml"""
    logger.warning('>>>> NOW RUNNING ALARM <<<<')

    # display the current time
    display.show_time(now)
    # write content to display
    display.write()

    # check if news or audio (offline mp3) is programmed
    if xml_data.content() == 'podcast':
        logger.info('chosen alarm option: podcast')

        # set the updated individual wake-up message in order to play it
        individual_message = set_ind_msg(xml_data.individual_message_active(), xml_data.individual_message_text())
        # wake up with individual message
        z = threading.Thread(target=sound.say, args=(individual_message, True,))
        z.start()

        # check if the provided podcast url is working. If not function chooses deafult url
        podcast_url = check_if_podcast_url_correct(xml_data.content_podcast_url())

        # download podcast_xml_file according to the podcast_url
        podcast_xml_file = download_file(podcast_url)

        # now parse the podcast_xml_file in order to find the most_recent_news_url
        most_recent_news_url = find_most_recent_news_url_in_xml_file(podcast_xml_file)

        # download the most recent news_mp3_file according to the most_recent_news_url
        news_mp3_file = download_file(most_recent_news_url)

        # wait untill thread z (say) is done
        while z.isAlive() is True:
            time.sleep(0.5)

        # play the most recent news_mp3_file
        a = threading.Thread(target=sound.play_mp3_file, args=(news_mp3_file,))
        a.start()

    elif xml_data.content() == 'mp3':
        logger.info('chosen alarm option: mp3')

        # set the updated individual wake-up message in order to play it
        individual_message = set_ind_msg(xml_data.individual_message_active(), xml_data.individual_message_text())
        # wake up with individual message
        sound.say(individual_message)

        b = threading.Thread(target=sound.play_wakeup_music, args=())
        b.start()

    elif xml_data.content() == 'stream':
        logger.info('chosen alarm option: stream')

        # add the provided stream url to mpc playlist, understands spotify urls as well
        add_stream_url_to_mpc_playlist(xml_data.content_stream_url())

        # set the updated individual wake-up message in order to play it
        individual_message = set_ind_msg(xml_data.individual_message_active(), xml_data.individual_message_text())
        # wake up with individual message
        sound.say(individual_message, force=True)

        c = threading.Thread(target=sound.play_online_stream, args=())
        c.start()

    # at the end of the alarm function reset the stop variable
    led.stop_led = False


def add_stream_url_to_mpc_playlist(stream_url):
    """reads the provided stream url"""
    os.system('mpc clear')
    # managa default stream url
    default_stream_url = "http://orange-01.live.sil.at:8000"
    if stream_url.startswith(('http://', 'https://', 'www.', 'spotify:')):
        pass
    else:
        logger.info('provided stream url does not look like a proper url. Playing default stream instead!')
        stream_url = default_stream_url
    os.system('mpc add ' + str(stream_url))


def check_if_podcast_url_correct(podcast_url):
    """check if the provided url is okay, if not, inform master and use default podcast url"""
    # manage default podcast url
    default_podcast_url = "http://www.deutschlandfunk.de/podcast-nachrichten.1257.de.podcast.xml"
    # BBC News: http://www.bbc.co.uk/programmes/p02nq0gn/episodes/downloads.rss
    # DLF News: http://www.deutschlandfunk.de/podcast-nachrichten.1257.de.podcast.xml
    most_recent_news_url = 'no_mp3_file'

    if podcast_url.startswith(('http://', 'https://', 'www.')):
        pass
    else:
        logger.info('provided podcast url does not look like a proper url. Playing default podcast instead!')
        return default_podcast_url

    try:
        podcast_xml_file = download_file(podcast_url)
        most_recent_news_url = find_most_recent_news_url_in_xml_file(podcast_xml_file)
    finally:
        if most_recent_news_url.endswith('.mp3'):
            return podcast_url
        else:
            logger.info('Cant find any m p 3 file in the provided podcast url. Playing default podcast instead!')
            return default_podcast_url


def shutdown_pi():
    """function is executed when button is pressed and hold for 5 seconds
    asks the user to shut down and does so by pressing the button again"""
    o = threading.Thread(target=sound.say, args=('Wanna shut me down?',))
    o.start()
    start_timer = time.time()
    timer = 0
    shutdown = False

    while GPIO.input(button_input_pin) == 1:
        time.sleep(0.1)

    if GPIO.input(button_input_pin) == 0:

        while timer < 5:
            loop_timer = time.time()
            timer = loop_timer - start_timer
            if GPIO.input(button_input_pin):
                shutdown = True
                break
            time.sleep(0.1)

        if shutdown:
            logger.debug('manually shutting down now')
            q = threading.Thread(target=display.shutdown, args=(3,))
            q.start()
            sound.say('O K. Bye!')
            display.clear_class()
            display.scroll('    ', 4)
            display.write()
            os.system('sudo poweroff')
        else:
            logger.debug("won't shut down")
            sound.say("O K. I'll stay!")


def if_interrupt():
    """stuff to do when script crashed because of interrupt or whatever"""
    k = threading.Thread(target=sound.say, args=('Outsch!', True,))
    k.start()
    display.snake(1)
    sound.toggle_amp_pin(0)   # switch amp off
    logger.error('\n... crashed ... bye!\n   -> check error.log for more information')


def change_stream_url(stream_url):
    """deletes old mpc radio playlist
    and adds the new provided url"""
    os.system('mpc clear')
    string_command_add_url = 'mpc add ' + str(stream_url)
    os.system(string_command_add_url)


def check_if_smartalarm_is_running_leds():
    """checks if this smart alarm version is running LEDs by
    looking for the file APA102_Pi/colorschemes.py. If it
    is there, the operating smart alarm mostlikely is running
    with LEDs"""
    logger.info('checking if I have LEDs installed...')
    if os.path.isfile('/home/pi/APA102_Pi/colorschemes.py'):
        logger.info('...yeah I\'m flashy')
        return True
    else:
        logger.info('...oh, sadly not')
        return False


project_path = os.environ['smart_alarm_path']


# write to error.log file
logger.info('\n \n         ______SMART ALARM STARTED______')

# initialize variables for creating objects
display = sound = xml_data = led = None

# import display_class
try:
    display = Display()
except Exception as e:
    logger.error("failed to instantiate display class with exception {}".format(e))

# import sound class
try:
    sound = Sound()
except Exception as e:
    logger.error("failed to instantiate sound class with exception {}".format(e))

# import xml class
try:
    xml_data = Xml_data(str(project_path) + '/data.xml')
except Exception as e:
    logger.error("failed to instantiate xml_data class with exception {}".format(e))

# import led class
try:
    led = LEDs()
except Exception as e:
    logger.error("failed to instantiate LED class with exception {}".format(e))

# set button input pin
button_input_pin = 24
# set pin for amplifier switch
amp_switch_pin = 5

# define time for led light show in seconds, needs to be >= 10,
# otherwise the leds functions will be skipped due to while functions
time_for_leds = 300

# turn off GPIO warnings
GPIO.setwarnings(False)
# configure RPI GPIO. Make sure to use 1k ohms resistor to protect input pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_input_pin, GPIO.IN)
# set pin to output
GPIO.setup(amp_switch_pin, GPIO.OUT)
# set output low in order to turn off amplifier and nullify noise
sound.toggle_amp_pin(0)
# alternative starting display
y = threading.Thread(target=display.big_stars, args=(7,))
y.start()

# one quick led rainbow
v = threading.Thread(target=led.rainbow, args=(10, 1,))
v.start()

# say welcome message
welcome_message = 'What is my purpose?'
read_name_of_connected_wifi = "successfully connected to "\
                              + os.popen("iw dev wlan0 link | grep SSID | awk '{print $2}'").read()\
                              + "wifi"
dummy_message = 'hi'
sound.say(dummy_message)

# start the the button interrupt thread
GPIO.add_event_detect(button_input_pin, GPIO.BOTH, callback=button_callback)

# read out the settings in 'data.xml' from the same folder
xml_file = xml_data.read_data()
# also read out the set volume in order to recognize changes
volume = xml_data.volume()

# set flag for just played alarm and just checked wifi
just_played_alarm = False
just_checked_wifi = False
just_played_light_show = False

# set loop counter to one (needed to calculate mean of 10 iterations for the display brightness control)
loop_counter = 1

# set brightness_data to zero in order to initialize the variable
brightness_data = 0

# set the number of iterations to go through for the mean of brightness value
# 5 seconds look pretty stable, but does not act too fast on sharp changes.
# Increase value for more stability, decrease it for faster response time
number_of_iterations = 5

# set decimal point flag - for decimal point blinking
point = False

# start timer for second-wise dot blinking
start_time = time.time()

if xml_data.test_alarm() == 1:
    logger.warning("setting test alarm to 0")
    xml_data.changeValue('test_alarm', '0')

logger.info('starting main loop...')

try:
    while True:
        # organise time format
        now = time.strftime("%H%M")

        # reset display
        display.clear_class()

        # read xml file and store data to xml_data
        new_xml_file = xml_data.read_data()
        # read new volume in order to recognize changes
        new_volume = xml_data.volume()

        logger.warning("test alarm in XML: {}".format(xml_data.test_alarm()))

        # check if xml file was updated. If so, update the variables
        if xml_file != new_xml_file:
            logger.info('data.xml file changed:')
            old_lines = str(xml_file).strip().splitlines()
            new_lines = str(new_xml_file).strip().splitlines()
            for line in difflib.unified_diff(old_lines, new_lines, fromfile="old_xml", tofile="new_xml", lineterm=''):
                logger.debug(line)
            sound.play_mp3_file(project_path + '/sounds/blop.mp3')

            # check if test alarm was pressed
            if xml_data.test_alarm() == '1' and just_played_alarm is False:
                logger.warning('running test alarm')
                xml_data.changeValue('test_alarm', '0')
                q = threading.Thread(target=run_alarm_sound, args=())
                q.start()
                just_played_alarm = True
            elif volume != new_volume:
                sound.adjust_volume(xml_data.volume())

        time_to_alarm = int(int(str(xml_data.alarm_time()[:2]) + str(xml_data.alarm_time()[3:]))) - int(now)

        # check if alarm is activated
        if xml_data.alarm_active() == '1' and just_played_alarm is False:  # alarm is activated start managing to go off
            # find the actual day of the week in format of a number in order to compare to the xml days variable
            today_nr = time.strftime('%w')

            if today_nr in xml_data.alarm_days():      # check if current day is programmed to alarm
                # alarm is set to go off today, calculate the remaining time to alarm

                if time_to_alarm % 5 == 0 and just_checked_wifi is False:      # checks every 5 min for wifi
                    just_checked_wifi = True
                    # logger.info('checking internet connection and restart wlan0 if needed')
                    # logger.debug(str(os.system('sudo ifup wlan0')) + ' zero means wlan0 is still on.')
                elif time_to_alarm % 5 != 0:
                    just_checked_wifi = False

                # logger.debug("time to alarm: {} min".format(time_to_alarm))

                if time_to_alarm == time_for_leds / 60 and just_played_light_show is False:
                    # is true 5 minutes before actual alarm was set
                    p = threading.Thread(target=run_alarm_light, args=())
                    p.start()
                    just_played_light_show = True

                if time_to_alarm == 0:
                    # ----------- RUN ALARM HERE! -----------
                    q = threading.Thread(target=run_alarm_sound, args=())
                    q.start()
                    just_played_alarm = True

        if time_to_alarm != time_for_leds / 60:
            # set just_played_alarm back to False in order to not miss the next alarm
            just_played_light_show = False

        if time_to_alarm != 0:
            # set just_played_alarm back to False in order to not miss the next alarm
            just_played_alarm = False

        # display the current time
        display.show_time(now)

        # check if alarm is active and set third decimal point
        if xml_data.alarm_active() == '1':
            display.set_decimal(3, True)
        else:
            # else if alarm is deactivated, turn last decimal point off
            display.set_decimal(3, False)

        if point:
            display.set_decimal(1, point)
            point = False
            # write content to display
            display.write()
            time.sleep(1.0 - ((time.time() - start_time) % 1.0))
        else:
            display.set_decimal(1, point)
            point = True
            # write content to display
            display.write()
            time.sleep(1.0 - ((time.time() - start_time) % 1.0))

        # delete old and unneeded mp3 files
        delete_old_files(time_to_alarm)

        # update xml file in order to find differences in next loop
        xml_file = new_xml_file

        # read area brightness with photocell, save the data to current_brightness and add it the brightness_data
        # in order to calculate the mean of an set of measurements
        current_brightness = read_photocell()
        brightness_data += current_brightness

        # increase loop counter +1 since loop is about to start again
        loop_counter += 1
        if loop_counter > number_of_iterations:
            display.set_brightness(int(brightness_data) / number_of_iterations)
            loop_counter = 1
            brightness_data = 0

# make sure to save all error messages to the log file
except Exception as e:
    logger.error('Got error on main handler: {}'.format(e))

finally:  # this block will run no matter how the try block exits
    if_interrupt()
