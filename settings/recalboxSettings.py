#!/usr/bin/env python

import re
import os

settingsFile = "/recalbox/share/system/recalbox.conf"

def load(name, default=None): 
    for line in open(settingsFile):
        if name in line:
            m = re.match(r"^"+name+"=(.+)", line)
	    if m :
	        return m.group(1)
    return default

def save(name,value):
    print "sed -i 's|^.?"+name+"=.*|"+name+"="+value+"|g' "+ settingsFile
    os.system("sed -i 's|^.*"+name+"=.*|"+name+"="+value+"|g' "+ settingsFile)

def disable(name):
    #        settings=`cat "$es_settings" | sed -n "s/.*name=\"${varname}\" value=\"\(.*\)\".*/\1/p"`
    os.system("sed -i \"s|^.*\("+name+"=.*\)|;\\1|g\" "+ settingsFile)

