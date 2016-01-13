#!/usr/bin/env python

import controllersConfig as controllers
import signal
import os
import recalboxFiles
from xml.dom import minidom

def getKodiMappingFile():
    if os.path.exists(recalboxFiles.kodiMappingUser):
        return recalboxFiles.kodiMappingUser
    else:
        return recalboxFiles.kodiMappingSystem

def getKodiMapping(scope):
    dom = minidom.parse(getKodiMappingFile())
    map = dict()
    for inputs in dom.getElementsByTagName('inputList'):
        for input in inputs.childNodes:
            if input.attributes:
                if input.attributes['scope']:
                    if input.attributes['scope'].value == scope:
                        if input.attributes['name']:
                            if input.attributes['value']:
                                map[input.attributes['name'].value] = input.attributes['value'].value
    return map

def getKodiMappingScopes():
    dom = minidom.parse(getKodiMappingFile())
    map = dict()
    for inputs in dom.getElementsByTagName('inputList'):
        for input in inputs.childNodes:
            if input.attributes:
                if input.attributes['scope']:
                    map[input.attributes['scope'].value] = True
    return map

def getKodiConfig(currentControllers):
    kodihatspositions    = {1: 'up', 2: 'right', 4: 'down', 8: 'left'}
    kodireversepositions = {'joystick1up': 'joystick1down', 'joystick1left': 'joystick1right', 'joystick2up': 'joystick2down', 'joystick2left': 'joystick2right' }
    
    config = minidom.Document()
    xmlkeymap = config.createElement('keymap')
    config.appendChild(xmlkeymap)

    # scopes
    for scope in getKodiMappingScopes():
        kodimapping = getKodiMapping(scope)
        xmlscope = config.createElement(scope)
        xmlkeymap.appendChild(xmlscope)
        for controller in currentControllers:
            cur = currentControllers[controller]
            xmljoystick = config.createElement('joystick')
            xmljoystick.attributes["name"] = cur.configName
            xmlscope.appendChild(xmljoystick)
            for x in cur.inputs:
                input = cur.inputs[x]
                if input.name in kodimapping:
                    if input.type == 'button':
                        xmlbutton = config.createElement('button')
                        xmlbutton.attributes["id"] = str(int(input.id)+1) # in kodi, it's sdl +1
                        action = config.createTextNode(kodimapping[input.name])
                        xmlbutton.appendChild(action)
                        xmljoystick.appendChild(xmlbutton)
                    elif input.type == 'hat' and int(input.value) in kodihatspositions:
                        xmlhat = config.createElement('hat')
                        xmlhat.attributes["id"] = str(int(input.id) + 1) # in kodi, it's sdl +1
                        xmlhat.attributes["position"] = kodihatspositions[int(input.value)]
                        action = config.createTextNode(kodimapping[input.name])
                        xmlhat.appendChild(action)
                        xmljoystick.appendChild(xmlhat)
                    elif input.type == 'axis':
                        # dir 1
                        xmlaxis = config.createElement('axis')
                        xmlaxis.attributes["id"] = str(int(input.id)+1) # in kodi, it's sdl +1
                        xmlaxis.attributes["limit"] = input.value
                        action = config.createTextNode(kodimapping[input.name])
                        xmlaxis.appendChild(action)
                        xmljoystick.appendChild(xmlaxis)
                        # dir 2
                        if input.name in kodireversepositions and kodireversepositions[input.name] in kodimapping:
                            xmlaxis = config.createElement('axis')
                            xmlaxis.attributes["id"] = str(int(input.id)+1) # in kodi, it's sdl +1
                            xmlaxis.attributes["limit"] = str(-int(input.value))
                            action = config.createTextNode(kodimapping[kodireversepositions[input.name]])
                            xmlaxis.appendChild(action)
                            xmljoystick.appendChild(xmlaxis)
    return config

def writeKodiConfig(controllersFromES):
    directory = os.path.dirname(recalboxFiles.kodiJoystick)
    if not os.path.exists(directory):
        os.makedirs(directory)
    kodiJoy = open(recalboxFiles.kodiJoystick, "w")
    kodiJoy.write(getKodiConfig(controllersFromES).toprettyxml())
    kodiJoy.close()
