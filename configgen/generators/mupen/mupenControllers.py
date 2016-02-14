#!/usr/bin/env python
import sys
import os
import ConfigParser

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from settings.unixSettings import UnixSettings
import recalboxFiles

# Must read :
# http://mupen64plus.org/wiki/index.php?title=Mupen64Plus_Plugin_Parameters

mupenSettings = UnixSettings(recalboxFiles.mupenCustom, separator=' ')
Config = ConfigParser.ConfigParser()
# To prevent ConfigParser from converting to lower case
Config.optionxform = str

# Mupen doesn't like to have 2 buttons mapped for N64 pad entry. That's why r2 is commented for now. 1 axis and 1 button is ok
mupenPad = { 'up': 'DPad U', 'down': 'DPad D', 'left': 'DPad L', 'right': 'DPad R'
			, 'start': 'Start', 'y': 'B Button', 'b': 'A Button'
			, 'pagedown': 'R Trig', 'l2': 'Z Trig', 'pageup': 'L Trig'
			, 'joystick1left': 'X Axis', 'joystick1up': 'Y Axis'
			, 'joystick2left': {'-1':'C Button L', '1': 'C Button R'}, 'joystick2up': {'-1':'C Button U', '1': 'C Button D'}
			, 'x': 'C Button U', 'a': 'C Button R'
			#, 'r2': 'R Trig'
}
mupenHatToAxis = {'1': 'Up', '2': 'Right', '4': 'Down', '8': 'Left'}
mupenDoubleAxis = {0:'X Axis', 1:'Y Axis'}

# Write a configuration for a specified controller
def writeControllersConfig(controllers):
	if os.path.isfile(recalboxFiles.mupenInput):
		os.remove(recalboxFiles.mupenInput)

	for controller in controllers:
		player = controllers[controller]
		# Dynamic controller bindings
		config = defineControllerKeys(player)
		# Write to file
		writeToIni(player, config)


def defineControllerKeys(controller):
	# config holds the final pad configuration in the mupen style
	# ex: config['DPad U'] = "button(1)"
	config = dict()
	for inputIdx in controller.inputs:
		input = controller.inputs[inputIdx]
		if input.name in mupenPad:
			# Make a dict of a single element so that the next step is just a browse of the keySetting array
			# With this trick, handle a single button Joystick2up just the same
			if type(mupenPad[input.name]) is not dict:
				keySetting = {input.name: mupenPad[input.name]}
			else:
				keySetting = mupenPad[input.name]

			for name in keySetting:
				value=setControllerLine(input, keySetting[name])
				# Handle multiple inputs for a single N64 Pad input
				if keySetting[name] not in config :
					config[keySetting[name]] = value
				else:
					config[keySetting[name]] += " " + value

	# Big dirty hack : handle when the pad has no analog sticks. Only Start A, B L and R survive from the previous configuration
	if "X Axis" not in config and "Y Axis" not in config:
		# remap Z Trig
		config['Z Trig'] = setControllerLine(controller.inputs['x'], "Z Trig")
		# remove C Button U and R
		if 'C Button U' in config: del config['C Button U']
		if 'C Button R' in config: del config['C Button R']
		# remove DPad
		if 'DPad U' in config:del config['DPad U']
		if 'DPad D' in config:del config['DPad D']
		if 'DPad L' in config:del config['DPad L']
		if 'DPad R' in config:del config['DPad R']
		# Remap up/down/left/right to  X and Y Axis
		if controller.inputs['left'].type == 'hat':
			config['X Axis'] = "hat({} {} {})".format(controller.inputs['left'].id, mupenHatToAxis[controller.inputs['left'].value], mupenHatToAxis[controller.inputs['right'].value])
			config['Y Axis'] = "hat({} {} {})".format(controller.inputs['up'].id, mupenHatToAxis[controller.inputs['up'].value], mupenHatToAxis[controller.inputs['down'].value])
		elif controller.inputs['left'].type == 'axis':
			config['X Axis'] = setControllerLine(controller.inputs['left'], "X Axis")
			config['Y Axis'] = setControllerLine(controller.inputs['up'], "Y Axis")
		elif controller.inputs['left'].type == 'button':
			config['X Axis'] = "button({},{})".format(controller.inputs['left'].id, controller.inputs['right'].id)
			config['Y Axis'] = "button({},{})".format(controller.inputs['up'].id, controller.inputs['down'].id)
	return config


def setControllerLine(input, mupenSettingName):
	value = ''
	inputType = input.type
	if inputType == 'button':
		value = "button({})".format(input.id)
	elif inputType == 'hat':
		value = "hat({} {})".format(input.id, mupenHatToAxis[input.value])
	elif inputType == 'axis':
		# Generic case for joystick1up and joystick1left
		if mupenSettingName in mupenDoubleAxis.values():
			# X axis : value = -1 for left, +1 for right
			# Y axis : value = -1 for up, +1 for down
			if input.value == "-1":				
				value = "axis({}-,{}+)".format(input.id, input.id)
			else:
				value = "axis({}+,{}-)".format(input.id, input.id)
		else:
			# Here is the case for joystick2up and joystick2left
			if type(mupenPad[input.name]) is dict:
				if mupenPad[input.name].keys()[mupenPad[input.name].values().index(mupenSettingName)] == "1":
					value = "axis({}+)".format(input.id)
				else:
					value = "axis({}-)".format(input.id)
			# Case of triggers L2/R2
			else : 
				if input.value == "1":
					value = "axis({}+)".format(input.id)
				else:
					value = "axis({}-)".format(input.id)

	return value


def writeToIni(controller, config):
	Config.read(recalboxFiles.mupenInput)
	section = controller.realName

	# Avoid a crash when writing twice a same section
	if Config.has_section(section):
		return None

	# Open file
	cfgfile = open(recalboxFiles.mupenInput,'w+')

	# Write static config
	Config.add_section(section)
	Config.set(section, 'plugged', True)
	Config.set(section, 'plugin', 2)
	Config.set(section, 'AnalogDeadzone', "4096,4096")
	Config.set(section, 'AnalogPeak', "32768,32768")
	Config.set(section, 'Mempak switch', "")
	Config.set(section, 'Rumblepak switch', "")
	Config.set(section, 'mouse', "False")
	#Config.set(section, 'name', controller.realName)
	#Config.set(section, 'device', controller.index)

	# Write dynamic config
	for inputName in sorted(config):
		Config.set(section, inputName, config[inputName])

	Config.write(cfgfile)
	cfgfile.close()
