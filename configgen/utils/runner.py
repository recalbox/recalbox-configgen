#!/usr/bin/env python
import os

import videoMode


# Set a specific video mode
def runCommand(command):
    if command.videoMode != 'default':
        videoMode.setVideoMode(command.videomode)

    os.system(command.commandline)

    if command.videoMode != 'default':
        videoMode.setPreffered()
