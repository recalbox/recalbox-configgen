#!/usr/bin/env python

import os
import sys
import os.path
import unittest
import shutil

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import settings.recalboxSettings as recalSettings

shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/recalbox.conf.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/recalbox.conf")))


# Injecting test recalbox.conf
recalSettings.settingsFile = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/recalbox.conf"))


class TestRecalboxSettings(unittest.TestCase):
    def test_load_empty_value_should_return_none(self):
        name = "I dont exists"
        loaded = recalSettings.load(name)
        self.assertEquals(None, loaded)


    def test_load_disabled_value_return_none(self):
        name = "enable_kodi"
        loaded = recalSettings.load(name)
        self.assertEquals(None, loaded)

    def test_load_enabled_value(self):
        name = "game_hdmi_mode"
        loaded = recalSettings.load(name)
        self.assertEquals("4", loaded)

    def test_write_disabled_value(self):
        name = "enable_kodi"
        loaded = recalSettings.load(name)
        self.assertEquals(None, loaded)

        recalSettings.save(name, "anewval")
        loaded = recalSettings.load(name)
        self.assertEquals("anewval", loaded)

        recalSettings.save(name, "1")
        loaded = recalSettings.load(name)
        self.assertEquals("1", loaded)

    def test_disable_value(self):
        name = "enable_kodi"
        recalSettings.save(name, "1")
        loaded = recalSettings.load(name)
        self.assertEquals("1", loaded)
        recalSettings.disable(name)
        loaded = recalSettings.load(name)
        self.assertEquals(None, loaded)

    def test_default_value(self):
        name = "idonotexists"
        loaded = recalSettings.load(name, "default")
        self.assertEquals("default", loaded)

    def test_write_new_value(self):
        name = "hello"
        recalSettings.save(name, "thehellovalue")
        loaded = recalSettings.load(name)
        self.assertEquals("thehellovalue", loaded)

    def test_load_dict(self):
        name = "snes"
        loaded = recalSettings.loadAll(name)
        self.assertEquals(4, len(loaded))
        self.assertEquals('myshaderfile.gplsp', loaded["shaders"])

    def test_ratio_with_slash(self):
        name = "nes.ratio"
        loaded = recalSettings.load(name)
        self.assertEquals("16/9", loaded)


if __name__ == '__main__':
    unittest.main()
