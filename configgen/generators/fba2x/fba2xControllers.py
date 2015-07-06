#!/usr/bin/env python
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import settings.unixSettings as unixSettings
import recalboxFiles

fbaSettings = unixSettings.UnixSettings(recalboxFiles.fbaCustom)


# Map an emulationstation button name to the corresponding fba2x name
fba4bnts = {'a': 'Y', 'b': 'X', 'x': 'B', 'y': 'A', \
            'pageup': 'L', 'pagedown': 'R', \
            'start': 'START', 'select': 'SELECT'}
fba6bnts = {'a': 'L', 'b': 'Y', 'x': 'X', 'y': 'A', \
            'pageup': 'B', 'pagedown': 'R', \
            'start': 'START', 'select': 'SELECT'}

# Map an emulationstation direction to the corresponding fba2x
fbadirs = {'up': 'UP', 'down': 'DOWN', 'left': 'LEFT', 'right': 'RIGHT'}
fbaaxis = {'up': 'UD', 'down': 'UD', 'left': 'LR', 'right': 'LR'}
fbaHatToAxis = {'1' : 'UD', '2' : 'LR', '4' : 'UD', '8' : 'LR'}

# Map an emulationstation joystick to the corresponding fba2x
retroarchjoysticks = {'joystickup': 'l_y', 'joystickleft': 'l_x'}

# Map an emulationstation input type to the corresponding retroarch type
typetoname = {'button': 'btn', 'hat': 'btn', 'axis': 'axis', 'key': 'key'}

# Map an emulationstation input hat to the corresponding retroarch hat value
hatstoname = {'1': 'up', '2': 'right', '4': 'down', '8': 'left'}

# Map buttons to the corresponding fba2x specials keys
fbaspecials = {'start': 'QUIT', 'hotkey': 'HOTKEY'}

# Write a configuration for a specified controller
def writeControllersConfig(system, controllers):
    writeIndexes(controllers)
    for controller in controllers:
        writeControllerConfig(controllers[controller])


# Write a configuration for a specified controller
def writeControllerConfig(controller):
    generatedConfig = generateControllerConfig(controller)
    for key in generatedConfig:
        fbaSettings.save(key, generatedConfig[key])


# Create a configuration file for a given controller
def generateControllerConfig(controller):
    config = dict()
    for btnkey in fba4bnts:
        btnvalue = fba4bnts[btnkey]
        if btnkey in controller.inputs:
            input = controller.inputs[btnkey]
            config[btnkey] = input
    for dirkey in fbadirs:
        dirvalue = fbadirs[dirkey]
        if dirkey in controller.inputs:
            input = controller.inputs[dirkey]
            config['input_%s_%s' % (dirvalue, typetoname[input.type])] = getConfigValue(input)
    for jskey in retroarchjoysticks:
        jsvalue = retroarchjoysticks[jskey]
        if jskey in controller.inputs:
            input = controller.inputs[jskey]
            config['input_%s_minus_axis' % jsvalue] = '-%s' % input.id
            config['input_%s_plus_axis' % jsvalue] = '+%s' % input.id
    for specialkey in retroarchspecials:
        specialvalue = retroarchspecials[specialkey]
        if specialkey in controller.inputs:
            input = controller.inputs[specialkey]
            config['input_%s_%s' % (specialvalue, typetoname[input.type])] = getConfigValue(input)
    return config


# Returns the value to write in retroarch config file, depending on the type
def getConfigValue(input):
    if input.type == 'button':
        return input.id
    if input.type == 'axis':
        if input.value == '-1':
            return '-%s' % input.id
        else:
            return '+%s' % input.id
    if input.type == 'hat':
        return 'h' + input.id + hatstoname[input.value]
    if input.type == 'key':
        return input.id


# Write indexes for configured controllers
def writeIndexes(controllers):
    for player in controllers:
        controller = controllers[player]
        libretroSettings.save('input_player{}_joypad_index'.format(player), controller.index)


# TODO set analog dpad from system
# return the retroarch analog_dpad_mode
def getAnalogMode(controller):
    for dirkey in retroarchdirs:
        if dirkey in controller.inputs:
            if controller.inputs[dirkey].type is 'button' or controller.inputs[dirkey].type is 'hat':
                return '1'
    return '0'
