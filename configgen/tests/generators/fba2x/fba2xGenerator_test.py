#!/usr/bin/env python

import sys
import os.path
import unittest
import shutil
import configgen.controllersConfig as controllersConfig
import configgen.settings.unixSettings as unixSettings

from configgen.Emulator import Emulator
from configgen.generators.fba2x.fba2xGenerator import Fba2xGenerator

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import configgen.generators.fba2x.fba2xConfig as fba2xConfig
import configgen.generators.fba2x.fba2xGenerator as fba2xGenerator


FBA2X_ORIGIN_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/fba2x.cfg.origin'))
FBA2X_CUSTOM_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/fba2x.cfg'))
RECALBOX_CFG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/recalbox.conf'))

# Cloning config files
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/fba2x.cfg.origin')), \
                FBA2X_ORIGIN_CFG_FILE)


# Injecting test files
fba2xGenerator.recalboxFiles.fbaCustom = FBA2X_CUSTOM_CFG_FILE
fba2xGenerator.recalboxFiles.fbaCustomOrigin = FBA2X_ORIGIN_CFG_FILE

fba2xConfig.fbaSettings = unixSettings.UnixSettings(FBA2X_CUSTOM_CFG_FILE)

# test Systems
fbaSystem = Emulator(name='fba', videomode='4', shaders='', ratio='auto', smooth='2',
                                emulator='pifba')

fbaSystemCustom = Emulator(name='fba', videomode='6', shaders='', ratio='auto', smooth='2',
               emulator='pifba', configfile='lol')
# test inputs
basicInputs1 = {'hotkey': controllersConfig.Input("hotkey", "button", "10", "1")}
basicController1 = controllersConfig.Controller("contr1", "joypad", "GUID1", "0", "Joypad1RealName", basicInputs1)

rom = "MyRom.zip"

fba2xGen = Fba2xGenerator()
fba2xGenerator.fba2xConfig.fbaSettings = fba2xConfig.fbaSettings

class TestLibretroGenerator(unittest.TestCase):
    def test_generate_system_no_custom_settings(self):
        command = fba2xGen.generate(fbaSystem, rom, dict())
        self.assertEquals(command.videomode, '4')
        self.assertEquals(command.array,['/usr/bin/fba2x', '--configfile', FBA2X_CUSTOM_CFG_FILE, 'MyRom.zip'])

    def test_generate_system_custom_settings(self):
        command = fba2xGen.generate(fbaSystemCustom, rom, dict())
        self.assertEquals(command.videomode, '6')
        self.assertEquals(command.array, ['/usr/bin/fba2x', '--configfile', 'lol', 'MyRom.zip'])


if __name__ == '__main__':
    unittest.main()