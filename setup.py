#!/usr/bin/env python

from distutils.core import setup
setup(name='recalbox-configgen',
      version='1.0',
      py_modules=['configgen'],
      packages=['configgen', 'configgen.generators', 'configgen.generators.libretro', 'configgen.settings','configgen.utils'],
      )
