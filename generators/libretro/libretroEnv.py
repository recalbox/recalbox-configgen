#!/usr/bin/env python
import sys
import os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../.." )))

import settings.emulationstationSettings as esSettings
import settings.recalboxSettings as recalSettings
import settings.libretroSettings as libretroSettings

# Read all needed variable from recalbox files and return a configration
def loadEnvConfig(system) :
    smooth = esSettings.load("Smooth", "false")
    shaders = esSettings.load("Shaders", "false")
    ratio = esSettings.load("GameRatio", "4/3")
    video_mode = recalSettings.load(system['name']+"_video_mode", system['video_mode'])
    custom_emulator = recalSettings.load(system['name']+"_emulator", system['core'])
    if shaders == "true" :
        smooth = false
    return { 'smooth' : smooth, 'shaders' : shaders, 'ratio' : ratio, 'video_mode' : video_mode,\
             'custom_emulator' : custom_emulator }




