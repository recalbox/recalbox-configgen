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
            if not os.path.isfile(recalboxFiles.retroarchCustom):
                shutil.copyfile(recalboxFiles.retroarchCustomOrigin, recalboxFiles.retroarchCustom)
            #  Write controllers configuration files
            libretroControllers.writeControllersConfig(system, playersControllers)
            # Write configuration to retroarchcustom.cfg
            libretroConfig.writeLibretroConfig(system)

        # Retroarch core on the filesystem
        retroarchCore = recalboxFiles.retroarchCores + system.config['core'] + recalboxFiles.libretroExt
        romName = os.path.basename(rom)

        # the command to run
        commandArray = [recalboxFiles.retroarchBin, "-L", retroarchCore, "--config", system.config['configfile']]
        
        # Custom configs - per core
        customCfg = "/recalbox/share/system/configs/retroarch/{}.cfg".format(system.name)
        if os.path.isfile(customCfg):
            commandArray.extend(["--append", customCfg])
        
        # Custom configs - per game
        customGameCfg = "/recalbox/share/system/configs/retroarch/{}/{}.cfg".format(system.name, romName)
        if os.path.isfile(customCfg):
            commandArray.extend(["--append", customGameCfg])
        
        # Overlay management
        overlayFile = "/recalbox/share/roms/{}/{}.cfg".format(system.name, romName)
        if os.path.isfile(overlayFile):
            commandArray.extend(["--append", overlayFile])
            
         # Netplay mode
        if 'netplaymode' in system.config:
            if system.config['netplaymode'] == 'host':
                commandArray.append("--host")
            elif system.config['netplaymode'] == 'client':
                commandArray.extend(["--connect", system.config['netplay.server.address']])
        
        commandArray.append(rom)
        return Command.Command(videomode=system.config['videomode'], array=commandArray)
