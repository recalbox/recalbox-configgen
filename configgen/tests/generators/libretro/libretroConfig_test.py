#!/usr/bin/env python

import os
import sys
import os.path
import unittest
import shutil
from Emulator import Emulator


sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

import generators.libretro.libretroConfig as libretroConfig
import generators.libretro.libretroGenerator as libretroGen
import settings.unixSettings as unixSettings
import settings.recalboxSettings as recalSettings

retroarchcustomFile = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/retroarchcustom.cfg'))
recalboxConfFile = os.path.abspath(os.path.join(os.path.dirname(__file__), 'tmp/recalbox.conf'))

# Cloning config files
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/retroarchcustom.cfg.origin')), \
                retroarchcustomFile)
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../resources/recalbox.conf.origin')), \
                recalboxConfFile)



libretroSettings = unixSettings.UnixSettings(retroarchcustomFile, ' ' )

# test Systems
snes = Emulator(name='snes', videomode='4', core='pocketsnes', shaders='', ratio='auto', smooth='2', rewind='false', emulator='libretro')
nes = Emulator(name='nes', videomode='4', core='pocketsnes', shaders='', ratio='16/9', smooth='1', rewind='false', emulator='libretro')
nes43 = Emulator(name='nes', videomode='4', core='pocketsnes', shaders='myshaders.gpslp', ratio='4/3', smooth='1', rewind='false', emulator='libretro')
nesauto = Emulator(name='nes', videomode='4', core='pocketsnes', shaders='myshaders.gpslp', ratio='auto', smooth='1', rewind='true', emulator='libretro')
nes43 = Emulator(name='nes', videomode='4', core='pocketsnes', shaders='myshaders.gpslp', ratio='4/3', smooth='1', rewind='false', emulator='libretro')
wswan = Emulator(name='wswan', emulator='libretro', core='mednafen_wswan', ratio='16/10')


class TestLibretroConfig(unittest.TestCase):
    def setUp(self):
        # Injecting test file
        recalSettings.settingsFile = recalboxConfFile
        libretroConfig.libretroSettings = libretroSettings

    def test_smooth_override_defaut_and_global(self):
        settings = snes.config
        settings.update(recalSettings.loadAll('snes'))
        retroconf = libretroConfig.createLibretroConfig(snes)
        self.assertEquals(retroconf['video_smooth'], 'false')

    def test_create_with_shader_true(self):
        settings = snes.config
        settings.update(recalSettings.loadAll('snes'))
        retroconf = libretroConfig.createLibretroConfig(snes)
        self.assertEquals(retroconf['video_shader'], 'myshaderfile.gplsp')
        self.assertEquals(retroconf['video_shader_enable'], 'true')
        self.assertEquals(retroconf['video_smooth'], 'false')

    def test_create_with_shader_true_and_smooth_true(self):
        settings = snes.config
        settings.update(recalSettings.loadAll('snes'))
        retroconf = libretroConfig.createLibretroConfig(snes)
        self.assertEquals(retroconf['video_shader_enable'], 'true')
        self.assertEquals(retroconf['video_smooth'], 'false')


    def test_create_with_ratio_169(self):
        retroconf = libretroConfig.createLibretroConfig(nes)
        self.assertEquals(retroconf['aspect_ratio_index'], '1')
        self.assertEquals(retroconf['video_aspect_ratio_auto'], 'false')


    def test_create_with_ratio_43(self):
        retroconf = libretroConfig.createLibretroConfig(nes43)
        self.assertEquals(retroconf['aspect_ratio_index'], '0')
        self.assertEquals(retroconf['video_aspect_ratio_auto'], 'false')

    def test_create_with_ratio_auto(self):
        retroconf = libretroConfig.createLibretroConfig(nesauto)
        self.assertEquals(retroconf['video_aspect_ratio_auto'], 'true')

    def test_create_rewind_true(self):
        retroconf = libretroConfig.createLibretroConfig(nesauto)
        self.assertEquals(retroconf['rewind_enable'], 'true')

    def test_create_rewind_false(self):
        retroconf = libretroConfig.createLibretroConfig(nes)
        self.assertEquals(retroconf['rewind_enable'], 'false')


    def test_write_config_to_file(self):
        retroconf = libretroConfig.createLibretroConfig(nesauto)
        libretroConfig.writeLibretroConfigToFile(retroconf)
        self.assertEquals(libretroSettings.load('rewind_enable'), 'true')

    def test_write_config_to_file_shaders(self):
        retroconf = libretroConfig.createLibretroConfig(nes43)
        libretroConfig.writeLibretroConfigToFile(retroconf)
        self.assertEquals(libretroSettings.load('rewind_enable'), 'false')
        self.assertEquals(libretroSettings.load('video_shader'), 'myshaders.gpslp')
        self.assertEquals(libretroSettings.load('video_shader_enable'), 'true')
        self.assertEquals(libretroSettings.load('aspect_ratio_index'), '0')
        self.assertEquals(libretroSettings.load('video_aspect_ratio_auto'), 'false')


    def test_write_config_to_file_new1610(self):
        retroconf = libretroConfig.createLibretroConfig(wswan)
        libretroConfig.writeLibretroConfigToFile(retroconf)
        self.assertEquals(libretroSettings.load('aspect_ratio_index'), '2')
        self.assertEquals(libretroSettings.load('video_aspect_ratio_auto'), 'false')

    def test_driver_udev_default(self):
        nes.config['inputdriver'] = None
        retroconf = libretroConfig.createLibretroConfig(nes)
        self.assertEquals(retroconf['input_joypad_driver'], 'udev')

    def test_driver_forced_sdl(self):
        nes.config['inputdriver'] = 'sdl2'
        retroconf = libretroConfig.createLibretroConfig(nes)
        self.assertEquals(retroconf['input_joypad_driver'], 'sdl2')


if __name__ == '__main__':
    unittest.main()