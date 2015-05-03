#!/usr/bin/env python

settingsRoot = "/recalbox/configs/retroarch"
settingsFileOrigin = settingsRoot + "/retroarchcustom.cfg.origin"
settingsFile = settingsRoot + "/retroarchcustom.cfg"

shadersRoot = "/recalbox/share/shaders/presets/"
shadersExt = ".gplsp"


class LibretroCore():
    def __init__(self, name, video_mode, core, shaders):
        self.name = name
        self.video_mode = video_mode
        self.core = core
        self.shaders = shaders



# Main entry of the module
# Configure retroarch and return a command
def generate(system, playersControllers):
    # Write controllers configuration files
    # write options in retroarchcustom from env
    # set videomode
    # launch the emulator
    # video mode default
    print 'ok'
    # return (video_mode, launch command)
