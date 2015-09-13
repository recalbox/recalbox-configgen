import os
import sys
import os.path
import unittest
import shutil
import controllersConfig
import time
import settings.unixSettings as unixSettings
import generators
from generators.configManager import ConfigManager
from Emulator import Emulator

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

scanlinesFile = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/scanlines.cfg"))
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/scanlines_shaderset.cfg")), \
                scanlinesFile)
recalboxConf = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/recalbox.conf"))
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../resources/recalbox.conf.origin")), \
                recalboxConf)


class ConfigManagerTest(unittest.TestCase):
    def setUp(self):
        self.snes = Emulator(name='snes', videomode='4', core='pocketsnes', shaders='', ratio='16/9', smooth='2',
                             rewind='false', emulator='libretro')
        self.wswan = Emulator(name='wswan', videomode='4', core='wswan', shaders='defaultshaders', ratio='16/9', smooth='2',
                             rewind='false', emulator='libretro')
        generators.configManager.recalboxFiles.shaderPresetRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/"))
        generators.configManager.recalboxFiles.recalboxConf = recalboxConf
        self.manager = ConfigManager()

    def test_globalOverrideSystemConfig(self):
        globalConf = {'shaders':'myshaders'}
        self.manager.updateConfiguration(self.wswan, globalConf)
        self.assertEquals(self.wswan.config['shaders'], 'myshaders')


    def test_autoRatio(self):
        globalConf = {'ratio':'auto'}
        self.manager.updateConfiguration(self.snes, globalConf)
        self.assertEquals(self.snes.config['ratio'], '16/9')


    def test_globalShaderSet(self):
        self.manager.configure(self.wswan)
        self.assertEquals(self.wswan.config['shaders'], '/path/to/my/scanline/wswan/shader/from/configfile.cfg')

    def test_specificShaderOverrideGlobalShader(self):
        self.manager.configure(self.snes)
        self.assertEquals(self.snes.config['shaders'], 'myshaderfile.gplsp')


    def test_specificShaderOverrideglobalShaderSet(self):
        self.manager.configure(self.snes)
        self.assertEquals(self.snes.config['shaders'], 'myshaderfile.gplsp')


    def test_shaderSetNone(self):
        self.manager.updateShaders(self.wswan, "none")
        self.assertEquals(self.wswan.config['shaders'], 'defaultshaders')

    def testNoShaderSetInConfig(self):
        pass