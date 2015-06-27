#!/usr/bin/env python
import Command
import libretroControllers
import settings.libretroSettings as libretroSettings
import recalboxFiles
import libretroConfig

settingsFile = recalboxFiles.retroarchCustom

shadersRoot = recalboxFiles.shadersRoot

retroarchBin = recalboxFiles.retroarchBin
retroarchCores = recalboxFiles.retroarchCores
shadersExt = '.gplsp'
libretroExt = '_libretro.so'


# Main entry of the module
# Configure retroarch and return a command
def generate(system, rom, playersControllers):
    # Settings recalbox default config file if no user defined one
    if not system.config['configfile']:
        # Using recalbox config file
        system.config['configfile'] = settingsFile
        # Create retroarchcustom.cfg if does not exists
        libretroSettings.copyFromOriginal()
        #  Write controllers configuration files
        libretroControllers.writeControllersConfig(system, playersControllers)
        # Write configuration to retroarchcustom.cfg
        libretroConfig.writeLibretroConfig(system)

    # Retroarch core on the filesystem
    retroarchCore = retroarchCores + system.config['core'] + libretroExt

    # the command to run
    commandline = '{} -L "{}" --config "{}" "{}"'.format(retroarchBin, retroarchCore, system.config['configfile'], rom)
    return Command.Command(videomode=system.config['videomode'], commandline=commandline)
