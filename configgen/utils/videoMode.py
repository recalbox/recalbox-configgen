#!/usr/bin/env python
import os

# Set a specific video mode
def setVideoMode(videomode):
    os.system(createVideoModeLine(videomode))

def createVideoModeLine(videoMode):
    if not ("CEA" in videoMode or "DMT" in videoMode):
        videoMode += " CEA"
    if not ("HDMI" in videoMode or "DVI" in videoMode):
        videoMode += " HDMI"
    return "tvservice -e " + videoMode

# Set a specific video mode
def isSupported(index, mode="CEA", drive="HDMI"):
   # todo
    return False

# Switch to prefered mode
def setPreffered():
    os.system("tvservice -p")

