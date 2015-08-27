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
from controllersConfig import Controller
from Emulator import Emulator
from settings.unixSettings import UnixSettings


RETROARCH_CONFIG = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/retroarchcustom.cfg"))
RETROARCH_CORE_CONFIG = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/retroarchcorecustom.cfg"))

shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/retroarchcustom.cfg.origin")), \
                RETROARCH_CONFIG)

shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/retroarchcores.cfg")), \
                RETROARCH_CORE_CONFIG)

shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/es_input.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_input.cfg")))

# Injecting test recalbox.conf
libretroControllers.settingsRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp"))
# Injecting test es_input
controllersConfig.esInputs = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_input.cfg"))
# Injecting retroarch configuration
libretroControllers.coreSettings = UnixSettings(RETROARCH_CORE_CONFIG, separator=' ')

# Test objects
basicInputs1 = {'a': controllersConfig.Input("a", "button", "10", "1"),
                'hotkey': controllersConfig.Input("hotkey", "button", "10", "1")}
basicController1 = Controller("contr1", "joypad", "GUID1", '1',  "0", "Joypad1RealName", basicInputs1)
PS3UUID = "060000004c0500006802000000010000"
GPIOUUID = "15000000010000000100000000010000"
snes = Emulator('snes', 'snes', 'libretro')


class TestLibretroController(unittest.TestCase):
    def test_generate_simple_controller(self):
        config = libretroControllers.generateControllerConfig(basicController1)
        self.assertEquals(config['input_player1_a_btn'], '10')

    def test_generate_ps3_controller_buttons(self):
        controllers = controllersConfig.loadControllerConfig(0, PS3UUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = libretroControllers.generateControllerConfig(controllers["1"])
        self.assertEquals(config['input_player1_select_btn'], '0')
        self.assertEquals(config['input_player1_a_btn'], '13')
        self.assertEquals(config['input_player1_start_btn'], '3')
        self.assertEquals(config['input_player1_b_btn'], '14')
        self.assertEquals(config['input_player1_l2_btn'], '8')
        self.assertEquals(config['input_player1_r_btn'], '11')
        self.assertEquals(config['input_player1_y_btn'], '15')
        self.assertEquals(config['input_player1_x_btn'], '12')
        self.assertEquals(config['input_player1_l_btn'], '10')

    def test_generate_ps3_controller_joysticks(self):
        controllers = controllersConfig.loadControllerConfig(0, PS3UUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = libretroControllers.generateControllerConfig(controllers["1"])
        self.assertEquals(config['input_player1_l_y_plus_axis'], '+1')
        self.assertEquals(config['input_player1_l_y_minus_axis'], '-1')
        self.assertEquals(config['input_player1_l_x_plus_axis'], '+0')
        self.assertEquals(config['input_player1_l_x_minus_axis'], '-0')


    def test_generate_joystick_as_directions(self):
        controllers = controllersConfig.loadControllerConfig(0, GPIOUUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = libretroControllers.generateControllerConfig(controllers["1"])
        self.assertEquals(config['input_player1_up_axis'], '-1')
        self.assertEquals(config['input_player1_down_axis'], '+1')
        self.assertEquals(config['input_player1_right_axis'], '+0')
        self.assertEquals(config['input_player1_left_axis'], '-0')

    def test_generate_specials(self):
        controllers = controllersConfig.loadControllerConfig(0, GPIOUUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = libretroControllers.generateControllerConfig(controllers["1"])
        print config
        self.assertEquals(config['input_exit_emulator_btn'], '7')


    def test_write_ps3_controller_joysticks(self):
        controllers = controllersConfig.loadControllerConfig(0, PS3UUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = libretroControllers.writeControllerConfig(controllers["1"], "1", snes)
        with open(RETROARCH_CONFIG) as controllerFile:
            lines = []
            for line in controllerFile:
                lines.append(line)
            self.assertTrue('input_player1_l2_btn = 8\n' in lines)
        self.assertTrue(libretroControllers.libretroSettings.load("input_player1_analog_dpad_mode"), "1")

    def test_write_only_joystick_controller(self):
        controllers = controllersConfig.loadControllerConfig(0, GPIOUUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = libretroControllers.writeControllerConfig(controllers["1"], "1", snes)
        self.assertTrue(libretroControllers.libretroSettings.load("input_player1_analog_dpad_mode"), "0")

    def test_write_hotkey(self):
        command = libretroControllers.writeHotKeyConfig({'1': basicController1})
        self.assertEqual(libretroControllers.libretroSettings.load('input_enable_hotkey_btn'), '10')

    def test_generate_ps3_controller_joysticks_right(self):
        controllers = controllersConfig.loadControllerConfig(0, PS3UUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = libretroControllers.generateControllerConfig(controllers["1"])
        self.assertEquals(config['input_player1_r_y_plus_axis'], '+3')
        self.assertEquals(config['input_player1_r_y_minus_axis'], '-3')
        self.assertEquals(config['input_player1_r_x_plus_axis'], '+2')
        self.assertEquals(config['input_player1_r_x_minus_axis'], '-2')


class TestLibretroGeneratorGetValue(unittest.TestCase):
    def test_on_button(self):
        val = libretroControllers.getConfigValue(controllersConfig.Input("a", "button", "10", "1"))
        self.assertEquals("10", val)

    def test_on_axis(self):
        val = libretroControllers.getConfigValue(controllersConfig.Input("down", "axis", "10", "1"))
        self.assertEquals("+10", val)
        val = libretroControllers.getConfigValue(controllersConfig.Input("down", "axis", "10", "-1"))
        self.assertEquals("-10", val)

    def test_on_hat(self):
        val = libretroControllers.getConfigValue(controllersConfig.Input("down", "hat", "2", "1"))
        self.assertEquals("h2up", val)
        val = libretroControllers.getConfigValue(controllersConfig.Input("down", "hat", "3", "8"))
        self.assertEquals("h3left", val)

    def test_on_key(self):
        val = libretroControllers.getConfigValue(controllersConfig.Input("down", "key", "2", "1"))
        self.assertEquals("2", val)
        val = libretroControllers.getConfigValue(controllersConfig.Input("down", "key", "3", "8"))
        self.assertEquals("3", val)


class TestLibretroDualAnalogPSone(unittest.TestCase):
    def test_enable_analog_mode_psx(self):
        val = libretroControllers.getAnalogCoreMode(basicController1)
        self.assertEquals("standard", val)

    def test_enable_analog_mode_psx(self):
        controllers = controllersConfig.loadControllerConfig(0, PS3UUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        val = libretroControllers.getAnalogCoreMode(controllers['1'])
        self.assertEquals("analog", val)

class TestLibretroGeneratorInputDriverTest(unittest.TestCase):
    def test_udev_by_default(self):
        controllers = dict()
        controllers['1'] =  Controller("contr1", "joypad", "GUID1", '1',  "0", "Joypad1RealName", dict())
        driver = libretroControllers.getInputDriver(controllers)
        self.assertEquals("udev", driver)

class TestLibretroGeneratorInputDriverTest(unittest.TestCase):
    def test_udev_by_default(self):
        controllers = dict()
        controllers['1'] =  Controller("contr1", "joypad", "GUID1", '1',  "0", "Joypad1RealName", dict())
        driver = libretroControllers.getInputDriver(controllers)
        self.assertEquals("udev", driver)


    def test_sdl2_for_nes30pro(self):
        controllers = dict()
        controllers['1'] =  Controller("contr1", "joypad", "GUID1", '1',  "0", "Bluetooth Wireless Controller   ", dict())
        driver = libretroControllers.getInputDriver(controllers)
        self.assertEquals("sdl2", driver)


    def test_sdl2_for_fc30pro(self):
        controllers = dict()
        controllers['1'] =  Controller("contr1", "joypad", "GUID1", '1',  "0", "szmy-power Ltd.  Joypad  ", dict())
        driver = libretroControllers.getInputDriver(controllers)
        self.assertEquals("sdl2", driver)

    def test_sdl2_for_fc30pro(self):
        controllers = dict()
        controllers['1'] = Controller("contr1", "joypad", "GUID1", '1',  "0", "szmy-power Ltd.  Joypad  ", dict())
        driver = libretroControllers.getInputDriver(controllers)
        self.assertEquals("sdl2", driver)

if __name__ == '__main__':
    unittest.main()
