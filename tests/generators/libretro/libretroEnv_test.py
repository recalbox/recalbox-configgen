#!/usr/bin/env python

import os
import sys
import os.path
import unittest
import shutil

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import generators.libretro.libretroEnv as libretroEnv
import generators.libretro.libretroGenerator as libretroGen

# Cloning config files
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/retroarchcustom.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/retroarchcustom.cfg")))
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/recalbox.conf.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/recalbox.conf")))
# Special file with env config
shutil.copyfile(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/recalbox.conf.origin.libretro")), \
    os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/recalbox.conf.libretro")))
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/es_settings.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_settings.cfg")))

# Injecting test files
libretroEnv.esSettings.settingsFile = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_settings.cfg"))
libretroEnv.recalSettings.settingsFile = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/recalbox.conf"))

# test Systems
psx = libretroGen.LibretroCore(name='psx', video_mode='4', corename='pcsx_rearmed', shaders='false')
snes = libretroGen.LibretroCore(name='psx', video_mode='5', corename='pcsx_rearmed', shaders='false')


class TestLibretroEnv(unittest.TestCase):
    def test_load_default(self):
        conf = libretroEnv.loadLibretroEnv(psx)
        self.assertEquals(conf["shaders"], "false")

    def test_load_es_settings_value(self):
        conf = libretroEnv.loadLibretroEnv(psx)
        self.assertEquals(conf["smooth"], "true")

    def test_video_mode_default(self):
        conf = libretroEnv.loadLibretroEnv(psx)
        self.assertEquals(conf["video_mode"], "5")


if __name__ == '__main__':
    unittest.main()