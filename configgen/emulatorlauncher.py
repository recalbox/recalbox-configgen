#!/usr/bin/env python

import argparse
import time

from Emulator import Emulator
import generators
from generators.libretro.libretroGenerator import LibretroGenerator
from generators.fba2x.fba2xGenerator import Fba2xGenerator
from generators.mupen.mupenGenerator import MupenGenerator
from generators.configManager import ConfigManager
import controllersConfig as controllers
import utils.runner as runner
import signal

generators = {
    'libretro': LibretroGenerator(),
    'fba2x': Fba2xGenerator(),
    'mupen64plus': MupenGenerator()
}

# List emulators with their cores rest mupen64, scummvm
emulators = dict()
# Nintendo
emulators["snes"] = Emulator(name='snes', emulator='libretro', core='pocketsnes')
emulators["nes"] = Emulator(name='nes', emulator='libretro', core='fceunext')
emulators["n64"] = Emulator(name='n64', emulator='mupen64plus', core='n64')
emulators["gba"] = Emulator(name='gba', emulator='libretro', core='gpsp')
emulators["gb"] = Emulator(name='gb', emulator='libretro', core='gambatte')
emulators["gbc"] = Emulator(name='gbc', emulator='libretro', core='gambatte')
emulators["fds"] = Emulator(name='fds', emulator='libretro', core='nestopia')
emulators["virtualboy"] = Emulator(name='virtualboy', emulator='libretro', core='vb')
# Sega
emulators["sg1000"] = Emulator(name='sg1000', emulator='libretro', core='genesisplusgx')
emulators["mastersystem"] = Emulator(name='mastersystem', emulator='libretro', core='picodrive')
emulators["megadrive"] = Emulator(name='megadrive', emulator='libretro', core='picodrive')
emulators["gamegear"] = Emulator(name='gamegear', emulator='libretro', core='genesisplusgx')
emulators["sega32x"] = Emulator(name='sega32x', emulator='libretro', core='picodrive')
emulators["segacd"] = Emulator(name='segacd', emulator='libretro', core='picodrive')
# Arcade
emulators["neogeo"] = Emulator(name='neogeo', emulator='fba2x')
emulators["mame"] = Emulator(name='mame', emulator='libretro', core='mame078')
emulators["fba"] = Emulator(name='fba', emulator='fba2x')
emulators["fbalibretro"] = Emulator(name='fbalibretro', emulator='libretro', core='fba')
#
emulators["ngp"] = Emulator(name='ngp', emulator='libretro', core='mednafen_ngp')
emulators["gw"] = Emulator(name='gw', emulator='libretro', core='gw')
emulators["vectrex"] = Emulator(name='vectrex', emulator='libretro', core='vecx')
emulators["lynx"] = Emulator(name='lynx', emulator='libretro', core='mednafen_lynx')
emulators["lutro"] = Emulator(name='lutro', emulator='libretro', core='lutro')
emulators["wswan"] = Emulator(name='wswan', emulator='libretro', core='mednafen_wswan', ratio='16/10')
emulators["pcengine"] = Emulator(name='pcengine', emulator='libretro', core='mednafen_supergrafx')
emulators["atari2600"] = Emulator(name='atari2600', emulator='libretro', core='stella')
emulators["atari7800"] = Emulator(name='atari7800', emulator='libretro', core='prosystem')
emulators["msx"] = Emulator(name='msx', emulator='libretro', core='fmsx')
emulators["prboom"] = Emulator(name='prboom', emulator='libretro', core='prboom')
emulators["psx"] = Emulator(name='psx', emulator='libretro', core='pcsx_rearmed')
emulators["cavestory"] = Emulator(name='cavestory', emulator='libretro', core='nxengine')


def signal_handler(signal, frame):
    print('Exiting')
    if runner.proc:
        print('killing runner.proc')
        runner.proc.kill()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser(description='emulator-launcher script')
    parser.add_argument("-p1index", help="player1 controller index", type=int, required=False)
    parser.add_argument("-p1guid", help="player1 controller SDL2 guid", type=str, required=False)
    parser.add_argument("-p1name", help="player1 controller name", type=str, required=False)
    parser.add_argument("-p1devicepath", help="player1 controller device", type=str, required=False)
    parser.add_argument("-p2index", help="player2 controller index", type=int, required=False)
    parser.add_argument("-p2guid", help="player2 controller SDL2 guid", type=str, required=False)
    parser.add_argument("-p2name", help="player2 controller name", type=str, required=False)
    parser.add_argument("-p2devicepath", help="player2 controller device", type=str, required=False)
    parser.add_argument("-p3index", help="player3 controller index", type=int, required=False)
    parser.add_argument("-p3guid", help="player3 controller SDL2 guid", type=str, required=False)
    parser.add_argument("-p3name", help="player3 controller name", type=str, required=False)
    parser.add_argument("-p3devicepath", help="player3 controller device", type=str, required=False)
    parser.add_argument("-p4index", help="player4 controller index", type=int, required=False)
    parser.add_argument("-p4guid", help="player4 controller SDL2 guid", type=str, required=False)
    parser.add_argument("-p4name", help="player4 controller name", type=str, required=False)
    parser.add_argument("-p4devicepath", help="player4 controller device", type=str, required=False)
    parser.add_argument("-system", help="select the system to launch", type=str, required=True)
    parser.add_argument("-rom", help="rom absolute path", type=str, required=True)
    parser.add_argument("-demo", help="mode demo", type=bool, required=False)

    args = parser.parse_args()

    playersControllers = dict()
    if not args.demo:
        # Read the controller configuration
        playersControllers = controllers.loadControllerConfig(args.p1index, args.p1guid, args.p1name, args.p2index,
                                                              args.p2guid,
                                                              args.p2name, args.p3index, args.p3guid, args.p3name,
                                                              args.p4index,
                                                              args.p4guid, args.p4name)

    systemName = args.system

    # Main Program
    # A generator will configure its emulator, and return a command
    if systemName in emulators:
        system = emulators[systemName]
        systemManager = ConfigManager()

        systemManager.configure(system)
        command = generators[system.config['emulator']].generate(system, args.rom, playersControllers)
        runner.runCommand(command)
        time.sleep(1)
