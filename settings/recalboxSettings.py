#!/usr/bin/env python

import re
import os

settingsFile = "/recalbox/share/system/recalbox.conf"


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
    os.system("sed -i \"s|^.*\(" + name + "=.*\)|;\\1|g\" " + settingsFile)


def loadAll(name):
    res = dict()
    for line in open(settingsFile):
        if name in line:
            m = re.match(r"^" + name + "\.(.+?)=(.+)", line)
            if m:
                res[m.group(1)] = m.group(2);
    return res