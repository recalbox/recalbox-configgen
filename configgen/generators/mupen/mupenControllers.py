#!/usr/bin/env python
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from settings.unixSettings import UnixSettings
import recalboxFiles

mupenSettings = UnixSettings(recalboxFiles.mupenCustom, separator=' ')

# Write a configuration for a specified controller
def writeControllersConfig(controllers):
    writeHotKeyConfig(controllers)


def writeHotKeyConfig(controllers):
    if '1' in controllers:
        if 'hotkey' in controllers['1'].inputs:
            mupenSettings.save('Joy Mapping Stop', "\"J{}B{}\"".format(controllers['1'].index, controllers['1'].inputs['hotkey'].id))
