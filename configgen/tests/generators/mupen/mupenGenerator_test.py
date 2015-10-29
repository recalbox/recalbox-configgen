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
from generators.mupen.mupenGenerator import MupenGenerator

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import generators.mupen.mupenControllers as mupenControllers

MUPEN_CUSTOM_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/mupen64plus.cfg'))
RECALBOX_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/recalbox.conf'))

# Cloning config files
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/mupen64plus.cfg')), \
                MUPEN_CUSTOM_CFG_FILE)


# Injecting test files
mupenControllers.recalboxFiles.mupenCustom = MUPEN_CUSTOM_CFG_FILE

mupenControllers.mupenSettings = unixSettings.UnixSettings(MUPEN_CUSTOM_CFG_FILE, separator=' ')

# test Systems
n64 = Emulator(name='n64', videomode='4', core='n64', shaders='', ratio='auto', smooth='2',
               rewind='false', emulator='mupen64plus')

# test inputs
basicInputs1 = {'hotkey': controllersConfig.Input("hotkey", "button", "10", "1")}
basicController1 = controllersConfig.Controller("contr1", "joypad", "GUID1", '1', "0", "Joypad1RealName", basicInputs1)
basicControllers = dict()
basicControllers['1'] = basicController1
mupenGen = MupenGenerator()


class TestMupenControllers(unittest.TestCase):
    def test_write_hotkey(self):
        mupenControllers.writeControllersConfig(basicControllers)
        self.assertEquals(mupenControllers.mupenSettings.load("Joy Mapping Stop"), 'J0B10')

    def test_commandline_core_n64(self):
        command = mupenGen.generate(n64, "rom.n64", basicControllers)
        self.assertEquals(command.array,
                          ['mupen64plus', '--corelib', '/usr/lib/libmupen64plus.so.2.0.0', '--gfx',
                           '/usr/lib/mupen64plus/mupen64plus-video-n64.so', '--configdir', '/recalbox/configs/mupen64/',
                           '--datadir', '/recalbox/configs/mupen64/', "rom.n64"])


if __name__ == '__main__':
    unittest.main()
