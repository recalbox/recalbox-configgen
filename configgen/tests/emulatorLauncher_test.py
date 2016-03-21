#!/usr/bin/env python

import os
import sys
import unittest
import shutil

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "resources/es_input.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "resources/es_input.cfg")))

# Injecting test es_input


class TestEmulatorLauncher(unittest.TestCase):
    def test_init(self):
        pass

if __name__ == '__main__':
    unittest.main()
