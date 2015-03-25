#!/usr/bin/env python

# First draft of emulator launcher python revision

import argparse
import os
import re
import readline
import sys
import settings.emulationstationSettings as esSettings
import settings.recalboxSettings as recalSettings
import settings.libretroSettings as libretroSettings
import generators.libretroGenerator as libretroGen
import controllersConfig as controllers

parser = argparse.ArgumentParser(description='emulator-launcher script')
parser.add_argument("-system", help="select the system to launch", type=str, required=True)
parser.add_argument("-p1index", help="player1 controller index", type=int, required=True)
parser.add_argument("-p1guid", help="player1 controller SDL2 guid", type=str, required=True)
parser.add_argument("-p1name", help="player1 controller name", type=str, required=True)
parser.add_argument("-p2index", help="player2 controller index", type=int, required=True)
parser.add_argument("-p2guid", help="player2 controller SDL2 guid", type=str, required=True)
parser.add_argument("-p2name", help="player2 controller name", type=str, required=True)
parser.add_argument("-p3index", help="player3 controller index", type=int, required=True)
parser.add_argument("-p3guid", help="player3 controller SDL2 guid", type=str, required=True)
parser.add_argument("-p3name", help="player3 controller name", type=str, required=True)
parser.add_argument("-p4index", help="player4 controller index", type=int, required=True)
parser.add_argument("-p4guid", help="player4 controller SDL2 guid", type=str, required=True)
parser.add_argument("-p4name", help="player4 controller name", type=str, required=True)


args = parser.parse_args()


# List libretro with their cores, and default video modes
libretro = dict()
libretro["psx"] = {'video_mode': 4, 'core': "pcsx_rearmed"}
libretro["snes"] = {'video_mode': 4, 'core': "pocketsnes"}


system = args.system


def loadEnvConfig(system) :
	smooth = esSettings.load("Smooth")
	shaders = esSettings.load("Shaders")
	ratio = esSettings.load("GameRatio")
	video_mode = recalSettings.load(system+"_video_mode")
	custom_emulator = recalSettings.load(system+"_emulator")
	if shaders == "true" :
		smooth = false
	return { 'smooth' : smooth, 'shaders' : shaders, 'ratio' : ratio, 'video_mode' : video_mode,\
		 'custom_emulator' : custom_emulator } 
	

envConfig = loadEnvConfig(system)
playersControllers = controllers.loadControllersConfig(args.p1index, args.p1guid, args.p1name, args.p2index, args.p2guid, args.p2name, args.p3index, args.p3guid, args.p3name, args.p4index, args.p4guid, args.p4name)


# Main Program
if system in libretro :
	libretroGen.run(libretro[system], envConfig, playersControllers)
