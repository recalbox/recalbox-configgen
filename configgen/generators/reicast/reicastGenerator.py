#!/usr/bin/env python
import Command
#~ import reicastControllers
import recalboxFiles
from generators.Generator import Generator
import reicastControllers
import shutil
import os.path
import ConfigParser


class ReicastGenerator(Generator):
    # Main entry of the module
    # Configure fba and return a command
    def generate(self, system, rom, playersControllers):
        if not system.config['configfile']:
            # Overwrite emu.cfg : it can be empty on a crash during configgen
            shutil.copyfile(recalboxFiles.reicastConfigInit, recalboxFiles.reicastConfig)
            # Write emu.cfg to map joysticks
            # For each pad detected
            Config = ConfigParser.ConfigParser()
            Config.read(recalboxFiles.reicastConfig)
            section = "input"
            for index in playersControllers :
                controller = playersControllers[index]
                # Get the event number
                eventNum = controller.dev.replace('/dev/input/event','')
                # Write its mapping file
                controllerConfigFile = reicastControllers.generateControllerConfig(controller)
                # set the evdev_device_id_X
                Config.set(section, 'evdev_device_id_' + controller.player, eventNum)
                # Set the evdev_mapping_X
                Config.set(section, 'evdev_mapping_' + controller.player, controllerConfigFile)

            cfgfile = open(recalboxFiles.reicastConfig,'w+')
            Config.write(cfgfile)
            cfgfile.close()
                
        # the command to run  
        commandArray = [recalboxFiles.reicastBin, rom]
        # Here is the trick to make reicast find files :
        # emu.cfg is in $XDG_CONFIG_DIRS or $XDG_CONFIG_HOME. The latter is better
        # VMU will be in $XDG_DATA_HOME because it needs rw access -> /recalbox/share/saves/dreamcast
        # BIOS will be in $XDG_DATA_DIRS
        # controller cfg files are set with an absolute path, so no worry
        return Command.Command(videomode=system.config['videomode'], array=commandArray, env={"XDG_CONFIG_HOME":recalboxFiles.CONF, "XDG_DATA_HOME":recalboxFiles.reicastSaves, "XDG_DATA_DIRS":recalboxFiles.reicastBios})
