from xml.dom import minidom
from collections import namedtuple
from xml.dom.minidom import Node


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
    settings = namedtuple("settings", "alarm_active time content days individual_message text volume")

    xmldoc = minidom.parse(xml_file)

    settings.alarm_active = xmldoc.getElementsByTagName('alarm_active')[0].childNodes[0].data
    settings.time = xmldoc.getElementsByTagName('time')[0].childNodes[0].data
    settings.content = xmldoc.getElementsByTagName('content')[0].childNodes[0].data
    settings.days = xmldoc.getElementsByTagName('days')[0].childNodes[0].data
    settings.individual_message = xmldoc.getElementsByTagName('individual_message')[0].childNodes[0].data
    settings.text = xmldoc.getElementsByTagName('text')[0].childNodes[0].data
    settings.volume = xmldoc.getElementsByTagName('volume')[0].childNodes[0].data

    return settings


if __name__ == '__main__':
    settings = read_xml_file_namedtuple('xml_dummy.xml')
    print str(settings.alarm_active) + '\n' + str(settings.time) + '\n' + str(settings.content) + '\n' + str(settings.days) + '\n'\
          + str(settings.individual_message) + '\n' + str(settings.text) + '\n' + str(settings.volume)

