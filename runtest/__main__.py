#!/usr/bin/env python
'''
Created on Mar 11, 2016

@author: laurent
'''
import sys
if sys.argv[0].endswith("__main__.py"):
    sys.argv[0] = "python -m runtest"

# Override the loader, so we can detect fixtures
import loader 
loader.main(testLoader=loader.TestLoader())
