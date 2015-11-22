#!/usr/bin/env python
import Command
import recalboxFiles
from generators.Generator import Generator
import kodiConfig

class KodiGenerator(Generator):
    # Main entry of the module
    # COnfigure kodi inputs and return the command to run
    def generate(self, system, rom, playersControllers):

        print "generating kodi"
        kodiConfig.writeKodiConfig(playersControllers)
        commandArray = [recalboxFiles.kodiBin, "--standalone", "-fs", "-n"]
        commandEnv = {'LD_LIBRARY_PATH':'/usr/lib/mysql'}
        return Command.Command(videomode=system.config['videomode'], array=commandArray, env=commandEnv)
