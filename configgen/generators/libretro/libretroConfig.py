#!/usr/bin/env python
import sys
import os
import recalboxFiles
import settings
from settings.unixSettings import UnixSettings

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

libretroSettings = UnixSettings(recalboxFiles.retroarchCustom, separator=' ')


# return true if the option is considered enabled (for boolean options)
def enabled(key, dict):
    return key in dict and (dict[key] == '1' or dict[key] == 'true')


# return true if the option is considered defined
def defined(key, dict):
    return key in dict and isinstance(dict[key], str) and len(dict[key]) > 0


ratioIndexes = {'16/9': '1', '4/3': '0', '16/10': '2'}

# Define the libretro device type corresponding to the libretro cores, when needed.
coreToP1Device = {'cap32': '513', '81': '257', 'fuse': '513'};
coreToP2Device = {'fuse': '513', 'snes9x_next': '257' };

# Define systems compatible with retroachievements
systemToRetroachievements = {'snes', 'nes', 'gba', 'gb', 'gbc', 'megadrive', 'pcengine'};

# Define systems not compatible with rewind option
systemNoRewind = {'virtualboy', 'sega32x', 'segacd', 'psx', 'fba_libretro', 'vectrex', 'zxspectrum', 'odyssey2', 'mame'};


def writeLibretroConfig(system):
    writeLibretroConfigToFile(createLibretroConfig(system))


# take a system, and returns a dict of retroarch.cfg compatible parameters
def createLibretroConfig(system):
    retroarchConfig = dict()
    recalboxConfig = system.config
    if enabled('smooth', recalboxConfig):
        retroarchConfig['video_smooth'] = 'true'
    else:
        retroarchConfig['video_smooth'] = 'false'

    if defined('shaders', recalboxConfig):
        retroarchConfig['video_shader'] = recalboxConfig['shaders']
        retroarchConfig['video_shader_enable'] = 'true'
        retroarchConfig['video_smooth'] = 'false'
    else:
        retroarchConfig['video_shader_enable'] = 'false'

    if defined('ratio', recalboxConfig):
        if recalboxConfig['ratio'] in ratioIndexes:
            retroarchConfig['aspect_ratio_index'] = ratioIndexes[recalboxConfig['ratio']]
            retroarchConfig['video_aspect_ratio_auto'] = 'false'
        elif recalboxConfig['ratio'] == "custom":
            retroarchConfig['video_aspect_ratio_auto'] = 'false'
        else:
            retroarchConfig['video_aspect_ratio_auto'] = 'true'
            retroarchConfig['aspect_ratio_index'] = ''

    retroarchConfig['rewind_enable'] = 'false'

    if enabled('rewind', recalboxConfig):
        if(not system.name in systemNoRewind):
            retroarchConfig['rewind_enable'] = 'true'
    else:
        retroarchConfig['rewind_enable'] = 'false'

    if enabled('autosave', recalboxConfig):
        retroarchConfig['savestate_auto_save'] = 'true'
        retroarchConfig['savestate_auto_load'] = 'true'
    else:
        retroarchConfig['savestate_auto_save'] = 'false'
        retroarchConfig['savestate_auto_load'] = 'false'

    if defined('inputdriver', recalboxConfig):
        retroarchConfig['input_joypad_driver'] = recalboxConfig['inputdriver']
    else:
        retroarchConfig['input_joypad_driver'] = 'udev'

    retroarchConfig['savestate_directory'] = recalboxFiles.savesDir + system.name
    retroarchConfig['savefile_directory'] = recalboxFiles.savesDir + system.name

    retroarchConfig['input_libretro_device_p1'] = '1'
    retroarchConfig['input_libretro_device_p2'] = '1'

    if(system.config['core'] in coreToP1Device):
        retroarchConfig['input_libretro_device_p1'] = coreToP1Device[system.config['core']]

    if(system.config['core'] in coreToP2Device):
        retroarchConfig['input_libretro_device_p2'] = coreToP2Device[system.config['core']]

    retroarchConfig['cheevos_enable'] = 'false'

    if enabled('retroachievements', recalboxConfig):
        if(system.name in systemToRetroachievements):
            retroarchConfig['cheevos_enable'] = 'true'
            retroarchConfig['cheevos_username'] = recalboxConfig.get('retroachievements.username', "")
            retroarchConfig['cheevos_password'] = recalboxConfig.get('retroachievements.password', "")
    else:
        retroarchConfig['cheevos_enable'] = 'false'

    if enabled('integerscale', recalboxConfig):
        retroarchConfig['video_scale_integer'] = 'true'
    else:
        retroarchConfig['video_scale_integer'] = 'false'
    return retroarchConfig


def writeLibretroConfigToFile(config):
    for setting in config:
        libretroSettings.save(setting, config[setting])
