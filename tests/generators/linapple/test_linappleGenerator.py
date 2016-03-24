#!/usr/bin/env python
'''
Created on Mar 7, 2016

@author: laurent
'''
import os
import argparse
import cStringIO

# Import runtest classes
import runtest
import linapple_fixture

# Import needed configgen modules
import configgen.emulatorlauncher as emulatorlauncher
from configgen.generators.linapple.linappleConfig import LinappleConfig
from configgen.generators.linapple.linappleGenerator import LinappleGenerator

class TestLinappleGenerator(runtest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Call base class
        runtest.TestCase.setUpClass('apple2', 'linapple')
        
        # Configure test class resources
        cls.path_init_conf = os.path.join(cls.path_init, 'linapple.conf')
        cls.path_user_conf = os.path.join(cls.path_user, 'linapple.conf')

    @classmethod
    def tearDownClass(cls):
        runtest.TestCase.tearDownClass()
    
    def setUp(self):
        super(self.__class__, self).setUp()
        self.maxDiff = None
    
    def tearDown(self):
        super(self.__class__, self).tearDown()
    
    @runtest.fixture_joystick(linapple_fixture.Joystick, 5)
    def test_main(self):
        # Override LinappleGenerator to echo the command instead than really 
        # executing it.
        generator = LinappleGenerator(self.path_init, self.path_user)
        generator.cmdArray.insert(0, '/bin/echo')
        emulatorlauncher.generators['linapple'] = generator
        
        # Load settings from system configuration file and apply 
        # expected results
        config_init = LinappleConfig(self.path_init_conf)
        config_init.settings.update(self.results)

        # Run tested function with updated arguments and load settings from
        # user configuration. 
        self.args.update(self.params)

        # Call main functions with args updated with fixture parameters and
        # outpout redirected into a string.
        main_stdout = cStringIO.StringIO()
        with runtest.RedirectStdStreams(main_stdout):
            emulatorlauncher.main(argparse.Namespace(**self.args))
        output_str = main_stdout.getvalue()
        main_stdout.close()

        config_user = LinappleConfig(self.path_user_conf)
        
        # Check results
        self.assertDictContentEqual(config_init.settings,
                                    config_user.settings)

    def test_config_upgrade(self):
        generator = LinappleGenerator(self.path_init, self.path_user)
        generator.config_upgrade('v4.0.0 2016/03/20 01:19')
        
    def test_config_upgrade_all(self):
        result = True
        generators = emulatorlauncher.generators
        for _,g in generators.items():
            result &= g.config_upgrade('v4.0.0 2016/03/20 01:19')
            
        #self.assertTrue(result)

if __name__ == "__main__":
    runtest.main(testLoader=runtest.TestLoader())
    
# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: