#!/usr/bin/env python

import re
import os
import recalboxFiles
settingsFile = recalboxFiles.recalboxConf


def load(name, default=None):
    for line in open(settingsFile):
        if name in line:
            m = re.match(r"^" + name + "=(.+)", line)
            if m:
                return m.group(1)
    return default


def save(name, value):
    os.system("sed -i 's|^.*" + name + "=.*|" + name + "=" + value + "|g' " + settingsFile)
    if load(name) is None:
        with open(settingsFile, "a") as settings:
            settings.write("\n{}={}".format(name, value))


def disable(name):
    # settings=`cat "$es_settings" | sed -n "s/.*name=\"${varname}\" value=\"\(.*\)\".*/\1/p"`
    os.system("sed -i \"s|^.*\({}=.*\)|;\\1|g\" {}".format(name,settingsFile))


def loadAll(name):
    res = dict()
    for line in open(settingsFile):
        if name in line:
            m = re.match(r"^" + name + "\.(.+?)=(.+)", line)
            if m:
                res[m.group(1)] = m.group(2);
    return res