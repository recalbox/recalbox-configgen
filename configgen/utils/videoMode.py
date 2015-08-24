#!/usr/bin/env python
import os

# Set a specific video mode
def setVideoMode(videomode):
    if videomode != 'default':
        os.system(createVideoModeLine(videomode))

def createVideoModeLine(videoMode):
    return "tvservice -e '{}'".format(videoMode)

# Set a specific video mode
def isSupported(index, mode="CEA", drive="HDMI"):
   # todo
    return True

# Switch to prefered mode
def setPreffered():
    os.system("tvservice -p")