from xml.dom import minidom


class Xml_data(object):
    """
    class handling the xml operations. The given functions will return
    the required variable by reading out the data.xml file.
    """

    def __init__(self, xml_file):
        self.xml_path = xml_file
        self.xmldoc = minidom.parse(self.xml_path)

    def alarm_active(self):
        return self.xmldoc.getElementsByTagName('alarm_active')[0].childNodes[0].data

    def alarm_time(self):
        return self.xmldoc.getElementsByTagName('alarm_time')[0].childNodes[0].data

    def content(self):
        return self.xmldoc.getElementsByTagName('content')[0].childNodes[0].data

    def alarm_days(self):
        return self.xmldoc.getElementsByTagName('days')[0].childNodes[0].data

    def individual_message_active(self):
        return self.xmldoc.getElementsByTagName('individual_message')[0].childNodes[0].data

    def individual_message_text(self):
        return self.xmldoc.getElementsByTagName('text')[0].childNodes[0].data

    def volume(self):
        return self.xmldoc.getElementsByTagName('volume')[0].childNodes[0].data

    def content_podcast_url(self):
        return self.xmldoc.getElementsByTagName('content_podcast_url')[0].childNodes[0].data

    def content_stream_url(self):
        return self.xmldoc.getElementsByTagName('content_stream_url')[0].childNodes[0].data

    def test_alarm(self):
        return self.xmldoc.getElementsByTagName('test_alarm')[0].childNodes[0].data

    def read_data(self):
        """reads the data.xml file and returns the data of the whole
        file as a string. Used for detecting changes in the file."""
        self.xmldoc = minidom.parse (self.xml_path)

        with open(self.xml_path) as infile:
            data = infile.read()
        return data

    def changeValue(self, element_name, value):
        """Allows editing the xml-file, by passing the elements-
        name and the desired value."""
        xmldoc = minidom.parse(self.xml_path)
        xmldoc.getElementsByTagName(element_name)[0].childNodes[0].data = value
        with open(self.xml_path, "wb") as f:
            xmldoc.writexml(f)