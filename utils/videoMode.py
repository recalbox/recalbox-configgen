#!/usr/bin/env python
import os

# Set a specific video mode
def setVideoMode(index, mode="CEA", drive="HDMI") :
	os.open("tvservice -e '%s %s %s'" % (mode, index, drive))

# Switch to prefered mode
def setPreffered():
	os.open("tvservice -p")

