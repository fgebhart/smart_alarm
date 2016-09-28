__author__ = 'fgebhart'

"""
1. Insert the url to the desired news web page
2. The corresponding XML file will be downloaded
3. Using minidom lib the first item url will be figured out
4. The first item url (= most recent news url) will be downloaded
5. Using pygame lib the news mp3 file will be played
"""

# import packages
# minidom = xml parser
# urllib manages to download web files
# pygame = plays mp3 files
# python text to speech library
from xml.dom import minidom
import urllib2
import pygame
import pyttsx


# dlf podcast link to XML file. Correct if modified!
dlf_news_url = "http://www.deutschlandfunk.de/podcast-nachrichten.1257.de.podcast.xml"


def download_file(link_to_file):
    """function for downloading files"""
    file_name = link_to_file.split('/')[-1]
    u = urllib2.urlopen(link_to_file)
    f = open(file_name, 'wb')
    print "Downloading: %s" % (file_name)

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
    while pygame.mixer.music.get_busy() == True:
        continue


def say(text):
    """synthesizes the given text to speech"""
    engine = pyttsx.init()
    engine.setProperty('rate', 150)
    # remove "pass" and uncomment next line in order to enable this function
    pass    
    #engine.say(text)
    engine.runAndWait()



# download dlf_xml_file according to the dlf_news_url
dlf_xml_file = download_file(dlf_news_url)
say("xml file downloaded")

# now parse the dlf_xml_file in order to find the most_recent_news_url
most_recent_news_url = find_most_recent_news_url_in_xml_file(dlf_xml_file)
say("url to newest file detected")

# download the most recent news_mp3_file according to the most_recent_news_url
news_mp3_file = download_file(most_recent_news_url)
say("mp3 file of news downloaded")

# play the most recent news_mp3_file
say("now playing the news")
play_mp3_file(news_mp3_file)



