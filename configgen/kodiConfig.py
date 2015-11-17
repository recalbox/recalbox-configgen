#!/usr/bin/env python

import controllersConfig as controllers
import signal
import recalboxFiles
from xml.dom import minidom

def signal_handler(signal, frame):
    print('Exiting')
    if runner.proc:
        print('killing runner.proc')
        runner.proc.kill()

def getCurrentControllers(dom):
    joys = dict()
    for config in dom.getElementsByTagName('config'):
        for node in config.childNodes:
            if node.attributes:
                if node.attributes['name']:
                    if node.attributes['name'].value in ['INPUT P1', 'INPUT P2', 'INPUT P3', 'INPUT P4']:
                        if node.attributes['value']:
                            if node.attributes['value'].value != 'DEFAULT':
                                joys[node.attributes['value'].value] = None
    return joys

def getKodiMapping():
    dom = minidom.parse(recalboxFiles.kodiMapping)
    map = dict()
    for inputs in dom.getElementsByTagName('inputList'):
        for input in inputs.childNodes:
            if input.attributes:
                if input.attributes['name']:
                    if input.attributes['value']:
                        map[input.attributes['name'].value] = input.attributes['value'].value
    return map

def getKodiConfig(currentControllers, playersControllers):
    kodimapping          = getKodiMapping()
    kodihatspositions    = {1: 'up', 2: 'right', 4: 'down', 8: 'left'}
    kodireversepositions = {'joystick1up': 'joystick1down', 'joystick1left': 'joystick1right', 'joystick2up': 'joystick2down', 'joystick2left': 'joystick2right' }
    
    config = minidom.Document()
    xmlkeymap = config.createElement('keymap')
    config.appendChild(xmlkeymap)
    xmlglobal = config.createElement('global')
    xmlkeymap.appendChild(xmlglobal)
    for cur in currentControllers:
        xmljoystick = config.createElement('joystick')
        xmljoystick.attributes["name"] = playersControllers[cur].configName
        xmlglobal.appendChild(xmljoystick)
        for x in playersControllers[cur].inputs:
            input = playersControllers[cur].inputs[x]
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
                    xmlaxis.attributes["limit"] = "-1"
                    action = config.createTextNode(kodimapping[input.name])
                    xmlaxis.appendChild(action)
                    xmljoystick.appendChild(xmlaxis)
                    # dir 2
                    if input.name in kodireversepositions and kodireversepositions[input.name] in kodimapping:
                        xmlaxis = config.createElement('axis')
                        xmlaxis.attributes["id"] = str(int(input.id)+1) # in kodi, it's sdl +1
                        xmlaxis.attributes["limit"] = "1"
                        action = config.createTextNode(kodimapping[kodireversepositions[input.name]])
                        xmlaxis.appendChild(action)
                        xmljoystick.appendChild(xmlaxis)

    return config
                
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    currentControllers = getCurrentControllers(minidom.parse(recalboxFiles.esSettings))
    playersControllers = controllers.loadAllControllersByNameConfig()

    file = open(recalboxFiles.kodiJoystick, "w")
    file.write(getKodiConfig(currentControllers, playersControllers).toprettyxml())
    file.close()
