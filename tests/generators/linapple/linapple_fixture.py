'''
Created on Mar 10, 2016

@author: laurent
'''
from runtest.fixture import FixtureJoystick
        
class Joystick(FixtureJoystick):
    '''
    Class implementing fixture's expected results for the specified controller.
    
    The base class implements fixture required parameters to enable the 
    controller. It also groups parameters and results before giving them to the 
    TestCase method.
    
    '''
    def results(self, controller, index, player, verbose=True):
        '''
        Provide results expected for the specified requested parameters.
        
        The format of the result is free, here a dictionary is used, you can 
        use your own, as you will be responsible to check the result in your 
        TestCase method.  
        
        Args:
            controller (controllerConfig.Controller):
                Controller that will be used by the player (player)
            index (int): 
                System index of the controller
            player (int): 
                Player number
                
        Returns (dict, None):
            Return the dictionary that will be apply to linapple settings to make
            same changes as the tested function.
            Return an empty dictionary for ignored players (2-5)
            Return None if an error occured, so the TestCase method is able to 
            skip the test.
            
        '''
        # Find the input corresponding to the requested type (itype)
        def find(itype, *choices):
            for a in choices:
                value = controller.inputs.get(a, None)
                if value is None: continue
                if value.type != itype: continue
                else: break
            else:
                raise UserWarning('Unsupported hardware (no {})'.format(itype))
            
            if verbose:
                exp = choices[0]
                if (a != exp) :
                    msg = '[INFO] Uses ({}) instead of ({})'.format(a, exp)
                    print(self.message(controller, message=msg))
            
            return str(value.id)
            
        
        # Player number is zero based in linapple
        player = player - 1
        try:
            results = {} if player > 0 else {
        # Strange button behaviour with 2 joysticks enabled :-( TBD
        #    results = {} if player > 1 else {
                'Joystick {}'.format(player) : '1',
                'Joy{}Index'.format(player) : str(index),
                'Joy{}Axis0'.format(player) : 
                    find('axis', 'joystick1left', 'joystick2left', 'left'),
                'Joy{}Axis1'.format(player) : 
                    find('axis','joystick1up', 'joystick2up', 'up'),
                'Joy{}Button1'.format(player) : 
                    find('button', 'pagedown','x'),
            }
            if player  < 1 :
                results.update({
                    'Joy{}Button2'.format(player) : 
                        find('button', 'pageup', 'y'),
                    'JoyExitEnable' : '1',
                    'JoyExitButton0' : 
                        str(controller.inputs['select'].id),
                    'JoyExitButton1' : 
                        str(controller.inputs['start'].id),
                })
                    
        except Exception as e:
            print(self.message(controller, message='[WARNING] {}'.format(e)))
            results = None

        return results
    
# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4: