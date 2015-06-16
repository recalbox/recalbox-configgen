#!/usr/bin/env python

# First draft of emulator launcher python revision

import argparse

import generators.libretro.libretroGenerator as libretroGen
import controllersConfig as controllers
import settings.recalboxSettings as recalSettings


parser = argparse.ArgumentParser(description='emulator-launcher script')
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
parser.add_argument("-system", help="select the system to launch", type=str, required=True)
parser.add_argument("-rom", help="rom absolute path", type=str, required=True)

args = parser.parse_args()


# List libretro with their cores, and default video modes

libretro = dict()
libretro["psx"] = libretroGen.LibretroCore(name='psx', videomode='4', emulator='pcsx_rearmed', shaders='', ratio='auto',
                                           smooth='1', rewind='0')
libretro["snes"] = libretroGen.LibretroCore(name='snes', videomode='4', emulator='pocketsnes', shaders='', ratio='auto',
                                            smooth='1', rewind='0')

system = args.system

# Read the controller configuration
playersControllers = controllers.loadControllerConfig(args.p1index, args.p1guid, args.p1name, args.p2index, args.p2guid,
                                                      args.p2name, args.p3index, args.p3guid, args.p3name, args.p4index,
                                                      args.p4guid, args.p4name)

# Main Program
# A generator will configure its emulator, and return a command
if system in libretro:
    # Get the default configuration of the core
    settings = libretro[system].config
    # Get the recalbox.conf global configuration
    recalFileSettings = recalSettings.loadAll("global")
    # Get the recalbox.conf core configuration
    coreSettings = recalSettings.loadAll(system.name)

    # Override the default config with the global one
    settings.update(recalFileSettings)
    # Override the config with the core specific one
    settings.update(coreSettings)

    # Create the retroarch config file, the controllers
    command = libretroGen.run(libretro[system], playersControllers)
    runner.run(command)
