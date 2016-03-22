#!/usr/bin/env python
import sys
import os.path
import unittest
import shutil

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import configgen.settings.emulationstationSettings as esSettings

shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/es_settings.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_settings.cfg")))


# Injecting test es_input.cfg
esSettings.settingsFile = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_settings.cfg"))


class TestEmulationstationSettings(unittest.TestCase):
    def test_load_empty_value_should_return_none(self):
        name = "I dont exists"
        loaded = esSettings.load(name)
        self.assertEquals(None, loaded)

    def test_load_value_return_a_value(self):
        name = "Smooth"
        loaded = esSettings.load(name)
        self.assertEquals("true", loaded)

    def test_load_default(self):
        name = "I do not exists"
        loaded = esSettings.load(name, "default")
        self.assertEquals("default", loaded)

    def test_write_value(self):
        name = "Smooth"
        esSettings.save(name, "false")
        loaded = esSettings.load(name)
        self.assertEquals("false", loaded)
        esSettings.save(name, "true")
        loaded = esSettings.load(name)
        self.assertEquals("true", loaded)

    def test_write_new_value(self):
        name = "UnexistingVal"
        esSettings.save(name, "false")
        loaded = esSettings.load(name)
        self.assertEquals("false", loaded)
        esSettings.save(name, "true")
        loaded = esSettings.load(name)
        self.assertEquals("true", loaded)


if __name__ == '__main__':
    unittest.main()
