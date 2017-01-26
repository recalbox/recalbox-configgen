#!/usr/bin/env python
import sys
import os
import recalboxFiles
import settings
from settings.unixSettings import UnixSettings

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

libretroSettings = UnixSettings(recalboxFiles.retroarchCustom, separator=' ')
coreSettings = UnixSettings(recalboxFiles.retroarchCoreCustom, separator=' ')


# return true if the option is considered enabled (for boolean options)
def enabled(key, dict):
    return key in dict and (dict[key] == '1' or dict[key] == 'true')


# return true if the option is considered defined
def defined(key, dict):
    return key in dict and isinstance(dict[key], str) and len(dict[key]) > 0


# Warning the values in the array must be exactly at the same index than
# https://github.com/libretro/RetroArch/blob/master/gfx/video_driver.c#L132
ratioIndexes = ["4/3", "16/9", "16/10", "16/15", "1/1", "2/1", "3/2", "3/4", "4/1", "4/4", "5/4", "6/5", "7/9", "8/3",
                "8/7", "19/12", "19/14", "30/17", "32/9", "config", "squarepixel"]


# Define the libretro device type corresponding to the libretro cores, when needed.
coreToP1Device = {'cap32': '513', '81': '257', 'fuse': '513'};
coreToP2Device = {'fuse': '513', 'snes9x_next': '257' };

# Define systems compatible with retroachievements
systemToRetroachievements = {'snes', 'nes', 'gba', 'gb', 'gbc', 'megadrive', 'pcengine'};

# Define systems not compatible with rewind option
systemNoRewind = {'virtualboy', 'sega32x', 'segacd', 'psx', 'fba_libretro', 'vectrex', 'zxspectrum', 'odyssey2', 'mame'};

# Define system emulated by bluemsx core
systemToBluemsx = {'msx': '"MSX2"', 'msx1': '"MSX2"', 'msx2': '"MSX2"', 'colecovision': '"COL - ColecoVision"' };

# Define the libretro device type corresponding to the libretro cores, when needed.
systemToP1Device = {'msx': '257', 'msx1': '257', 'msx2': '257', 'colecovision': '513' };
systemToP2Device = {'msx': '257', 'msx1': '257', 'msx2': '257', 'colecovision': '513' };

# Netplay modes
systemNetplayModes = {'host', 'client'}

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
            retroarchConfig['aspect_ratio_index'] = ratioIndexes.index(recalboxConfig['ratio'])
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
    retroarchConfig['cheevos_hardcore_mode_enable'] = 'false'

    if enabled('retroachievements', recalboxConfig):
        if(system.name in systemToRetroachievements):
            retroarchConfig['cheevos_enable'] = 'true'
            retroarchConfig['cheevos_username'] = recalboxConfig.get('retroachievements.username', "")
            retroarchConfig['cheevos_password'] = recalboxConfig.get('retroachievements.password', "")
            if enabled('retroachievements.hardcore', recalboxConfig):
                retroarchConfig['cheevos_hardcore_mode_enable'] = 'true'
            else:
                retroarchConfig['cheevos_hardcore_mode_enable'] = 'false'
    else:
        retroarchConfig['cheevos_enable'] = 'false'

    if enabled('integerscale', recalboxConfig):
        retroarchConfig['video_scale_integer'] = 'true'
    else:
        retroarchConfig['video_scale_integer'] = 'false'

    if(system.name in systemToBluemsx):
        if system.config['core'] == 'bluemsx':
            coreSettings.save('bluemsx_msxtype', systemToBluemsx[system.name])
            retroarchConfig['input_libretro_device_p1'] = systemToP1Device[system.name]
            retroarchConfig['input_libretro_device_p2'] = systemToP2Device[system.name]

    # Netplay management
    if 'netplaymode' in system.config and system.config['netplaymode'] in systemNetplayModes:
        # Security : hardcore mode disables save states, which would kill netplay
        retroarchConfig['cheevos_hardcore_mode_enable'] = 'false'
        # Quite strangely, host mode requires netplay_mode to be set to false when launched from command line
        retroarchConfig['netplay_mode']              = "false"
        retroarchConfig['netplay_ip_port']           = recalboxConfig.get('netplay.server.port', "")
        retroarchConfig['netplay_delay_frames']      = recalboxConfig.get('netplay.frames', "")
        retroarchConfig['netplay_nickname']          = recalboxConfig.get('netplay.nick', "")
        retroarchConfig['netplay_client_swap_input'] = "false"
        if system.config['netplaymode'] == 'client':
            # But client needs netplay_mode = true ... bug ?
            retroarchConfig['netplay_mode']              = "true"
            retroarchConfig['netplay_ip_address']        = recalboxConfig.get('netplay.server.ip', "")
            retroarchConfig['netplay_client_swap_input'] = "true"

    # Display FPS
    if enabled('showFPS', recalboxConfig):
        retroarchConfig['fps_show'] = 'true'
    else:
        retroarchConfig['fps_show'] = 'false'
        
    return retroarchConfig


def writeLibretroConfigToFile(config):
    for setting in config:
        libretroSettings.save(setting, config[setting])


def updateLibretroConfig(version):
    # Version is unsued so far, but who knows, one day
    try: 
        # Read files
        sourceSettings = UnixSettings(recalboxFiles.retroarchInitCustomOrigin, separator=' ')
        sourceConf = sourceSettings.loadFile()
        destSettings = UnixSettings(recalboxFiles.retroarchCustomOrigin, separator=' ')
        destConf = destSettings.loadFile()
        
        # Compare missing keys
        for key, value in sourceConf.iteritems():
            if key not in destConf: destConf[key] = value
        # Save
        for key, value in destConf.iteritems():
            destSettings.save(key, value)
            
        return True
    except:
        print "Libretro update failed !"
        return False