#!/usr/bin/env python
import Command
import mupenControllers
import recalboxFiles
from generators.Generator import Generator


class MupenGenerator(Generator):
    # Main entry of the module
    # Configure mupen and return a command
    def generate(self, system, rom, playersControllers):
        # Settings recalbox default config file if no user defined one
        if not system.config['configfile']:
            # Using recalbox config file
            system.config['configfile'] = recalboxFiles.mupenCustom
            #  Write controllers configuration files
            mupenControllers.writeControllersConfig(playersControllers)

        commandArray = ["mupen64plus", "--corelib", "/usr/lib/libmupen64plus.so.2.0.0", "--gfx", "/usr/lib/mupen64plus/mupen64plus-video-{}.so".format(system.config['core']),
                        "--configdir", "/recalbox/share/system/configs/mupen64/", "--datadir", "/recalbox/share/system/configs/mupen64/", rom]
        return Command.Command(videomode=system.config['videomode'], array=commandArray, env={"SDL_VIDEO_GL_DRIVER":"/usr/lib/libGLESv2.so"})
