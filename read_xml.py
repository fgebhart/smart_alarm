from xml.dom import minidom
from xml.dom.minidom import Node


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


fetched_data = read_xml_file('xml_dummy.xml')

print fetched_data
