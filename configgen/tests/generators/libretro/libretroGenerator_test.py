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



rom = "MyRom.nes"

libretroGen = LibretroGenerator()


class TestLibretroGenerator(unittest.TestCase):
    def setUp(self):
        self.snes = Emulator(name='snes', videomode='4', core='pocketsnes', shaders='', ratio='auto', smooth='2',
                        rewind='false', emulator='libretro')
        self.nes = Emulator(name='nes', videomode='6', core='catsfc', shaders='', ratio='16/9', smooth='1',
                       rewind='false', configfile='/myconfigfile.cfg', emulator='libretro')

        # test inputs
        self.basicInputs1 = {'hotkey': controllersConfig.Input("hotkey", "button", "10", "1")}
        self.basicController1 = controllersConfig.Controller("contr1", "joypad", "GUID1", 1,0, "Joypad1RealName", self.basicInputs1)

        self.sdl2controler = controllersConfig.Controller("contr1", "joypad", "GUID1", 2,1, "Bluetooth Wireless Controller   ", self.basicInputs1)
        self.controllers = dict()
        self.controllers['1'] = self.basicController1

        self.sdl2controllers = dict()
        self.sdl2controllers['1'] = self.basicController1
        self.sdl2controllers['2'] = self.sdl2controler

    def test_generate_system_no_custom_settings(self):
        command = libretroGen.generate(self.snes, rom, dict())
        self.assertEquals(command.videomode, '4')
        self.assertEquals(command.commandline,
                          'retroarch -L \"/usr/lib/libretro/pocketsnes_libretro.so\" --config \"' + RETROARCH_CUSTOM_CFG_FILE + "\" \"MyRom.nes\"")

    def test_generate_system_custom_settings(self):
        command = libretroGen.generate(self.nes, rom, dict())
        self.assertEquals(command.videomode, '6')
        self.assertEquals(command.commandline,
                          'retroarch -L \"/usr/lib/libretro/catsfc_libretro.so\" --config \"/myconfigfile.cfg\" \"MyRom.nes\"')


    def test_generate_forced_input_config(self):
        command = libretroGen.generate(self.nes, rom, dict())
        self.assertEquals(command.videomode, '6')
        self.assertEquals(command.commandline,
                          'retroarch -L \"/usr/lib/libretro/catsfc_libretro.so\" --config \"/myconfigfile.cfg\" \"MyRom.nes\"')


    def test_custom_inputdriver_override_choice(self):
        self.snes.config['inputdriver'] = 'sdl2'
        command = libretroGen.generate(self.snes, rom, self.controllers)
        self.assertEquals(libretroConfig.libretroSettings.load('input_joypad_driver'), 'sdl2')

    def test_standard_inputdriver(self):
        command = libretroGen.generate(self.snes, rom, self.controllers)
        self.assertEquals(libretroConfig.libretroSettings.load('input_joypad_driver'), 'udev')


    def test_inputdriver_auto(self):
        command = libretroGen.generate(self.snes, rom, self.sdl2controllers)
        self.assertEquals(libretroConfig.libretroSettings.load('input_joypad_driver'), 'sdl2')
        # def test_copy_original_file(self):
        #    os.remove(RETROARCH_CUSTOM_CFG_FILE)
        #    time.sleep(1)
        #   command = libretroGen.generate(snes, rom, dict())
        #    self.assertTrue(os.path.isfile(RETROARCH_CUSTOM_CFG_FILE))


if __name__ == '__main__':
    unittest.main()