#!/usr/bin/env python
import os
import sys
import recalboxFiles
import re
from settings.unixSettings import UnixSettings

# Set a specific video mode
def setVideoMode(videomode):
    os.system(createVideoModeLine(videomode))

def createVideoModeLine(videoMode):
    # pattern (CEA|DMT) [0-9]{1,2} HDMI
    if re.match("^(CEA|DMT) [0-9]{1,2}( HDMI)?$", videoMode):
        return "tvservice -e '{}'".format(videoMode)
    if re.match("^hdmi_cvt [\d\s]{10,20}$", videoMode):
        return "vcgencmd {} && tvservice -e 'DMT 87'".format(videoMode)
    if re.match("^hdmi_timings [\d\s]{48,58}$", videoMode):
        return "vcgencmd {} && tvservice -e 'DMT 87'".format(videoMode)

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
        setVideoMode(esVideoMode)
