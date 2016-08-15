#!/usr/bin/env python
import os, sys
import recalboxFiles
import settings
from settings.unixSettings import UnixSettings
import subprocess
import json

mupenSettings = UnixSettings(recalboxFiles.mupenCustom, separator=' ')

def writeMupenConfig(system, controllers):
	setPaths()
	writeHotKeyConfig(controllers)
	if system.config['videomode'] != 'default':
		group, mode, drive = system.config['videomode'].split()
		setRealResolution(group, mode, drive)

	
def writeHotKeyConfig(controllers):
	if '1' in controllers:
		if 'hotkey' in controllers['1'].inputs:
			if 'start' in controllers['1'].inputs:
				mupenSettings.save('Joy Mapping Stop', "\"J{}{}/{}\"".format(controllers['1'].index, createButtonCode(controllers['1'].inputs['hotkey']), createButtonCode(controllers['1'].inputs['start'])))
			if 'y' in controllers['1'].inputs:	
				mupenSettings.save('Joy Mapping Save State', "\"J{}{}/{}\"".format(controllers['1'].index, createButtonCode(controllers['1'].inputs['hotkey']), createButtonCode(controllers['1'].inputs['y'])))
			if 'x' in controllers['1'].inputs:	
				mupenSettings.save('Joy Mapping Load State', "\"J{}{}/{}\"".format(controllers['1'].index, createButtonCode(controllers['1'].inputs['hotkey']), createButtonCode(controllers['1'].inputs['x'])))
			if 'pageup' in controllers['1'].inputs:	
				mupenSettings.save('Joy Mapping Screenshot', "\"J{}{}/{}\"".format(controllers['1'].index, createButtonCode(controllers['1'].inputs['hotkey']), createButtonCode(controllers['1'].inputs['pageup'])))
			if 'up' in controllers['1'].inputs:	
				mupenSettings.save('Joy Mapping Increment Slot', "\"J{}{}/{}\"".format(controllers['1'].index, createButtonCode(controllers['1'].inputs['hotkey']), createButtonCode(controllers['1'].inputs['up'])))
			if 'right' in controllers['1'].inputs:	
				mupenSettings.save('Joy Mapping Fast Forward', "\"J{}{}/{}\"".format(controllers['1'].index, createButtonCode(controllers['1'].inputs['hotkey']), createButtonCode(controllers['1'].inputs['right'])))

			
def createButtonCode(button):
	if(button.type == 'axis'):
		if button.value == '-1':
			return 'A'+button.id+'-'
		else:
			return 'A'+button.id+'+'
	if(button.type == 'button'):
		return 'B'+button.id
	if(button.type == 'hat'):
		return 'H'+button.id+'V'+button.value


def setRealResolution(group, mode, drive):
	# Use tvservice to get the real resolution
	groups = ['CEA', 'DMT']
	if group not in groups:
		sys.exit("{} is an unknown group. Can't switch to {} {} {}".format(group, group, mode, drive))
		
	drives = ['HDMI', 'DVI']
	if drive not in drives:
		sys.exit("{} is an unknown drive. Can't switch to {} {} {}".format(drive, group, mode, drive))
		
	proc = subprocess.Popen(["tvservice -j -m {}".format(group)], stdout=subprocess.PIPE, shell=True)
	(out, err) = proc.communicate()
	#print "program output:", out
	tvmodes = json.loads(out)
	
	for tvmode in tvmodes:
		if tvmode["code"] == int(mode):
			mupenSettings.save('ScreenWidth', "{}".format(tvmode["width"]))
			mupenSettings.save('ScreenHeight', "{}".format(tvmode["height"]))
			return
			
	sys.exit("The resolution for '{} {} {}' is not supported by your monitor".format(group, mode, drive))


def setPaths():
	mupenSettings.save('ScreenshotPath', recalboxFiles.SCREENSHOTS)
	mupenSettings.save('SaveStatePath', recalboxFiles.mupenSaves)
	mupenSettings.save('SaveSRAMPath', recalboxFiles.mupenSaves)
