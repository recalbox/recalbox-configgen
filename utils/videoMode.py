#!/usr/bin/env python
import os

# Set a specific video mode
def setVideoMode(index, mode="CEA", drive="HDMI"):
    os.system("tvservice -e '%s %s %s'" % (mode, index, drive))

# Set a specific video mode
def isSupported(index, mode="CEA", drive="HDMI"):
   # todo
    return False

# Switch to prefered mode
def setPreffered():
    os.system("tvservice -p")

