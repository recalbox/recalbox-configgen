#!/usr/bin/env python

import os
import sys
import os.path
import unittest
import shutil

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import generators.fba2x.fba2xControllers as fba2xControllers
import generators.fba2x.fba2xConfig as fba2xConfig
import settings.unixSettings as unixSettings
import controllersConfig as controllersConfig

fba2xCustom = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/fba2x.cfg'))

# Injecting test recalbox.conf
controllersConfig.esInputs = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_input.cfg"))

# Test objects
basicInputs1 = {'a': controllersConfig.Input("a", "button", "10", "1"),'hotkey': controllersConfig.Input("hotkey", "button", "10", "1")}
basicController1 = controllersConfig.Controller("contr1", "joypad", "GUID1", "2", "Joypad1RealName", basicInputs1)
PS3UUID = "060000004c0500006802000000010000"
GPIOUUID = "15000000010000000100000000010000"
MICROSOFT = "030000005e0400008e02000014010000"


class TestFba2xController(unittest.TestCase):
    def setUp(self):
        # Cloning config files
        shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/es_input.cfg.origin")), \
                        os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_input.cfg")))
        shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/fba2x.cfg.origin')), \
                        fba2xCustom)
        # Injecting test file

        self.fbaSettings = unixSettings.UnixSettings(fba2xCustom)
        fba2xControllers.fbaSettings = self.fbaSettings


    def test_generate_simple_controller(self):
        config = fba2xControllers.generateControllerConfig('1', basicController1)
        self.assertEquals(config['Y_1'], '10')

    def test_generate_ps3_controller_buttons(self):
        controllers = controllersConfig.loadControllerConfig(0, PS3UUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = fba2xControllers.generateControllerConfig("1", controllers["1"])
        self.assertEquals(config['X_1'], '14')
        self.assertEquals(config['Y_1'], '13')
        self.assertEquals(config['A_1'], '15')
        self.assertEquals(config['B_1'], '12')
        self.assertEquals(config['L_1'], '10')
        self.assertEquals(config['R_1'], '11')

    def test_generate_ps3_controller_6buttons(self):
        controllers = controllersConfig.loadControllerConfig(0, PS3UUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                         "p3controller", -1, 0, "p4controller")
        config = fba2xControllers.generateControllerConfig("1", controllers["1"], True)
        self.assertEquals(config['X_1'], '12')
        self.assertEquals(config['Y_1'], '14')
        self.assertEquals(config['A_1'], '15')
        self.assertEquals(config['B_1'], '10')
        self.assertEquals(config['L_1'], '13')
        self.assertEquals(config['R_1'], '11')

    def test_generate_ps3_controller_directions(self):
        controllers = controllersConfig.loadControllerConfig(0, PS3UUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = fba2xControllers.generateControllerConfig("1", controllers["1"])

        self.assertEquals(config['UP_1'], '4')
        self.assertEquals(config['DOWN_1'], '6')
        self.assertEquals(config['LEFT_1'], '7')
        self.assertEquals(config['RIGHT_1'], '5')

    def test_generate_ps3_controller_specials(self):
        controllers = controllersConfig.loadControllerConfig(0, PS3UUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = fba2xControllers.generateControllerConfig("1", controllers["1"])
        self.assertEquals(config['HOTKEY'], '16')
        self.assertEquals(config['QUIT'], '3')

    def test_generate_ps3_controller_joystick(self):
        controllers = controllersConfig.loadControllerConfig(0, PS3UUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = fba2xControllers.generateControllerConfig("1", controllers["1"])
        self.assertEquals(config['JA_UD_1'], '1')
        self.assertEquals(config['JA_LR_1'], '0')

    def test_write_controller_config(self):
        controllers = controllersConfig.loadControllerConfig(2, PS3UUID, "p1controller", 1, PS3UUID, "p2controller", -1, PS3UUID,
                                                             "p3controller", -1, PS3UUID, "p4controller")
        fba2xControllers.writeControllersConfig("fba", "sf2.zip", controllers)

        self.assertEquals(self.fbaSettings.load('SDLID_1'), '2')
        self.assertEquals(self.fbaSettings.load('SDLID_2'), '1')
        self.assertEquals(self.fbaSettings.load('SDLID_3'), '-1')
        self.assertEquals(self.fbaSettings.load('SDLID_4'), '-1')

    def test_6btnGamesIsFalseFor4BtnGame(self):
        self.assertFalse(fba2xControllers.is6btn("/recalbox/share/anygame.zip"))


    def test_6btnGamesIsTrueFor6BtnGame(self):
        self.assertTrue(fba2xControllers.is6btn("/recalbox/share/sf2.zip"))

if __name__ == '__main__':
    unittest.main()
