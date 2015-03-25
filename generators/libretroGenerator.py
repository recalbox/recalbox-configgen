#!/usr/bin/env python

settingsRoot = "/recalbox/configs/retroarch"
settingsFileOrigin = settingsRoot + "/retroarchcustom.cfg.origin"
settingsFile = settingsRoot + "/retroarchcustom.cfg"

# Configure and run retroarch
# Main entry of the module
def run(system, videoConfig, playersControllers) :
    


# Map an emulationstation button name to the corresponding retroarch name
retroarchbtns = { 'a' : 'a', 'b' : 'b', 'x' : 'x', 'y' : 'y', \
		'pageup' : 'l', 'pagedown' : 'r', 'l2' : 'l2', 'r2' : 'r2', \
		'start' : 'start', 'select' : 'select' }

# Map an emulationstation direction to the corresponding retroarch
retroarchdirs = { 'up' : 'up', 'down' : 'down', 'left' : 'left', 'right' : 'right' }

# Map an emulationstation joystick to the corresponding retroarch
retroarchjoysticks = { 'joystickup' : 'l_y', 'joystickleft' : 'l_x' }

# Map an emulationstation input type to the corresponding retroarch type
typetoname = { 'button' : 'btn', 'hat' : 'btn', 'axis' : 'axis', 'key' : 'key' }

# Map an emulationstation input hat to the corresponding retroarch hat value
retroarchhats = { '1' : 'up', '2' : 'right', '4' : 'down', '8' : 'left' }

# Map buttons to the corresponding retroarch specials keys
retroarchspecials = { 'x' : 'load_state', 'y' : 'save_state', 'pageup' : 'screenshot', \
		      'b' : 'menu_toggle', 'start' : 'exit_emulator', 'up' : 'state_slot_increase', \
		      'down' : 'state_slot_decrease', 'left' : 'rewind', 'right' : 'hold_fast_forward' } 



# Write a configuration for a specified controller
def writeControllerConfig(controller) :
    configFile = settingsRoot+"/inputs/"+controller.realName+".cfg"
    f = open(configFile,'w')
    generatedConfig = generateControllerConfig(controller)
    f.write(generatedConfig)
    f.close() 	


# Create a configuration file for a given controller
def generateControllerConfig(controller) :
    config = 'input_device = "%s"\n' % controller.realName
    config += 'input_driver = "udev"\n'
    for btnkey in retroarchbtns:
        btnvalue = retroarchbtns[btnkey]
	if btnkey in controller.inputs:
		input = controller.inputs[btnkey]
		config += "input_%s_%s = %s\n" % (btnvalue, typetoname[input.type], getConfigValue(input))
    for dirkey in retroarchdirs:
        dirvalue = retroarchdirs[dirkey]
	if dirkey in controller.inputs:
		input = controller.inputs[dirkey]
		config += "input_%s_%s = %s\n" % (dirvalue, typetoname[input.type], getConfigValue(input))
    for jskey in retroarchjoysticks:
        jsvalue = retroarchjoysticks[jskey]
	if jskey in controller.inputs:
		input = controller.inputs[jskey]
		getConfigValue(input)
		config += "input_%s_minus_axis = %s\n" % (jsvalue, "-"+input.id)
		config += "input_%s_plus_axis = %s\n" % (jsvalue, "+"+input.id)
    for specialkey in retroarchspecials:
        specialvalue = retroarchspecials[specialkey]
	if specialkey in controller.inputs:
		input = controller.inputs[specialkey]
		config += "input_%s_%s = %s\n" % (specialvalue, typetoname[input.type], getConfigValue(input))
    return config

# Returns the value to put in retroarch config file, depending on the type
def getConfigValue(input):
    if input.type == "button":
	return input.id
    if input.type == "axis":
        if input.value == "-1":
            return "-%s" % input.id
        else :
	    return "+%s" % input.id
    if input.type == "hat":
        return "h"+input.id+retroarchhats[input.value]
    if input.type == "key":
        return input.id
