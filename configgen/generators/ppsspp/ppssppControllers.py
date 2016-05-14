#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import ConfigParser
import recalboxFiles

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import settings.unixSettings as unixSettings
import recalboxFiles

# This configgen is based on PPSSPP 1.2.2. Therefore, all code/github references are valid at this version, and may not be valid with later updates

# PPSSPP internal "NKCodes" https://github.com/hrydgard/ppsspp/blob/master/ext/native/input/keycodes.h#L198
# Will later be used to convert SDL input ids
NKCODE_BUTTON_1 = 188
NKCODE_BUTTON_2 = 189
NKCODE_BUTTON_3 = 190
NKCODE_BUTTON_4 = 191
NKCODE_BUTTON_5 = 192
NKCODE_BUTTON_6 = 193
NKCODE_BUTTON_7 = 194
NKCODE_BUTTON_8 = 195
NKCODE_BUTTON_9 = 196
NKCODE_BUTTON_10 = 197
NKCODE_BUTTON_11 = 198
NKCODE_BUTTON_12 = 199
NKCODE_BUTTON_13 = 200
NKCODE_BUTTON_14 = 201
NKCODE_BUTTON_15 = 202
NKCODE_BUTTON_16 = 203
JOYSTICK_AXIS_X = 0
JOYSTICK_AXIS_Y = 1
JOYSTICK_AXIS_HAT_X = 15
JOYSTICK_AXIS_HAT_Y = 16
JOYSTICK_AXIS_Z = 11
JOYSTICK_AXIS_RZ = 14
JOYSTICK_AXIS_LTRIGGER = 17
JOYSTICK_AXIS_RTRIGGER = 18
NKCODE_DPAD_UP = 19
NKCODE_DPAD_DOWN = 20
NKCODE_DPAD_LEFT = 21
NKCODE_DPAD_RIGHT = 22

# PPSSPP defined an offset for axis, see https://github.com/hrydgard/ppsspp/blob/eaeddc6c23cf86514f45199659ecc7396c91a3c0/Common/KeyMap.cpp#L694
AXIS_BIND_NKCODE_START = 4000

# From https://github.com/hrydgard/ppsspp/blob/master/ext/native/input/input_state.h#L26
DEVICE_ID_PAD_0 = 10
# SDL input ids conversion table to NKCodes
# See https://github.com/hrydgard/ppsspp/blob/master/SDL/SDLJoystick.h#L91
sdlIdToNKCode = {
		"0" : NKCODE_BUTTON_1,
		"1" : NKCODE_BUTTON_2,
		"2" : NKCODE_BUTTON_3,
		"3" : NKCODE_BUTTON_4,
		"4" : NKCODE_BUTTON_5,
		"5" : NKCODE_BUTTON_6,
		"6" : NKCODE_BUTTON_7,
		"7" : NKCODE_BUTTON_8,
		"8" : NKCODE_BUTTON_9,
		"9" : NKCODE_BUTTON_10,
		"10" : NKCODE_BUTTON_11,
		"11" : NKCODE_BUTTON_12,
		"12" : NKCODE_BUTTON_13,
		"13" : NKCODE_DPAD_UP,
		"14" : NKCODE_DPAD_DOWN,
		"15" : NKCODE_DPAD_LEFT,
		"16" : NKCODE_DPAD_RIGHT
}



SDLJoyAxisMap = {
		"0" : JOYSTICK_AXIS_X,
		"1" : JOYSTICK_AXIS_Y,
		"2" : JOYSTICK_AXIS_Z,
		"3" : JOYSTICK_AXIS_RZ,
		"4" : JOYSTICK_AXIS_LTRIGGER,
		"5" : JOYSTICK_AXIS_RTRIGGER
}

ppssppMapping =  { 'a' :             {'button': 'Circle'},
                   'b' :             {'button': 'Cross'},
                   'x' :             {'button': 'Triangle'},
                   'y' :             {'button': 'Square'},
                   'start' :         {'button': 'Start'},
                   'select' :        {'button': 'Select'},
                   'hotkey' :        {'button': 'Pause'},
                   'pageup' :        {'button': 'L'},
                   'pagedown' :      {'button': 'R'},
                   'joystick1left' : {'axis': 'An.Left'},
                   'joystick1up' :   {'axis': 'An.Up'},
                   'joystick2left' : {'axis': 'RightAn.Left'},
                   'joystick2up' :   {'axis': 'RightAn.Up'},
                   # The DPAD can be an axis (for gpio sticks for example) or a hat
                   'up' :            {'hat': 'Up',    'axis': 'Up',    'button': 'Up'},
                   'down' :          {'hat': 'Down',  'axis': 'Down',  'button': 'Down'},
                   'left' :          {'hat': 'Left',  'axis': 'Left',  'button': 'Left'},
                   'right' :         {'hat': 'Right', 'axis': 'Right', 'button': 'Right'},
                   # Need to add pseudo inputs as PPSSPP doesn't manually invert axises, and these are not referenced in es_input.cfg
                   'joystick1right' :{'axis': 'An.Right'},
                   'joystick1down' : {'axis': 'An.Down'},
                   'joystick2right' :{'axis': 'RightAn.Right'},
                   'joystick2down' : {'axis': 'RightAn.Down'}
}


# Create the controller configuration file
# returns its name
def generateControllerConfig(controller):
	# Set config file name
	configFileName = recalboxFiles.ppssppControls
	Config = ConfigParser.ConfigParser()
	Config.optionxform = str
	# We need to read the default file as PPSSPP needs the keyboard defs ine the controlls.ini file otherwise the GYUI won't repond
	Config.read(recalboxFiles.ppssppControlsInit)
	# As we start with the default ini file, no need to create the section
	section = "ControlMapping"

	# Parse controller inputs
	for index in controller.inputs:
		input = controller.inputs[index]
		if input.name not in ppssppMapping or input.type not in ppssppMapping[input.name]:
			continue
		
		var = ppssppMapping[input.name][input.type]
		
		code = input.code
		if input.type == 'button':
			pspcode = sdlIdToNKCode[input.id]
			val = "{}-{}".format( DEVICE_ID_PAD_0, pspcode )
			val = optionValue(Config, section, var, val)
			Config.set(section, var, val)
			
		elif input.type == 'axis':
			# Get the axis code
			nkAxisId = SDLJoyAxisMap[input.id]
			# Apply the magic axis formula
			pspcode = axisToCode(nkAxisId, int(input.value))
			val = "{}-{}".format( DEVICE_ID_PAD_0, pspcode )
			val = optionValue(Config, section, var, val)
			Config.set(section, var, val)
			
			# Also need to do the opposite direction manually. The input.id is the same as up/left, but the direction is opposite
			if input.name == 'joystick1up':
				var = ppssppMapping['joystick1down'][input.type]
			elif input.name == 'joystick1left':
				var = ppssppMapping['joystick1right'][input.type]
			elif input.name == 'joystick2up':
					var = ppssppMapping['joystick2down'][input.type]
			elif input.name == 'joystick2left':
				var = ppssppMapping['joystick2right'][input.type]
				
			pspcode = axisToCode(nkAxisId, -int(input.value))
			val = "{}-{}".format( DEVICE_ID_PAD_0, pspcode )
			val = optionValue(Config, section, var, val)
			Config.set(section, var, val)
		
		elif input.type == 'hat':
			var = ppssppMapping[input.name][input.type]
			if input.name == 'up':
				pspcode = axisToCode(JOYSTICK_AXIS_HAT_Y, -1)
			elif input.name == 'down':
				pspcode = axisToCode(JOYSTICK_AXIS_HAT_Y, 1)
			elif input.name == 'left':
				pspcode = axisToCode(JOYSTICK_AXIS_HAT_X, -1)
			elif input.name == 'right':
				pspcode = axisToCode(JOYSTICK_AXIS_HAT_X, 1)
			val = "{}-{}".format( DEVICE_ID_PAD_0, pspcode )
			val = optionValue(Config, section, var, val)
			Config.set(section, var, val)
		
	cfgfile = open(configFileName,'w+')
	Config.write(cfgfile)
	cfgfile.close()
	return configFileName


# Simple rewrite of https://github.com/hrydgard/ppsspp/blob/eaeddc6c23cf86514f45199659ecc7396c91a3c0/Common/KeyMap.cpp#L747
def axisToCode(axisId, direction) :
	if direction < 0:
		direction = 1
	else:
		direction = 0
	return AXIS_BIND_NKCODE_START + axisId * 2 + direction

# determine if the option already exists or not
def optionValue(config, section, option, value):
	if config.has_option(section, option):
		return "{},{}".format(config.get(section, option), value)
	else:
		return value
