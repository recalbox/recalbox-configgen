#!/usr/bin/env python

import re
import os

settingsFile = "/recalbox/configs/retroarch/retroarchcustom.cfg"

def load(name, default=None): 
    for line in open(settingsFile):
        if name in line:
            m = re.match(r"^"+name+" ?= ?\"(.+)\"", line)
	    if m :
	        return m.group(1)
            else :
                m = re.match(r"^"+name+" ?= ?(.+)", line)
	        if m :
	            return m.group(1)
    return default

def save(name,value):
    os.system("sed -i \"s|#\?"+name+" \?=.*|"+name+" = "+value+"|g\" "+ settingsFile)

def disable(name):
    os.system("sed -i \"s|^.*\("+name+" =.*\)|#\\1|g\" "+ settingsFile)
