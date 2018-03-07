import xml.etree.cElementTree as ET
import copy
import os
import logging

from os import listdir
from os.path import isfile, join


# read environmental variable for project path
project_path = os.environ['smart_alarm_path']
logger = logging.getLogger(__name__)


class Xml_data(object):
    """
    class handling the xml operations. The given functions will return
    the required variable by reading out the data.xml file.
    """

    def __init__(self, xml_file):
        self.xml_path = xml_file
        self.xmldoc = ET.parse(self.xml_path)
        self.readFileNamesInMusicDirectory()

    def alarm_active(self):
        return self.xmldoc.find('alarm_active').text

    def alarm_time(self):
        return self.xmldoc.find('alarm_time').text

    def content(self):
        return self.xmldoc.find('content').text

    def alarm_days(self):
        return self.xmldoc.find('days').text

    def individual_message_active(self):
        return self.xmldoc.find('individual_message').text

    def individual_message_text(self):
        return self.xmldoc.find('text').text

    def volume(self):
        return self.xmldoc.find('volume').text

    def content_podcast_url(self):
        return self.xmldoc.find('content_podcast_url').text

    def content_stream_url(self):
        return self.xmldoc.find('content_stream_url').text

    def test_alarm(self):
        return self.xmldoc.find('test_alarm').text

    def read_data(self):
        """reads the data.xml file and returns the data of the whole
        file as a string. Used for detecting changes in the file."""
        self.xmldoc = ET.parse(self.xml_path)
        self.readFileNamesInMusicDirectory()

        with open(self.xml_path) as infile:
            data = infile.read()
        return data

    def changeValue(self, element_name, value):
        """Allows editing the xml-file, by passing the elements-
        name and the desired value."""
        logger.warning("XML CHANGE: element: {}; value: {}".format(element_name, value))
        self.xmldoc.find(element_name).text = value
        self.writeFile()

    def writeFile(self):
        self.xmldoc.write(self.xml_path)

    def readFileNamesInMusicDirectory(self):
        mp3_tracks_node = self.xmldoc.find('mp3_files')
        mp3_tracks_node_old = copy.deepcopy(mp3_tracks_node)
        mp3_tracks_node.clear()
        fileNames = [f for f in listdir(project_path + '/music') if isfile(join(project_path + '/music', f))]
        for file in fileNames:
            node = ET.SubElement(mp3_tracks_node, 'track')
            node.text = file

        if not elements_equal(mp3_tracks_node, mp3_tracks_node_old):
            self.xmldoc.write(self.xml_path)


def elements_equal(e1, e2):
    if e1.tag != e2.tag: return False
    if e1.text != e2.text: return False
    if e1.tail != e2.tail: return False
    if e1.attrib != e2.attrib: return False
    if len(e1) != len(e2): return False
    return all(elements_equal(c1, c2) for c1, c2 in zip(e1, e2))
