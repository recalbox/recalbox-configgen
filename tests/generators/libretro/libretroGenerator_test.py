#!/usr/bin/env python

import os
import sys
import os.path
import unittest
import shutil


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import generators.libretro.libretroConfig as libretroConfig
import generators.libretro.libretroGenerator as libretroGen

import settings.libretroSettings as libretroSettings

RETROARCH_ORIGIN_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/retroarchcustomorigin.cfg'))
RETROARCH_CUSTOM_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/retroarchcustom.cfg'))
RECALBOX_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/recalbox.conf'))

# Cloning config files
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/retroarchcustom.cfg.origin')), \
                RETROARCH_CUSTOM_CFG_FILE)
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/retroarchcustom.cfg.origin')), \
                RETROARCH_ORIGIN_CFG_FILE)


# Injecting test files
libretroGen.settingsFileOrigin = RETROARCH_ORIGIN_CFG_FILE
libretroGen.settingsFile = RETROARCH_CUSTOM_CFG_FILE

libretroSettings.settingsFile  = RETROARCH_CUSTOM_CFG_FILE
libretroConfig.libretroSettings.settingsFile = RETROARCH_CUSTOM_CFG_FILE

# test Systems
snes = libretroGen.LibretroCore(name='snes', videomode='4', core='pocketsnes', shaders='', ratio='auto', smooth='2',
                                rewind='false')
nes = libretroGen.LibretroCore(name='nes', videomode='4', core='pocketsnes', shaders='', ratio='16/9', smooth='1',
                               rewind='false')
nes43 = libretroGen.LibretroCore(name='nes', videomode='4', core='pocketsnes', shaders='myshaders.gpslp', ratio='4/3',
                                 smooth='1', rewind='false')
nesauto = libretroGen.LibretroCore(name='nes', videomode='4', core='pocketsnes', shaders='myshaders.gpslp',
                                   ratio='auto', smooth='1', rewind='true')

class TestLibretroGenerator(unittest.TestCase):
    def test_generate_system_no_custom_settings(self):
        command = libretroGen.generate(snes, dict())

        self.assertEquals(command.videomode, '4')
        self.assertEquals(command.commandline, 'retroarch -L /usr/lib/libretro/pocketsnes.so --config /home/matthieu/dev/recalbox-configgen/tests/generators/libretro/tmp/retroarchcustom.cfg')

    def test_generate_system_no_custom_settings(self):
        command = libretroGen.generate(snes, dict())
    
        self.assertEquals(command.videomode, '4')
        self.assertEquals(command.commandline, 'retroarch -L /usr/lib/libretro/pocketsnes.so --config /home/matthieu/dev/recalbox-configgen/tests/generators/libretro/tmp/retroarchcustom.cfg')


if __name__ == '__main__':
    unittest.main()