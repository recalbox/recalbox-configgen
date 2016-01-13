#!/usr/bin/env python
import sys
import os
import ConfigParser

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from settings.unixSettings import UnixSettings
import recalboxFiles

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
    writeHotKeyConfig(controllers)

    for controller in controllers:
		player = controllers[controller]
		# Dynamic controller bindings
		# Write to file
		config = defineControllerKeys(player)
		writeToIni(player, config)


def writeHotKeyConfig(controllers):
    if '1' in controllers:
        if 'hotkey' in controllers['1'].inputs:
            mupenSettings.save('Joy Mapping Stop', "\"J{}B{}\"".format(controllers['1'].index, controllers['1'].inputs['hotkey'].id))

def defineControllerKeys(controller):
	config = dict()
	for inputIdx in controller.inputs:
		input = controller.inputs[inputIdx]
		if input.name in mupenPad:
			# Make a dict of a single element so that the next step is just a browse of the keySetting array
			if type(mupenPad[input.name]) is not dict:
				keySetting = {input.name: mupenPad[input.name]}
			else:
				keySetting = mupenPad[input.name]
			for name in keySetting:
				value=setControllerLine(input, keySetting[name])
				
				if keySetting[name] not in config :
					config[keySetting[name]] = value
				else:
					config[keySetting[name]] += " " + value

	return config

def setControllerLine(input, mupenSettingName):
	value = ''
	inputType = input.type
	if inputType == 'button':
		value = "button({})".format(input.id)
	elif inputType == 'hat':
		value = "hat({} {})".format(input.id, mupenHatToAxis[input.value])
	elif inputType == 'axis':
		if mupenSettingName in mupenDoubleAxis.values():
			# X axis : value = -1 for left, +1 for right
			# Y axis : value = -1 for up, +1 for down
			if input.value == "-1":				
				value = "axis({}-,{}+)".format(input.id, input.id)
			else:
				value = "axis({}+,{}-)".format(input.id, input.id)
		else:
			if (type(mupenPad[input.name]) is dict and mupenPad[input.name].keys()[mupenPad[input.name].values().index(mupenSettingName)] == "1") or input.value == "-1":
				value = "axis({}+)".format(input.id)
			else:
				value = "axis({}-)".format(input.id)
	return value


def writeToIni(controller, config):
	# Open file
	cfgfile = open(recalboxFiles.mupenInput,'w+')
	#Config.read(recalboxFiles.mupenCustom)
	# Set section name
	#section = "Input-SDL-Control{}".format(controller.index)
	section = controller.realName

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
