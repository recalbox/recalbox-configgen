#!/usr/bin/env python

# First draft of emulator launcher python revision

import argparse

import generators.libretro.libretroGenerator as libretroGen
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
libretro["psx"] = libretroGen.LibretroCore(name='psx', video_mode='4', corename='pcsx_rearmed', shaders='false')
libretro["psx"] = libretroGen.LibretroCore(name='snes', video_mode='4', corename='pocketsnes', shaders='false')

system = args.system

playersControllers = controllers.loadControllerConfig(args.p1index, args.p1guid, args.p1name, args.p2index, args.p2guid,
                                                      args.p2name, args.p3index, args.p3guid, args.p3name, args.p4index,
                                                      args.p4guid, args.p4name)


class Command:
    def __init__(self, videoMode, commandline):
        self.videoMode = videoMode
        self.commandLine = commandLine

# Main Program
# A generator ill configure its emulator, and return a command
if system in libretro:
    command = libretroGen.run(libretro[system], playersControllers)
    runner.run(command)
