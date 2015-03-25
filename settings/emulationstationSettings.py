#!/usr/bin/env python

import re
import os

settingsFile = "/root/.emulationstation/es_settings.cfg"

def load(name, default=None): 
    for line in open(settingsFile):
        if name in line:
            m = re.match(r".*value=\"(.+?)\".*", line)
	    if m :
	        return m.group(1)
    return default			

def save(name,value):
    os.system("sed -i 's|name=\""+name+"\" value=\".*\"|name=\""+name+"\" value=\""+value+"\"|g' "+settingsFile)
