#!/usr/bin/env python
import Command
import moonlightControllers
import recalboxFiles
from generators.Generator import Generator
import shutil
import os.path


class MoonlightGenerator(Generator):
    # Main entry of the module
    # Configure fba and return a command
    def generate(self, system, rom, playersControllers):
        config = moonlightControllers.writeControllersConfig(system, rom, playersControllers)
        gameName = self.getRealGameName(rom)
        # the command to run
        # stream -remote -keydir ${moonlight_keydir} -${moonlight_screen} -${moonlight_fps} -mapping ${moonlight_mapping} -app \"$game\" ${moonlight_ip}"
        # commandArray = [recalboxFiles.moonlightBin, 'stream','-remote', '-keydir', recalboxFiles.moonlightCustom + '/keydir', '-720',  '-60fps']
        commandArray = [recalboxFiles.moonlightBin, 'stream','-config',  recalboxFiles.moonlightConfig]
        for mapping in config:
            commandArray.append('-mapping')
            commandArray.append(mapping)
            commandArray.append('-input')
            commandArray.append(config[mapping])
        commandArray.append('-app')
        commandArray.append(gameName)
        return Command.Command(videomode='default', array=commandArray)

    def getRealGameName(self, rom):
        # Rom's basename without extension
        romName = os.path.splitext(os.path.basename(rom))[0]
        # find the real game name
        f = open(recalboxFiles.moonlightGamelist, 'r')
        for line in f:
            gfeRom = line.split(';')[0].strip()
            gfeGame = line.split(';')[1].strip()
            #If found
            if gfeRom == romName:
                # return it
                f.close()
                return gfeGame