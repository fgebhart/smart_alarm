from xml.dom import minidom
from collections import namedtuple


def read_xml_file_namedtuple(xml_file):
    settings = namedtuple("settings", "alarm_active time content days individual_message text volume")

    xmldoc = minidom.parse(xml_file)

    settings.alarm_active = xmldoc.getElementsByTagName('alarm_active')[0].childNodes[0].data
    settings.time = xmldoc.getElementsByTagName('alarm_time')[0].childNodes[0].data
    settings.content = xmldoc.getElementsByTagName('content')[0].childNodes[0].data
    settings.days = xmldoc.getElementsByTagName('days')[0].childNodes[0].data
    settings.individual_message = xmldoc.getElementsByTagName('individual_message')[0].childNodes[0].data
    settings.text = xmldoc.getElementsByTagName('text')[0].childNodes[0].data
    settings.volume = xmldoc.getElementsByTagName('volume')[0].childNodes[0].data

    return settings


def find_most_recent_news_url_in_xml_file(xml_file):
    """parse the xml file in order to find the url in the first item,
    corresponding to the most_recent_news_url"""
    # run XML parser and create a list with all 'enclosure' item urls
    xmldoc = minidom.parse(xml_file)
    itemlist = xmldoc.getElementsByTagName('enclosure')

    # search for 'url' and take the first list element
    most_recent_news_url = itemlist[0].attributes['url'].value

    return most_recent_news_url


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


def changeValue(xml_file, element_name, value):
    xmldoc = minidom.parse(xml_file)
    xmldoc.getElementsByTagName(element_name)[0].childNodes[0].data = value
    with open(xml_file, "wb") as f:
        xmldoc.writexml(f)



"""
def read(xml_file, settings):
    xmldoc = minidom.parse(xml_file)

    settings.alarm_active = xmldoc.getElementsByTagName('alarm_active')[0].childNodes[0].data
    settings.alarm_time = xmldoc.getElementsByTagName('alarm_time')[0].childNodes[0].data
    settings.content = xmldoc.getElementsByTagName('content')[0].childNodes[0].data
    settings.days = xmldoc.getElementsByTagName('days')[0].childNodes[0].data
    settings.individual_message = xmldoc.getElementsByTagName('individual_message')[0].childNodes[0].data
    settings.text = xmldoc.getElementsByTagName('text')[0].childNodes[0].data
    settings.volume = xmldoc.getElementsByTagName('volume')[0].childNodes[0].data


def write(currentTime, settings):
    doc = Document()

    dataNode = doc.createElement('data')
    doc.appendChild(dataNode)

    timeNode = dataNode.appendChild(doc.createElement('alarm_time'))
    timeNode.appendChild(doc.createTextNode(settings.alarm_time))

    timeNode = dataNode.appendChild(doc.createElement('last_modified'))
    timeNode.appendChild(doc.createTextNode(currentTime))

    timeNode = dataNode.appendChild(doc.createElement('content'))
    timeNode.appendChild(doc.createTextNode(settings.content))

    daysNode = dataNode.appendChild(doc.createElement('days'))
    daysNode.appendChild(doc.createTextNode(settings.days))

    daysNode = dataNode.appendChild(doc.createElement('alarm_active'))
    daysNode.appendChild(doc.createTextNode(settings.alarm_active))

    daysNode = dataNode.appendChild(doc.createElement('individual_message'))
    daysNode.appendChild(doc.createTextNode(settings.individual_message))

    daysNode = dataNode.appendChild(doc.createElement('text'))
    daysNode.appendChild(doc.createTextNode(settings.text))

    daysNode = dataNode.appendChild(doc.createElement('volume'))
    daysNode.appendChild(doc.createTextNode(settings.volume))

    return doc
"""