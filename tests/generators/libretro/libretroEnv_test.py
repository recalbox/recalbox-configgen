#!/usr/bin/env python

import re
import os
import sys
import os.path
import unittest
import shutil
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.." )))


import settings.emulationstationSettings as esSettings
import settings.recalboxSettings as recalSettings
import settings.libretroSettings as libretroSettings

import generators.libretro.libretroEnv as libretroEnv

# Cloning config files
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/retroarchcustom.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/retroarchcustom.cfg")))
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/recalbox.conf.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/recalbox.conf")))
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/es_settings.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_settings.cfg")))

# Injecting test files
libretroEnv.esSettings.settingsFile = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_settings.cfg"))
libretroEnv.recalSettings.settingsFile = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/recalbox.conf"))
libretroEnv.libretroSettings.settingsFile = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/retroarchcustom.cfg"))


class TestLibretroEnv(unittest.TestCase): 
    def test_load_default(self):	
	conf =  libretroEnv.loadEnvConfig({'name' : 'snes', 'video_mode': 4, 'core': "pocketsnes"})
	self.assertEquals(conf["shaders"], "false")

    def test_load_es_settings_value(self):
	conf =  libretroEnv.loadEnvConfig({'name' : 'snes', 'video_mode': 4, 'core': "pocketsnes"})
	self.assertEquals(conf["smooth"], "true")

    def test_load_recal_settings_value(self):
	conf =  libretroEnv.loadEnvConfig({'name' : 'snes', 'video_mode': 4, 'core': "pocketsnes"})
	self.assertEquals(conf["video_mode"], "10")


if __name__ == '__main__':
    unittest.main()
