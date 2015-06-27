#!/usr/bin/env python
import os

import videoMode


# Set a specific video mode
def runCommand(command):
    videoMode.setVideoMode(command.videomode)
    os.system(command.commandline)
    videoMode.setPreffered()
