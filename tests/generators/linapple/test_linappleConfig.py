#!/usr/bin/env python
'''
Created on Mar 6, 2016

@author: Laurent Marchelli
'''
import os
import re
import random

# Import runtest classes
import runtest
import linapple_fixture

# Import needed configgen modules
import configgen.controllersConfig as controllersConfig
from configgen.generators.linapple.linappleConfig import LinappleConfig

class TestLinappleConfig(runtest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Call base class
        runtest.TestCase.setUpClass('apple2', 'linapple')
        
        # Configure test class resources
        cls.path_init_conf = os.path.join(cls.path_init, 'linapple.conf')
        cls.path_user_conf = os.path.join(cls.path_user, 'linapple.conf')
    
    @classmethod
    def tearDownClass(cls):
        # Clean test class resources
        
        # Call base class
        runtest.TestCase.tearDownClass()
    
    def setUp(self):
        super(self.__class__, self).setUp()
        self.maxDiff = None
        
    def tearDown(self):
        pass
    
    def test01_load(self):
        '''
        Test load function accurency.
        
        1. Open system configuration file
        2. Count the number of non commented or non empty line.
        3. Load settings from system configuration file.
        4. Check number of settings is equal to the number of valid lines.
        ''' 
        # Count the number of expected parameters
        # Ignore commented or empty lines 
        count = 0
        patten = re.compile(r'^(#.*)|(\s*)$')
        with open(self.path_init_conf, 'r' ) as lines:
            for l in lines:
                m = patten.match(l)
                if not m: count += 1

        # Load system config
        config = LinappleConfig(self.path_init_conf)
                
        # Check result
        self.assertEqual(len(config.settings), count)
        
    def test02_save(self):
        '''
        Test save settings in user configuration file.
        
        1. Load settings from system configuration file.
        2. Save settings in user configuration file.
        3. Load settings from user configuration file.
        4. Check loaded settings is equal to user settings.
        '''
        # Create user settings from system configuration file
        config_user = LinappleConfig(self.path_init_conf)
        filename_init = config_user.filename
        
        # Settings random modifications
        config_user.settings = dict(random.sample(
                    config_user.settings.items(),
                    random.randint(1, len(config_user.settings) -1)))
        
        # Save settings in user configuration file
        config_user.save(self.path_user_conf)
        filename_user = config_user.filename

        # Load settings from user configuration file
        config_load = LinappleConfig(self.path_user_conf)
        filename_load = config_load.filename
                
        # Check results
        self.assertEqual(filename_load, filename_user)
        self.assertNotEqual(filename_init, filename_user)
        self.assertDictContentEqual(config_user.settings,
                                    config_load.settings)
        
    @runtest.fixture_joystick(linapple_fixture.Joystick, 5)
    def test03_joysticks(self):
        # Load settings from system configuration file and apply 
        # expected results
        config_init = LinappleConfig(self.path_init_conf)
        config_init.settings.update(self.results)

        # Apply params to defaults arguments copy
        args = self.args_dict.copy()
        args.update(self.params)
        
        # Load settings from system configuration file and run
        # tested function with parameters
        config_user = LinappleConfig(self.path_init_conf)
        controllers = controllersConfig.loadControllerConfig2(**args)
        config_user.joysticks(controllers)
        
        # Check results
        self.assertDictContentEqual(config_init.settings,
                                    config_user.settings)
    
    def test04_system(self):
        pass

if __name__ == "__main__":
    runtest.main(testLoader=runtest.TestLoader())

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: