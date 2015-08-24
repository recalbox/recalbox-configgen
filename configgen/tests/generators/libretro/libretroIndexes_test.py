#!/usr/bin/env python

import os
import sys
import os.path
import unittest
import shutil

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import generators.libretro.libretroControllers as libretroControllers
import settings.unixSettings as unixSettings
import controllersConfig as controllersConfig
from Emulator import Emulator

shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/retroarchcustom.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/retroarchcustom.cfg")))
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/es_input.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_input.cfg")))

# Injecting test recalbox.conf
libretroControllers.settingsRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp"))
# Injecting test es_input
controllersConfig.esInputs = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_input.cfg"))

# Injecting test retroarch.conf
libretroSettingsFile = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/retroarchcustom.cfg"))
libretroSettings = unixSettings.UnixSettings(libretroSettingsFile, ' ')
libretroControllers.libretroSettings = libretroSettings

# Test objects
basicInputs1 = {'a': controllersConfig.Input("a", "button", "10", "1")}
basicController1 = controllersConfig.Controller("contr1", "joypad", "GUID1", '1', 0, "Joypad1RealName", basicInputs1)
basicController2 = controllersConfig.Controller("contr2", "joypad", "GUID2", '2', 1, "Joypad2RealName", basicInputs1)
basicController3 = controllersConfig.Controller("contr3", "joypad", "GUID3", '3', 2, "Joypad3RealName", basicInputs1)
basicController4 = controllersConfig.Controller("contr4", "joypad", "GUID4", '4', 3, "Joypad4RealName", basicInputs1)
controllers4 = {"1": basicController1, "2": basicController2, "3": basicController3, "4": basicController4}
controllers2 = {"1": basicController1, "2": basicController2}
controllers2weird = {"3": basicController4, "2": basicController3}
controllers4reversed = {"1": basicController4, "2": basicController3, "3": basicController2, "4": basicController1}


snes = Emulator(name='snes', videomode='4', core='pocketsnes', shaders='', ratio='auto', smooth='2',
                rewind='false', emulator='libretro')
class TestLibretro4ControllerIndex(unittest.TestCase):
    def test_4_controller(self):
        val = libretroControllers.writeControllersConfig(snes,controllers4)
        self.assertEquals(libretroSettings.load("input_player1_joypad_index"), "0")
        self.assertEquals(libretroSettings.load("input_player2_joypad_index"), "1")
        self.assertEquals(libretroSettings.load("input_player3_joypad_index"), "2")
        self.assertEquals(libretroSettings.load("input_player4_joypad_index"), "3")

    def test_reversed_controller(self):
        val = libretroControllers.writeControllersConfig(snes,controllers4reversed)
        self.assertEquals(libretroSettings.load("input_player1_joypad_index"), "3")
        self.assertEquals(libretroSettings.load("input_player2_joypad_index"), "2")
        self.assertEquals(libretroSettings.load("input_player3_joypad_index"), "1")
        self.assertEquals(libretroSettings.load("input_player4_joypad_index"), "0")

    def test_2_last_controllers(self):
        val = libretroControllers.writeControllersConfig(snes,controllers2weird)
        self.assertEquals(libretroSettings.load("input_player2_joypad_index"), "2")
        self.assertEquals(libretroSettings.load("input_player3_joypad_index"), "3")



if __name__ == '__main__':
    unittest.main()
