#!/usr/bin/env python
import Command
import recalboxFiles
from generators.Generator import Generator
import os.path
import glob


class ViceGenerator(Generator):
    # Main entry of the module
    # Return command
    def generate(self, system, rom, playersControllers):
        # Settings recalbox default config file if no user defined one
        if not system.config['configfile']:
            # Using recalbox config file
            #system.config['configfile'] = recalboxFiles.mupenCustom
            pass
        # Find rom path
        romPath = os.path.dirname(rom)
        romName = os.path.splitext(os.path.basename(rom))[0]

        commandArray = [recalboxFiles.recalboxBins[system.config['emulator']], 
                        "-config", recalboxFiles.viceConfig,
                        "-autostart", rom]

        return Command.Command(videomode='default', array=commandArray,  env={"SDL_VIDEO_GL_DRIVER": "/usr/lib/libGLESv2.so"})
