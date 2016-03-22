'''
Created on Mar 11, 2016

@author: Laurent Marchelli
'''
import unittest
main = unittest.main

class TestLoader(unittest.TestLoader):
    _str_fixture_class = '_runtest_fixture_class'
    _str_fixture_args = '_runtest_fixture_args'
    _str_fixture_kwargs = '_runtest_fixture_kwargs'

    def __init__(self):
        self.fixtures = dict()

    def loadTestsFromTestCase(self, testCaseClass):
        """Return a suite of all tests cases contained in testCaseClass"""
        if issubclass(testCaseClass, unittest.TestSuite):
            raise TypeError("Test cases should not be derived from TestSuite." \
                                " Maybe you meant to derive from TestCase?")
        tests = []
        testCaseNames = self.getTestCaseNames(testCaseClass)
        if testCaseNames:
            for t in testCaseNames:
                fn = getattr(testCaseClass, t)
                fix_cls = getattr(fn, self._str_fixture_class, None)
                if fix_cls is not None:
                    tests.extend(self.loadTestsFromFixture(
                                testCaseClass, t, fn, fix_cls))
                else:
                    tests.append(testCaseClass(t))
                    
        elif hasattr(testCaseClass, 'runTest'):
            tests = [testCaseClass('runTest')]

        loaded_suite = self.suiteClass(tests)
        return loaded_suite

    def loadTestsFromFixture(self, testCaseClass, name, fn, fix_cls):
        # First check if we already generated this fixture previously
        fix_args = getattr(fn, self._str_fixture_args)
        fix_kwargs = getattr(fn, self._str_fixture_kwargs)
        fix_key = str(fix_cls) + str(fix_args) + \
                    str(sorted(fix_kwargs.items()))
        fix_list = self.fixtures.get(fix_key, None)

        # The fixture does not exist yet, create it
        if fix_list is None:
            fix_obj = fix_cls(*fix_args, **fix_kwargs)
            fix_list = fix_obj.generate() 
            self.fixtures[fix_key] = fix_list

        # Create test list from the fixture  
        fix_tests = [testCaseClass(name, params=p, results=r, msg=m)
                    for (p, r, m) in fix_list]
        return fix_tests 
