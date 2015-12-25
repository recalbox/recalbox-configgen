#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import settings.unixSettings as unixSettings
import recalboxFiles

moonlightBtns   = {'a': 'btn_east', 'b': 'btn_south', 'y': 'btn_west', 'x': 'btn_north',\
                 'pageup': 'btn_tl', 'pagedown': 'btn_tr', \
                 'l2': 'btn_tl2', 'r2': 'btn_tr2',\
                 'l3': 'btn_thumbl', 'r3': 'btn_thumbr',\
                 'start': 'btn_start', 'select': 'btn_select', 'hotkey': 'btn_mode',\
                 'up': 'btn_dpad_up', 'down': 'btn_dpad_down', 'left': 'btn_dpad_left', 'right': 'btn_dpad_right'}
moonlightHat    = {'up': 'abs_dpad_x', 'left': 'abs_dpad_y'}
moonlightAxis   = {'joystick1left': 'abs_x', 'joystick1up': 'abs_y', \
                   'joystick2left': 'abs_rx', 'joystick2up': 'abs_ry', \
                   'l2': 'abs_z', 'r2': 'abs_rz'}

# Returns an array
# Index = mapping configuration file for player X
# Value = device path associated to the index
def writeControllersConfig(system, rom, controllers):
    config = dict()
    for controller in controllers:
        playerConfig = generateControllerConfig(controller, controllers[controller])
        confFile = recalboxFiles.moonlightMapping[int(controller)]
        mappingFile = unixSettings.UnixSettings(confFile, ' ')
        mappingFile.save("# Device name", controllers[controller].realName)
        mappingFile.save("# SDL2 GUID  ", controllers[controller].guid)
        mappingFile.save("# Event path ", controllers[controller].dev)
        for input in playerConfig:
            mappingFile.save(input, playerConfig[input])
            config[confFile] = controllers[controller].dev
    return config


# Create a configuration file for a given controller
# returns an array :
# Index = Moonlight configuration parameter
# Value = the code extracted from es_input.cfg corresponding to the index
# ex : ['btn_select'] = 296
def generateControllerConfig(player, controller):
    config = dict()
   
    for inputIdx in controller.inputs:
        input = controller.inputs[inputIdx]
        inputType = input.type
        if inputType == 'button':
            mlBtn = moonlightBtns[inputIdx]
            config[mlBtn] = input.code
        elif inputType == 'hat' and inputIdx in moonlightHat:
            mlHat = moonlightHat[inputIdx]
            config[mlHat] = input.code
        elif inputType == 'axis':
            mlAxis = moonlightAxis[inputIdx]
            config[mlAxis] = input.code
        # else :
            # print input.name + ' not supported'

    # Second pass : set unmapped buttons/axis/hat to -1
    fullKeys = dict()
    fullKeys.update(moonlightBtns)
    fullKeys.update(moonlightHat)
    fullKeys.update(moonlightAxis)
    for idx in fullKeys:
        mlName = fullKeys[idx]
        if mlName not in config:
            config[mlName] = "-1"
    
    # DIRTY HACK : ABS_HAT0Y is not yet managed by es_input.cfg. Add it manually
    hats = {'10':'11', '12':'13', '14':'15', '16':'17'}
    if 'abs_dpad_x' in config:
        value = config['abs_dpad_x']
        if value != "-1":
            config['abs_dpad_y'] = hats[value]
    
    # DIRTY HACK ! missing DPAD buttons
    if 'btn_dpad_up' not in config:
        config['btn_dpad_up'] = "-1"
    if 'btn_dpad_left' not in config:
        config['btn_dpad_left'] = "-1"
            
    # Add unhandled config
    config['reverse_x']         = "false"
    config['reverse_y']         = "true"
    config['reverse_rx']        = "false"
    config['reverse_ry']        = "true"
    config['reverse_dpad_x']    = "false"
    config['reverse_dpad_y']    = "false"
    config['abs_deadzone']      = "4"
    
    return config

