'''
Created on Mar 6, 2016

@author: Laurent Marchelli
'''
import os
#import sys

# Define working directories
dir_root = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
dir_res = os.path.join(dir_root, 'tests/resources')
dir_tmp = os.path.join(dir_root , 'tests/tmp')
# if dir_root not in sys.path:
#     sys.path.append(dir_root)

# Override configuration directories
import recalboxFiles
recalboxFiles.esInputs = os.path.join(dir_res, 'es_input.cfg')
recalboxFiles.esSettings = os.path.join(dir_res, 'es_settings.cfg')
recalboxFiles.recalboxConf = os.path.join(dir_res, 'recalbox.conf')
recalboxFiles.savesDir = os.path.join(dir_tmp, 'saves')

from .fixture import FixtureJoystick, fixture_joystick
from .case import TestCase, RedirectStdStreams
from .loader import TestLoader, main
