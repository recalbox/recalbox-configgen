#!/usr/bin/env python

import os
import sys
import os.path
import unittest
import shutil

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import settings.unixSettings as unixSet
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/unixSettings.cfg")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/unixSettings.cfg")))
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/retroarchcustom.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/retroarchcustom.cfg")))
# Injecting test unixSettings
noSeparatorFile = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "tmp/unixSettings.cfg"))
spaceSeparatorFile = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "tmp/retroarchcustom.cfg"))

unixSettings = unixSet.UnixSettings(noSeparatorFile)
recalboxSettings = unixSet.UnixSettings(spaceSeparatorFile, ' ')

class TestUnixSettings(unittest.TestCase):
    def test_load_empty_value_should_return_none(self):
        name = "I dont exists"
        loaded = unixSettings.load(name)
        self.assertEquals(None, loaded)

    def test_load_disabled_value_return_none(self):
        name = "aspect_ratio_index"
        loaded = unixSettings.load(name)
        self.assertEquals(None, loaded)

    def test_load_enabled_value_without_quotes(self):
        name = "config_save_on_exit"
        loaded = unixSettings.load(name)
        self.assertEquals("false", loaded)

    def test_load_enabled_value_with_quotes(self):
        name = "video_threaded"
        loaded = unixSettings.load(name)
        self.assertEquals("true", loaded)

    def test_load_default(self):
        name = "video_threaded_do_not_exsists"
        loaded = unixSettings.load(name, "defaultvalue")
        self.assertEquals("defaultvalue", loaded)

    def test_write_value(self):
        name = "video_threaded"
        unixSettings.save(name, "false")
        loaded = unixSettings.load(name)
        self.assertEquals("false", loaded)

    def test_write_new_value(self):
        name = "unbelievablevalue"
        unixSettings.save(name, "false")
        loaded = unixSettings.load(name)
        self.assertEquals("false", loaded)

    def test_write_disabled_value(self):
        name = "video_aspect_ratio"
        loaded = unixSettings.load(name)
        self.assertEquals(None, loaded)

        unixSettings.save(name, "anewval")
        loaded = unixSettings.load(name)
        self.assertEquals("anewval", loaded)

        unixSettings.save(name, "1")
        loaded = unixSettings.load(name)
        self.assertEquals("1", loaded)

    def test_disable_value(self):
        name = "aspect_ratio_index"
        unixSettings.save(name, "1")
        loaded = unixSettings.load(name)
        self.assertEquals("1", loaded)
        unixSettings.disable(name)
        loaded = unixSettings.load(name)
        self.assertEquals(None, loaded)

    def test_load_all(self):
        name = "snes"
        loaded = unixSettings.loadAll(name)
        self.assertEquals(4, len(loaded))
        self.assertEquals('myshaderfile.gplsp', loaded["shaders"])

class TestUnixSettingsWithSeparator(unittest.TestCase):
    def test_load_empty_value_should_return_none(self):
        name = "I dont exists"
        loaded = recalboxSettings.load(name)
        self.assertEquals(None, loaded)

    def test_load_disabled_value_return_none(self):
        name = "aspect_ratio_index"
        loaded = recalboxSettings.load(name)
        self.assertEquals(None, loaded)

    def test_load_enabled_value_without_quotes(self):
        name = "config_save_on_exit"
        loaded = recalboxSettings.load(name)
        self.assertEquals("false", loaded)

    def test_load_enabled_value_with_quotes(self):
        name = "video_threaded"
        loaded = recalboxSettings.load(name)
        self.assertEquals("true", loaded)

    def test_load_default(self):
        name = "video_threaded_do_not_exsists"
        loaded = recalboxSettings.load(name, "defaultvalue")
        self.assertEquals("defaultvalue", loaded)

    def test_write_value(self):
        name = "video_threaded"
        recalboxSettings.save(name, "false")
        loaded = recalboxSettings.load(name)
        self.assertEquals("false", loaded)

    def test_write_new_value(self):
        name = "unbelievablevalue"
        recalboxSettings.save(name, "false")
        loaded = recalboxSettings.load(name)
        self.assertEquals("false", loaded)

    def test_write_disabled_value(self):
        name = "video_aspect_ratio"
        loaded = recalboxSettings.load(name)
        self.assertEquals(None, loaded)

        recalboxSettings.save(name, "anewval")
        loaded = recalboxSettings.load(name)
        self.assertEquals("anewval", loaded)

        recalboxSettings.save(name, "1")
        loaded = recalboxSettings.load(name)
        self.assertEquals("1", loaded)

    def test_disable_value(self):
        name = "aspect_ratio_index"
        recalboxSettings.save(name, "1")
        loaded = recalboxSettings.load(name)
        self.assertEquals("1", loaded)
        recalboxSettings.disable(name)
        loaded = recalboxSettings.load(name)
        self.assertEquals(None, loaded)


if __name__ == '__main__':
    unittest.main()
