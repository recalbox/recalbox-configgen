#!/usr/bin/env python

# First draft of emulator launcher python revision

import argparse

from Emulator import Emulator
import generators
import generators.libretro.libretroGenerator as libretroGen
import controllersConfig as controllers
import settings.recalboxSettings as recalSettings
import utils.runner as runner


parser = argparse.ArgumentParser(description='emulator-launcher script')
parser.add_argument("-p1index", help="player1 controller index", type=int, required=False)
parser.add_argument("-p1guid", help="player1 controller SDL2 guid", type=str, required=False)
parser.add_argument("-p1name", help="player1 controller name", type=str, required=False)
parser.add_argument("-p2index", help="player2 controller index", type=int, required=False)
parser.add_argument("-p2guid", help="player2 controller SDL2 guid", type=str, required=False)
parser.add_argument("-p2name", help="player2 controller name", type=str, required=False)
parser.add_argument("-p3index", help="player3 controller index", type=int, required=False)
parser.add_argument("-p3guid", help="player3 controller SDL2 guid", type=str, required=False)
parser.add_argument("-p3name", help="player3 controller name", type=str, required=False)
parser.add_argument("-p4index", help="player4 controller index", type=int, required=False)
parser.add_argument("-p4guid", help="player4 controller SDL2 guid", type=str, required=False)
parser.add_argument("-p4name", help="player4 controller name", type=str, required=False)
parser.add_argument("-system", help="select the system to launch", type=str, required=True)
parser.add_argument("-rom", help="rom absolute path", type=str, required=True)

args = parser.parse_args()


generators = {
    'libretro': generators.libretro.libretroGenerator.generate
}

# List emulators with their cores
emulators = dict()
emulators["psx"] = Emulator(name='psx', emulator='libretro', core='pcsx_rearmed')
emulators["snes"] = Emulator(name='snes', emulator='libretro', core='pocketsnes')
emulators["nes"] = Emulator(name='nes', emulator='libretro')
emulators["neogeo"] = Emulator(name='neogeo', emulator='fba2x')
emulators["fba"] = Emulator(name='fba', emulator='fba2x')



# Read the controller configuration
playersControllers = controllers.loadControllerConfig(args.p1index, args.p1guid, args.p1name, args.p2index, args.p2guid,
                                                      args.p2name, args.p3index, args.p3guid, args.p3name, args.p4index,
                                                      args.p4guid, args.p4name)

systemName = args.system

# Load recalbox.conf configuration
recalFileSettings = recalSettings.loadAll(systemName)

# Main Program
# A generator will configure its emulator, and return a command
if systemName in emulators :
    system = emulators[systemName]
    # Get the default configuration of the core
    systemSettings = system.config
    # Get the recalbox.conf core configuration
    coreSettings = recalSettings.loadAll(system.name)
    # Override the default config with the global one
    systemSettings.update(recalFileSettings)
    # Override the config with the core specific one
    systemSettings.update(coreSettings)

    command = generators[system.config['emulator']].generate(system, args.rom, playersControllers)
    runner.runCommand(command)