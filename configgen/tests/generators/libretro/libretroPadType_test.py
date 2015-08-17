#!/usr/bin/env python

import os
import sys
import os.path
import unittest
import shutil

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import generators.libretro.libretroControllers as libretroControllers
import controllersConfig as controllersConfig
from Emulator import Emulator
# Cloning config files
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/retroarchcustom.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/retroarchcustom.cfg")))

# Injecting test retroarchroot
libretroControllers.settingsRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp"))

onlyBtnsInputs = {'up': controllersConfig.Input("up", "button", "1", "1")}
onlyHatsInputs = {'up': controllersConfig.Input("up", "hat", "1", "1")}
onlyAxisInputs = {'up': controllersConfig.Input("up", "axis", "1", "1")}

axisAndBtnsInputs = {'up': controllersConfig.Input("up", "button", "1", "1"),
                     'joystickup': controllersConfig.Input("up", "axis", "1", "1")}
snes = Emulator('snes', 'snes', 'libretro')
psx = Emulator('psx', 'psx', 'libretro')

# Test the padtype settings
class TestLibretroAnalogMode(unittest.TestCase):
    def test_padtype_only_btn(self):
        basicControllerBTN = controllersConfig.Controller("contr1", "joypad", "GUID1", '1', "0", "Joypad1RealName",
                                                          onlyBtnsInputs)
        padtype = libretroControllers.getAnalogMode(basicControllerBTN, snes)
        self.assertEqual("1", padtype)

    def test_padtype_only_joystick(self):
        basicController = controllersConfig.Controller("contr1", "joypad", "GUID1", '1', "0", "Joypad1RealName",
                                                       onlyAxisInputs)
        padtype = libretroControllers.getAnalogMode(basicController, snes)
        self.assertEqual("0", padtype)

    def test_padtype_only_hats(self):
        basicController = controllersConfig.Controller("contr1", "joypad", "GUID1", '1', "0", "Joypad1RealName",
                                                       onlyHatsInputs)
        padtype = libretroControllers.getAnalogMode(basicController, snes)
        self.assertEqual("1", padtype)

    def test_padtype_dual(self):
        basicController = controllersConfig.Controller("contr1", "joypad", "GUID1", '1', "0", "Joypad1RealName",
                                                       axisAndBtnsInputs)
        padtype = libretroControllers.getAnalogMode(basicController, snes)
        self.assertEqual("1", padtype)


    def test_padtype_dual(self):
        basicController = controllersConfig.Controller("contr1", "joypad", "GUID1", '1', "0", "Joypad1RealName",
                                                       axisAndBtnsInputs)
        padtype = libretroControllers.getAnalogMode(basicController, snes)
        self.assertEqual("1", padtype)

    def test_padtype_psx(self):
        basicController = controllersConfig.Controller("contr1", "joypad", "GUID1", '1', "0", "Joypad1RealName",
                                                       axisAndBtnsInputs)
        padtype = libretroControllers.getAnalogMode(basicController, psx)
        # self.assertEqual("0", padtype)