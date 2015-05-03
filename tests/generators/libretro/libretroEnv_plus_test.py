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
# Special file with env config
shutil.copyfile(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/recalbox.conf.origin.libretro")), \
    os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/recalbox.conf.libretro")))
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/es_settings.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_settings.cfg")))

# Injecting test files
libretroEnv.esSettings.settingsFile = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_settings.cfg"))
libretroEnv.recalSettings.settingsFile = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "tmp/recalbox.conf.libretro"))


# test Systems
core_all_default_no_shaders = libretroGen.LibretroCore(name='psx', video_mode='4', core='pcsx_rearmed', shaders='false')
core_video_mode_set = libretroGen.LibretroCore(name='snes', video_mode='5', core='pcsx_rearmed', shaders='false')
core_shader_default_exists = libretroGen.LibretroCore(name='gb', video_mode='5', core='pcsx_rearmed', shaders='false')
core_shader_set_in_conf_not_existing = libretroGen.LibretroCore(name='gba', video_mode='5', core='pcsx_rearmed',
                                                                shaders='false')
core_shader_set_in_conf_exists = libretroGen.LibretroCore(name='mastersystem', video_mode='5', core='pcsx_rearmed',
                                                          shaders='false')

libretroEnv.esSettings.save("Shaders", "true")


class TestLibretroVideoModeEnv(unittest.TestCase):
    def test_video_mode_default(self):
        self.assertEquals("1",libretroEnv.recalSettings.load("snes_emulator"))
        conf = libretroEnv.loadLibretroEnv(core_all_default_no_shaders)
        self.assertEquals(conf["video_mode"], "DEFAULT_VIDEO_MODE")

    def test_video_mode_per_emu(self):
        conf = libretroEnv.loadLibretroEnv(core_video_mode_set)
        self.assertEquals(conf["video_mode"], "SNES_VIDEO_MODE")


class TestLibretroSmoothEnv(unittest.TestCase):
    def test_smooth_enabled_if_no_shader(self):
        conf = libretroEnv.loadLibretroEnv(core_shader_set_in_conf_exists)
        self.assertEqual(conf["shaders"], "true")
        self.assertEqual(conf["shader_file"], "true")


class TestLibretroShadersEnv(unittest.TestCase):


    def test_default_shader(self):
        conf = libretroEnv.loadLibretroEnv(core_all_default_no_shaders)
        self.assertEqual(conf["shaders"], "false")

    def test_shaders_enabled_but_not_existing(self):
        conf = libretroEnv.loadLibretroEnv(core_all_default_no_shaders)
        self.assertEqual(conf["shaders"], "false")

    def test_shaders_enabled_and_default_not_existing(self):
        conf = libretroEnv.loadLibretroEnv(core_shader_set_in_conf_not_existing)
        self.assertEqual(conf["shaders"], "false")

    def test_shader_enabled_and_default(self):
        conf = libretroEnv.loadLibretroEnv(core_shader_default_exists)
        self.assertEqual(conf["shaders"], "true")
        self.assertEqual(conf["shader_file"], "gb.glslp")

    def test_shader_enabled_and_set_in_recalbox(self):
        libretroEnv.esSettings.save("Shaders", "true")
        conf = libretroEnv.loadLibretroEnv(core_shader_set_in_conf_exists)
        self.assertEqual(conf["shaders"], "true")
        self.assertEqual(conf["shader_file"], "true")

        if __name__ == '__main__':
            unittest.main()
