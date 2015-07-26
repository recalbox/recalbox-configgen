#!/usr/bin/env python
import Command
import libretroControllers
import recalboxFiles
import libretroConfig
import shutil
from generators.Generator import Generator
import os.path


class LibretroGenerator(Generator):
    # Main entry of the module
    # Configure retroarch and return a command
    def generate(self, system, rom, playersControllers):
        # Settings recalbox default config file if no user defined one
        if not system.config['configfile']:
            # Using recalbox config file
            system.config['configfile'] = recalboxFiles.retroarchCustom
            # Create retroarchcustom.cfg if does not exists
            if not os.path.isfile(recalboxFiles.retroarchCustomOrigin):
                shutil.copyfile(recalboxFiles.retroarchCustomOrigin, recalboxFiles.retroarchCustom)
            #  Write controllers configuration files
            libretroControllers.writeControllersConfig(system, playersControllers)
            # Write configuration to retroarchcustom.cfg
            libretroConfig.writeLibretroConfig(system)

        # Retroarch core on the filesystem
        retroarchCore = recalboxFiles.retroarchCores + system.config['core'] + recalboxFiles.libretroExt

        # the command to run
        commandline = '{} -L "{}" --config "{}" "{}"'.format(recalboxFiles.retroarchBin, retroarchCore, system.config['configfile'], rom)
        return Command.Command(videomode=system.config['videomode'], commandline=commandline)
