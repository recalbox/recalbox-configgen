#!/usr/bin/env python
import Command;

settingsRoot = "/recalbox/configs/retroarch"
settingsFileOrigin = settingsRoot + "/retroarchcustom.cfg.origin"
settingsFile = settingsRoot + "/retroarchcustom.cfg"

shadersRoot = "/recalbox/share/shaders/presets/"
shadersExt = ".gplsp"

retroarchBin = "retroarch"
retroarchCores = "/usr/lib/libretro/"


class LibretroCore():
    def __init__(self, name, videomode, core, shaders, ratio, smooth, rewind, configfile=None):
        self.name = name
        self.config = dict()
        self.config["videomode"] = videomode
        self.config["core"] = core
        self.config["shaders"] = shaders
        self.config["ratio"] = ratio
        self.config["smooth"] = smooth
        self.config["rewind"] = rewind
        self.config["configfile"] = configfile


# Main entry of the module
# Configure retroarch and return a command
def generate(system, playersControllers):
    # Write controllers configuration files
    # write options in retroarchcustom from env
    # set videomode
    # launch the emulator
    # video mode default
    print 'ok'
    if not system.config["configfile"]:
        # and system.config['configfile'] is not None :
        system.config['configfile'] = settingsFile

    retroarchCore = retroarchCores + system.config['core'] + ".so"

    commandline = "{} -L {} --config {}".format(retroarchBin, retroarchCore, system.config['configfile'])
    return Command.Command(videomode=system.config['videomode'], commandline=commandline)
