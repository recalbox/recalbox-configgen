#!/usr/bin/env python

import os
import sys
import os.path
import unittest
import shutil
import controllersConfig
import time
import settings.unixSettings as unixSettings

from Emulator import Emulator
from generators.libretro.libretroGenerator import LibretroGenerator

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import generators.libretro.libretroConfig as libretroConfig
import generators.libretro.libretroGenerator as libretroGenerator


RETROARCH_ORIGIN_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/retroarchcustomorigin.cfg'))
RETROARCH_CUSTOM_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/retroarchcustom.cfg'))
RECALBOX_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/recalbox.conf'))

# Cloning config files
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/retroarchcustom.cfg.origin')), \
                RETROARCH_CUSTOM_CFG_FILE)
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/retroarchcustom.cfg.origin')), \
                RETROARCH_ORIGIN_CFG_FILE)


# Injecting test files
libretroGenerator.recalboxFiles.retroarchCustom = RETROARCH_CUSTOM_CFG_FILE
libretroGenerator.recalboxFiles.retroarchCustomOrigin = RETROARCH_ORIGIN_CFG_FILE

libretroConfig.libretroSettings = unixSettings.UnixSettings(RETROARCH_CUSTOM_CFG_FILE, separator=' ')

# test Systems
snes = Emulator(name='snes', videomode='4', core='pocketsnes', shaders='', ratio='auto', smooth='2',
                                rewind='false', emulator='libretro')
nes = Emulator(name='nes', videomode='6', core='catsfc', shaders='', ratio='16/9', smooth='1',
                               rewind='false', configfile='/myconfigfile.cfg', emulator='libretro')

# test inputs
basicInputs1 = {'hotkey': controllersConfig.Input("hotkey", "button", "10", "1")}
basicController1 = controllersConfig.Controller("contr1", "joypad", "GUID1", "0", "Joypad1RealName", basicInputs1)

rom = "MyRom.nes"

libretroGen = LibretroGenerator()
class TestLibretroGenerator(unittest.TestCase):
    def test_generate_system_no_custom_settings(self):
        command = libretroGen.generate(snes, rom, dict())
        self.assertEquals(command.videomode, '4')
        self.assertEquals(command.commandline,
                          'retroarch -L \"/usr/lib/libretro/pocketsnes_libretro.so\" --config \"' + RETROARCH_CUSTOM_CFG_FILE + "\" \"MyRom.nes\"")

    def test_generate_system_custom_settings(self):
        command = libretroGen.generate(nes, rom, dict())
        self.assertEquals(command.videomode, '6')
        self.assertEquals(command.commandline, 'retroarch -L \"/usr/lib/libretro/catsfc_libretro.so\" --config \"/myconfigfile.cfg\" \"MyRom.nes\"')

    #def test_copy_original_file(self):
    #    os.remove(RETROARCH_CUSTOM_CFG_FILE)
    #    time.sleep(1)
    #   command = libretroGen.generate(snes, rom, dict())
    #    self.assertTrue(os.path.isfile(RETROARCH_CUSTOM_CFG_FILE))


if __name__ == '__main__':
    unittest.main()