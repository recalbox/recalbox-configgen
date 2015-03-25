#!/usr/bin/env python

import re
import os
import sys
import os.path
import unittest
import shutil
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import settings.recalboxSettings as recalSettings
import settings.emulationstationSettings as esSettings


shutil.copyfile("resources/es_settings.cfg.origin", "resources/es_settings.cfg")
shutil.copyfile("resources/recalbox.conf.origin", "resources/recalbox.conf")

#Injecting config files
recalboxSettings.settingsFile = os.path.abspath(os.path.join(os.path.dirname(__file__), "resources/recalbox.conf"))


class TestEnvConfig(unittest.TestCase): 
    def test_load_env(self):
        name = "I dont exists"
        loaded = libretroSettings.load(name)
        self.assertEquals(None, loaded)

    def test_load_disabled_value_return_none(self):
        name = "aspect_ratio_index"
        loaded = libretroSettings.load(name)
        self.assertEquals(None, loaded)

    def test_load_enabled_value_without_quotes(self):
        name = "config_save_on_exit"
        loaded = libretroSettings.load(name)
        self.assertEquals("false", loaded)

    def test_load_enabled_value_with_quotes(self):
        name = "video_threaded"
        loaded = libretroSettings.load(name)
        self.assertEquals("true", loaded)
	
    def test_write_value(self):
        name = "video_threaded"
        libretroSettings.save(name, "false")
        loaded = libretroSettings.load(name)
        self.assertEquals("false", loaded)

    def test_write_disabled_value(self):
        name = "video_aspect_ratio"
        loaded = libretroSettings.load(name)
        self.assertEquals(None, loaded)

        libretroSettings.save(name, "anewval")
        loaded = libretroSettings.load(name)
	self.assertEquals("anewval", loaded)

        libretroSettings.save(name, "1")
        loaded = libretroSettings.load(name)
        self.assertEquals("1", loaded)
    
    def test_disable_value(self):
        name = "aspect_ratio_index"
        libretroSettings.save(name, "1")
	loaded = libretroSettings.load(name)
        self.assertEquals("1", loaded)
	libretroSettings.disable(name)
	loaded = libretroSettings.load(name)
        self.assertEquals(None, loaded)


if __name__ == '__main__':
    unittest.main()
