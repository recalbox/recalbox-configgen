#!/usr/bin/env python

from distutils.core import setup
setup(name='recalbox-configgen',
      version='1.0',
      py_modules=['configgen'],
      packages=['configgen', 
        'configgen.generators', 
        'configgen.generators.fba2x', 
        'configgen.generators.kodi', 
        'configgen.generators.libretro', 
        'configgen.generators.linapple', 
        'configgen.generators.moonlight', 
        'configgen.generators.mupen', 
        'configgen.generators.scummvm', 
        'configgen.settings','configgen.utils'],
      )
