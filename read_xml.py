from xml.dom import minidom
from xml.dom.minidom import Node

from collections import namedtuple


def read_xml_file_list(xml_file):
    """reads the xml file, parse it and save the fetched data to the list
    called 'xml_data'."""
    xmldoc = minidom.parse(xml_file)
    xml_data = []

    for elem in xmldoc.getElementsByTagName('data'):
        for x in elem.childNodes:
            if x.nodeType == Node.ELEMENT_NODE:
                xml_data.append(str(x.childNodes[0].data))

    return xml_data

def read_xml_file_namedtuple(xml_file):
    settings = namedtuple("settings", "lastmodified alarmtime content days")

    xmldoc = minidom.parse(xml_file)

    settings.lastmodified = xmldoc.getElementsByTagName('lastmodified')[0].childNodes[0].data
    settings.alarmtime = xmldoc.getElementsByTagName('alarmtime')[0].childNodes[0].data
    settings.content = xmldoc.getElementsByTagName('content')[0].childNodes[0].data
    settings.days = xmldoc.getElementsByTagName('days')[0].childNodes[0].data

    return settings



if __name__ == '__main__':
    settings = read_xml_file_namedtuple('data.xml')
    print settings.lastmodified +' '+ settings.alarmtime +' '+ settings.content +' '+ settings.days