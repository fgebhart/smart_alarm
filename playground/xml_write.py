# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 20:01:58 2016

@author: sebastian
"""
from xml.dom.minidom import Document


def create(currentTime, settings):
    doc = Document()

    dataNode = doc.createElement('data')
    doc.appendChild(dataNode)

    print settings.alarm_time
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