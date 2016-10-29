#!/usr/bin/env python
# -*- coding: utf-8 -*-

import recalboxFiles

# Create the controller configuration file
def generateControllerConfig(system, playersControllers):
    if system.name == "wii":
        generateControllerConfig_wii(playersControllers)
    elif system.name == "gamecube":
        generateControllerConfig_gamecube(playersControllers)
    else:
        raise ValueError("Invalid system name : '" + system.name + "'")

def generateControllerConfig_wii(playersControllers):
    wiiMapping = {
        'a':      'Buttons/2',  'b':        'Buttons/A',
        'x':      'Buttons/1',  'y':        'Buttons/B',
        'pageup': 'Buttons/-',  'pagedown': 'Buttons/+',
        'select':    'Buttons/Home',
        'up': 'D-Pad/Up', 'down': 'D-Pad/Down', 'left': 'D-Pad/Left', 'right': 'D-Pad/Right',
        'joystick1up': 'IR/Up',    'joystick1left': 'IR/Left',
        'joystick2up': 'Swing/Up', 'joystick2left': 'Swing/Left'
    }
    wiiReverseAxes = {
        'D-Pad/Up':   'D-Pad/Down',
        'D-Pad/Left': 'D-Pad/Right',
        'IR/Up':      'IR/Down',
        'IR/Left':    'IR/Right',
        'Swing/Up':   'Swing/Down',
        'Swing/Left': 'Swing/Right',
    }
    generateControllerConfig_any(playersControllers, "WiimoteNew.ini", "Wiimote", wiiMapping, wiiReverseAxes)

def generateControllerConfig_gamecube(playersControllers):
    gamecubeMapping = {
        'a':      'Buttons/X',  'b':        'Buttons/A',
        'x':      'Buttons/Y',  'y':        'Buttons/B',
        'r2':     'Buttons/Z',  'start':    'Buttons/Start',
        'pageup': 'Triggers/L', 'pagedown': 'Triggers/R',
        'up': 'D-Pad/Up', 'down': 'D-Pad/Down', 'left': 'D-Pad/Left', 'right': 'D-Pad/Right',
        'joystick1up': 'Main Stick/Up', 'joystick1left': 'Main Stick/Left',
        'joystick2up': 'C-Stick/Up',    'joystick2left': 'C-Stick/Left'
    }
    gamecubeReverseAxes = {
        'D-Pad/Up':        'D-Pad/Down',
        'D-Pad/Left':      'D-Pad/Right',
        'Main Stick/Up':   'Main Stick/Down',
        'Main Stick/Left': 'Main Stick/Right',
        'C-Stick/Up':      'C-Stick/Down',
        'C-Stick/Left':    'C-Stick/Right'
    }
    generateControllerConfig_any(playersControllers, "GCPadNew.ini", "GCPad", gamecubeMapping, gamecubeReverseAxes)
    
def generateControllerConfig_any(playersControllers, filename, anyDefKey, anyMapping, anyReverseAxes):
    configFileName = "{}/{}".format(recalboxFiles.dolphinConfig, filename)
    f = open(configFileName, "w")
    nplayer = 1
    nsamepad = 0

    # in case of two pads having the same name, dolphin wants a number to handle this
    double_pads = dict()

    for playercontroller in playersControllers:
        # handle x pads having the same name
        pad = playersControllers[playercontroller]
        if pad.configName in double_pads:
            nsamepad = double_pads[pad.configName]
        else:
            nsamepad = 0
        double_pads[pad.configName] = nsamepad+1

        f.write("[" + anyDefKey + str(nplayer) + "]" + "\n")
        f.write("Device = evdev/" + str(nsamepad) + "/" + pad.configName + "\n")

        for x in pad.inputs:
            input = pad.inputs[x]

            keyname = None
            if input.name in anyMapping:
                keyname = anyMapping[input.name]
            #else:
            #    f.write("# undefined key: name="+input.name+", type="+input.type+", id="+str(input.id)+", value="+str(input.value)+"\n")

            # write the configuration for this key
            if keyname is not None:
                write_key(f, keyname, input.type, input.id, input.value, pad.nbaxes, False)
            # write the 2nd part
            if input.name in { "joystick1up", "joystick1left", "joystick2up", "joystick2left"} and keyname is not None:
                write_key(f, anyReverseAxes[keyname], input.type, input.id, input.value, pad.nbaxes, True)

        nplayer += 1
    f.write
    f.close()

def write_key(f, keyname, input_type, input_id, input_value, input_global_id, reverse):
    f.write(keyname + " = `")
    if input_type == "button":
        f.write("Button " + str(input_id))
    elif input_type == "hat":
        if input_value == "1" or input_value == "4": # up or down
            f.write("Axis " + str(int(input_global_id)+1))
        else:
            f.write("Axis " + str(input_global_id))
        if input_value == "1" or input_value == "8": # up or left
            f.write("-")
        else:
            f.write("+")
    elif input_type == "axis":
        if (reverse and input_value == "-1") or (not reverse and input_value == "1"):
            f.write("Axis " + str(input_id) + "+")
        else:
            f.write("Axis " + str(input_id) + "-")
    f.write("`\n")
