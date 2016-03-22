'''
Created on Mar 6, 2016

@author: Laurent Marchelli
'''
import os
import sys
import shutil
import unittest
from . import dir_res, dir_tmp

class TestCase(unittest.TestCase):
    args_dict = {}

    @classmethod
    def setUpClass(cls, system, emulator):
        # Define test system configuration path 
        cls.path_init = os.path.join(dir_res, emulator)
        cls.path_user = os.path.join(dir_tmp, emulator)
        
        # Define test needed objects
        lst_args = [
            "p1index", "p1guid", "p1name", "p1devicepath",
            "p2index", "p2guid", "p2name", "p2devicepath",
            "p3index", "p3guid", "p3name", "p3devicepath",
            "p4index", "p4guid", "p4name", "p4devicepath",
            "p5index", "p5guid", "p5name", "p5devicepath",
            "system",  "rom", "emulator", "core", "demo",
        ]
        lst_values = [None] * len(lst_args)
        cls.args_dict = dict(zip(lst_args, lst_values))
        cls.args_dict['system'] = system
        cls.args_dict['emulator'] = emulator 
        
    @classmethod
    def tearDownClass(cls):
        pass
    
    def setUp(self):
        # Cleanup previous test temporary files
        if os.path.exists(self.path_user):
            shutil.rmtree(self.path_user)

        # Create test environment
        os.makedirs(self.path_user)
    
        # Copy class args into instance args to avoid corruption by
        # test instances.
        self.args = self.__class__.args_dict.copy()

    def tearDown(self):
        pass
    
    def __init__(self, methodName='runTest', params=None, results=None, msg=None):
        super(TestCase, self).__init__(methodName)
        self.params = params
        self.results = results
        self.message = msg
        
    def __str__(self):
        msg = '' if self.message is None else '({})'.format(self.message)
        return "{}.{}{}".format(self.__class__.__name__, 
                                 self._testMethodName, msg)
        
    def assertDictContentEqual(self, d1, d2, msg=None):
        self.assertListEqual(sorted(d1.items()), 
                             sorted(d2.items()))
     

# Thanks to Rob Cowie (http://stackoverflow.com/users/46690/rob-cowie)
# From : http://stackoverflow.com/posts/6796752/revisions
class RedirectStdStreams(object):
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush(); self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush(); self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        
# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: