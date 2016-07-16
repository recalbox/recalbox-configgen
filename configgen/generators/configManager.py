#!/usr/bin/env python
import sys
import os
import recalboxFiles
from settings.unixSettings import UnixSettings


class ConfigManager():

    def configure(self, system, emulator='default', core='default', ratio='auto', netplay=None):
        recalSettings = UnixSettings(recalboxFiles.recalboxConf)
        globalSettings = recalSettings.loadAll('global')
        system.config['specials'] = recalSettings.load('system.emulators.specialkeys', 'default')
        if netplay is not None:
            globalSettings['netplaymode'] = netplay
        self.updateConfiguration(system, globalSettings)
        self.updateConfiguration(system, recalSettings.loadAll(system.name))
        self.updateForcedConfig(system, emulator, core, ratio)

    def updateConfiguration(self, system, settings):
        systemSettings = system.config
        # Special case of auto ratio
        if 'ratio' in settings and settings['ratio'] == 'auto':
            del settings['ratio']
        if 'emulator' in settings and settings['emulator'] == 'default':
            del settings['emulator']
        if 'core' in settings and settings['core'] == 'default':
            del settings['core']
        systemSettings.update(settings)
        # ShaderSets
        if ('shaderset' in settings and settings['shaderset'] != ''):
            self.updateShaders(system,settings['shaderset'])

    def updateShaders(self, system, shaderSet):
        if shaderSet != None and shaderSet != 'none':
            shaderfile = recalboxFiles.shaderPresetRoot + '/' + shaderSet + '.cfg'
            systemShader = UnixSettings(shaderfile).load(system.name)
            if systemShader != None:
                system.config['shaders'] = systemShader

    def updateForcedConfig(self, system, emulator, core, ratio):
        if emulator != None and emulator != 'default':
            system.config['emulator'] = emulator
        if core != None and core != 'default':
            system.config['core'] = core
        if ratio != None and ratio != 'auto':
            system.config['ratio'] = ratio
