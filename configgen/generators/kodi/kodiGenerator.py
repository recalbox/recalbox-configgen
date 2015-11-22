#!/usr/bin/env python
import Command
import recalboxFiles
from generators.Generator import Generator
import kodiConfig

class KodiGenerator(Generator):
    # Main entry of the module
    # Configure kodi inputs and return the command to run
    def generate(self, system, rom, playersControllers):
        kodiConfig.writeKodiConfig(playersControllers)
        commandArray = [recalboxFiles.kodiBin]
        return Command.Command(videomode=system.config['videomode'], array=commandArray)
