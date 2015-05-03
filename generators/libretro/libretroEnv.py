#!/usr/bin/env python
import sys
import os

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import settings.emulationstationSettings as esSettings
import settings.recalboxSettings as recalSettings

# Read all needed variable from recalbox files and return a configuration
# For retroarch configuration variable the priority is


#if a variable nammed [corename]_[option] exists in recalbox conf it will be used
#else if a variable named default_[option] exists in recalbox.conf it will be used
#else if the option exists in es_settings it will be used
#else if the core contains the default value that will be used

# So [corename]_[option] > default_[option] > es_settings > default value

libretro_options = ['video_smooth','video_shader','rewind_enable','aspect_ratio_index']
def loadLibretroEnv(system):
    smooth = esSettings.load("Smooth", "false")
    ratio = esSettings.load("GameRatio", "auto")
    # Not in loop because of default value
    video_mode = recalSettings.load(system.name + "_video_mode", recalSettings.load("default_video_mode", system.video_mode))
    custom_emulator = recalSettings.load(system.name + "_emulator", system.core)

    config = dict()
    # Getting default options
    for option in libretro_options:
        optioname = "default_" + option
        recal_option = recalSettings.load(optioname)
        if recal_option :
            config[option] = recal_option
    # Overwrite default option if core options present
    for option in libretro_options:
        optioname = system.name + "_" + option
        recal_option = recalSettings.load(optioname)
        if recal_option :
            config[option] = recal_option

    # If smooth has not been set, taking es setting value
    if 'video_smooth' not in config :
        config['video_smooth'] = smooth

    # Ratio : if not set getting es settings
    if 'aspect_ratio_index' not in config :
        if ratio == 'auto':
            config['video_aspect_ratio_auto'] = "true"
        elif ratio == '4/3':
            config['video_aspect_ratio_auto'] = "false"
            config['aspect_ratio_index'] = "0"
        elif ratio == '16/9':
            config['video_aspect_ratio_auto'] = "false"
            config['aspect_ratio_index'] = "1"
    else :
        config['video_aspect_ratio_auto'] = "false"


    # Shaders
    shaders = esSettings.load("Shaders", system.shaders)
    if shaders == "true" :
        if 'video_shader' in config :
            config['video_shader_enable'] = "true"
            config['video_smooth'] = "false"


    return {'video_mode': video_mode, \
            'core': custom_emulator,\
            'retroarch_conf' : config}




