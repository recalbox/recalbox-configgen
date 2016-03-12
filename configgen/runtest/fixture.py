'''
Created on Mar 10, 2016

@author: Laurent Marchelli
'''
import types
import functools
from unittest import SkipTest
from loader import TestLoader

from controllersConfig import loadAllControllersConfig

def fixture_joystick(cls_fix, *args_fix, **kwargs_fix):
    def decorator(fn):
        if not isinstance(fn, (type, types.ClassType)):
            fn_sve = fn
            @functools.wraps(fn)
            def wrapper(*args, **kwargs):
                if args[0].results is None:
                    raise SkipTest('Unsupported hardware')
                else:
                    fn_sve(*args, **kwargs)
            fn = wrapper
            setattr(fn, TestLoader._str_fixture_class,cls_fix)
            setattr(fn, TestLoader._str_fixture_args, args_fix)
            setattr(fn, TestLoader._str_fixture_kwargs, kwargs_fix)
        return fn
    return decorator

class FixtureJoystick(object):
    def __init__(self, players=5):
        # Compute ljust size for display
        ctrls, max_len = loadAllControllersConfig().values(), 0
        for c in ctrls: 
            name = c.configName.strip()
            max_len = max(len(name), max_len)
        
        self.controllers = ctrls
        self.ctrlname_pad = max_len
        self.players = players
    
    def params(self, controller, index, player):
        params = {
            "p{}index".format(player) : index,
            "p{}guid".format(player) : controller.guid,
            "p{}name".format(player) : controller.configName,
            "p{}devicepath".format(player) : '/dev/input/js{}'.format(index),
        }
        return params
    
    def results(self, controller, index, player, verbose=True):
        assert(False)
    
    def message(self, controller, index=None, player=None, message=None):

        msg = '{} x '.format(player) if player is not None else ''
        lpad = self.ctrlname_pad + len(msg)
        
        msg += controller.configName.strip()
        
        if message is None:
            return msg.ljust(lpad)
            
        msg += ' : ' 
        return msg.ljust(lpad + 3) + message
    
    def generate(self):
        ctrl_list = self.controllers 
        fixture = []
        # Create a fixture for each controllers
        for c in ctrl_list:
            supported = True
            verbose = True
            # Create a fixture for each cases (1, 2 ..) players
            for n in range(0, self.players):
                params_dict = {}
                results_dict = {}
                # Ignore unsupported hardware detected with the 1 player 
                # configuration
                if supported:
                    # Merge all players parameters and results
                    for p in range(0, n + 1):
                        args = (c, p, p + 1)
                        params_dict.update(self.params(*args))
                        if results_dict is not None:
                            results = self.results(*args, verbose=verbose)
                            verbose = False
                            if results is None:
                                assert(len(results_dict) == 0)
                                results_dict = None
                            else:
                                results_dict.update(results)
                    fixture.append((params_dict, results_dict, 
                                     self.message(*(c, n, n + 1))))
                supported &= results_dict is not None
        return fixture
        
# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: