#!/usr/bin/env python
import os
import sys
import recalboxFiles
from settings.unixSettings import UnixSettings

# Set a specific video mode
def setVideoMode(videomode):
    os.system(createVideoModeLine(videomode))

def createVideoModeLine(videoMode):
    return "tvservice -e '{}'".format(videoMode)

# Set a specific video mode
def isSupported(index, mode="CEA", drive="HDMI"):
   # todo
    return True

# Switch to prefered mode
def setPreffered():
    recalSettings = UnixSettings(recalboxFiles.recalboxConf)
    esVideoMode = recalSettings.load('system.es.videomode')
    if esVideoMode is None:
        os.system("tvservice -p")
    else:
        os.system("tvservice -e '{}'".format(esVideoMode))
