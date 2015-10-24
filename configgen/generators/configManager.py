#!/usr/bin/env python
import sys
import os
import recalboxFiles
from settings.unixSettings import UnixSettings


class ConfigManager():

    def configure(self, system):
        recalSettings = UnixSettings(recalboxFiles.recalboxConf)
        globalSettings = recalSettings.loadAll('global')
        system.config['specials'] = recalSettings.load('system.emulators.specialkeys', 'default')
        self.updateConfiguration(system, globalSettings)
        self.updateConfiguration(system, recalSettings.loadAll(system.name))

    def updateConfiguration(self, system, settings):
        systemSettings = system.config
        # Special case of auto ratio
        if 'ratio' in settings and settings['ratio'] == 'auto':
            del settings['ratio']
        systemSettings.update(settings)
        # ShaderSets
        if ('shaderset' in settings and settings['shaderset'] != ''):
            self.updateShaders(system,settings['shaderset'])



    def updateShaders(self, system, shaderSet):
        if shaderSet != None and shaderSet != "none":
            shaderfile = recalboxFiles.shaderPresetRoot + "/" + shaderSet + ".cfg"
            systemShader = UnixSettings(shaderfile).load(system.name)
            if systemShader != None:
                system.config['shaders'] = systemShader
