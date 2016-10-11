# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 20:01:58 2016

@author: sebastian
"""
from xml.dom.minidom import Document
from datetime import datetime

def create_xml(currentTime, alarmTime, content, days):
    doc = Document()
    
    dataNode = doc.createElement('data')
    doc.appendChild(dataNode)

    timeNode = dataNode.appendChild(doc.createElement('alarmtime'))
    timeNode.appendChild(doc.createTextNode(alarmTime))
    
    timeNode = dataNode.appendChild(doc.createElement('lastmodified'))
    timeNode.appendChild(doc.createTextNode(currentTime))
    
    timeNode = dataNode.appendChild(doc.createElement('content'))
    timeNode.appendChild(doc.createTextNode(content))
    
    daysNode = dataNode.appendChild(doc.createElement('days'))
    daysNode.appendChild(doc.createTextNode(days))  
    
    return doc
    
if __name__ == '__main__':
    #make_xml().writexml( sys.stdout) #write in console
    create_xml(datetime.now().strftime('%H:%M:%S'), "11:00", "music", "monday tuesday").writexml(open('data.xml', 'w'))