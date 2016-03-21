#!/usr/bin/env python

import sys
import os.path
import unittest
import shutil
from configgen.Emulator import Emulator


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import configgen.generators.fba2x.fba2xConfig as fba2xConfig
import configgen.settings.unixSettings as unixSettings

fba2xCustom = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/fba2x.cfg'))

# Cloning config files
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/fba2x.cfg.origin')), \
                fba2xCustom)

fbaSettings = unixSettings.UnixSettings(fba2xCustom)

# test Systems
fba2xNormal = Emulator(name='fba', videomode='4', ratio='auto', smooth='1', emulator='fba2x')
fba2x43 = Emulator(name='fba', videomode='4', ratio='4/3', smooth='0', shaders='scanlines',  emulator='fba2x')
fba2x169 = Emulator(name='fba', videomode='4', ratio='16/9', emulator='fba2x')


class TestFBAConfig(unittest.TestCase):
    def setUp(self):
        # Injecting test file
        fba2xConfig.fbaSettings = fbaSettings

    def test_ratioAutoReturnsMaintainAspect1(self):
        fbaConf = fba2xConfig.createFBAConfig(fba2xNormal)
        self.assertEquals(fbaConf['MaintainAspectRatio'], '1')

    def test_ratio43ReturnsMaintainAspect1(self):
        fbaConf = fba2xConfig.createFBAConfig(fba2x43)
        self.assertEquals(fbaConf['MaintainAspectRatio'], '1')


    def test_ratio169ReturnsMaintainAspect0(self):
        fbaConf = fba2xConfig.createFBAConfig(fba2x169)
        self.assertEquals(fbaConf['MaintainAspectRatio'], '0')

    def test_SmoothReturnsDisplaySmoothStretch(self):
        fbaConf = fba2xConfig.createFBAConfig(fba2xNormal)
        self.assertEquals(fbaConf['DisplaySmoothStretch'], '1')

    def test_SmoothOffReturnsDisplaySmoothStretch0(self):
        fbaConf = fba2xConfig.createFBAConfig(fba2x43)
        self.assertEquals(fbaConf['DisplaySmoothStretch'], '0')

    def test_shadersOffNoScanlines(self):
        fbaConf = fba2xConfig.createFBAConfig(fba2xNormal)
        self.assertEquals(fbaConf['DisplayEffect'], '0')

    def test_shadersSetToScanlineReturnsScanlines(self):
        fbaConf = fba2xConfig.createFBAConfig(fba2x43)
        self.assertEquals(fbaConf['DisplayEffect'], '1')



if __name__ == '__main__':
    unittest.main()