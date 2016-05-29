#!/usr/bin/env python
import Command
#~ import reicastControllers
import recalboxFiles
from generators.Generator import Generator
import ppssppControllers
import shutil
import os.path
import ConfigParser


class PPSSPPGenerator(Generator):
    # Main entry of the module
    # Configure fba and return a command
    def generate(self, system, rom, playersControllers):
        if not system.config['configfile']:
            # Write emu.cfg to map joysticks, init with the default emu.cfg
            Config = ConfigParser.ConfigParser()
            Config.read(recalboxFiles.reicastConfigInit)
            section = "input"
            # For each pad detected
            for index in playersControllers :
                controller = playersControllers[index]
                # we only care about player 1
                if controller.player != "1":
                    continue
                ppssppControllers.generateControllerConfig(controller)

        # the command to run  
        #~ commandArray = [recalboxFiles.ppssppBin, rom, "--escape-exit"]
        commandArray = [recalboxFiles.ppssppBin, rom]
        return Command.Command(videomode=system.config['videomode'], array=commandArray, env={"XDG_CONFIG_HOME":recalboxFiles.CONF, "SDL_VIDEO_GL_DRIVER": "/usr/lib/libGLESv2.so"})
