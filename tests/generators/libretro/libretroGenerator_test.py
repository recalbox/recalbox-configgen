#!/usr/bin/env python

import os
import sys
import os.path
import unittest
import shutil
import controllersConfig
import time

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import generators.libretro.libretroConfig as libretroConfig
import generators.libretro.libretroGenerator as libretroGen


RETROARCH_ORIGIN_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/retroarchcustomorigin.cfg'))
RETROARCH_CUSTOM_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/retroarchcustom.cfg'))
RECALBOX_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/recalbox.conf'))

# Cloning config files
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/retroarchcustom.cfg.origin')), \
                RETROARCH_CUSTOM_CFG_FILE)
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/retroarchcustom.cfg.origin')), \
                RETROARCH_ORIGIN_CFG_FILE)


# Injecting test files
libretroGen.settingsFile = RETROARCH_CUSTOM_CFG_FILE
libretroGen.libretroSettings.settingsFile = RETROARCH_CUSTOM_CFG_FILE
libretroGen.libretroSettings.settingsFileOriginal = RETROARCH_ORIGIN_CFG_FILE

libretroConfig.libretroSettings.settingsFile = RETROARCH_CUSTOM_CFG_FILE

# test Systems
snes = libretroGen.LibretroCore(name='snes', videomode='4', core='pocketsnes', shaders='', ratio='auto', smooth='2',
                                rewind='false')
nes = libretroGen.LibretroCore(name='nes', videomode='6', core='catsfc', shaders='', ratio='16/9', smooth='1',
                               rewind='false', configfile='/myconfigfile.cfg')

# test inputs
basicInputs1 = {'hotkey': controllersConfig.Input("hotkey", "button", "10", "1")}
basicController1 = controllersConfig.Controller("contr1", "joypad", "GUID1", "0", "Joypad1RealName", basicInputs1)

class TestLibretroGenerator(unittest.TestCase):
    def test_generate_system_no_custom_settings(self):
        command = libretroGen.generate(snes, dict())
        self.assertEquals(command.videomode, '4')
        self.assertEquals(command.commandline, 'retroarch -L /usr/lib/libretro/pocketsnes.so --config '+RETROARCH_CUSTOM_CFG_FILE)

    def test_generate_system_custom_settings(self):
        command = libretroGen.generate(nes, dict())
        self.assertEquals(command.videomode, '6')
        self.assertEquals(command.commandline, 'retroarch -L /usr/lib/libretro/catsfc.so --config /myconfigfile.cfg')

    def test_copy_original_file(self):
        libretroGen.libretroSettings.settingsFile = RETROARCH_CUSTOM_CFG_FILE
        os.remove(RETROARCH_CUSTOM_CFG_FILE)
        time.sleep(1)
        command = libretroGen.generate(snes, dict())
        self.assertTrue(os.path.isfile(RETROARCH_CUSTOM_CFG_FILE))



if __name__ == '__main__':
    unittest.main()