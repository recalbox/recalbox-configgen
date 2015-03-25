#!/usr/bin/env python
import os
import videoMode

# Set a specific video mode
def runCommand(command) :
    videoMode.setVideoMode(command.video_mode)
    os.open(command.commandLine)
    videoMode.setPreffered()
