#!/usr/bin/env python
import Command
import reicastControllers
import recalboxFiles
from generators.Generator import Generator
import shutil
import os.path

def writeReicastConfig(system, playersControllers):
    for index, controller in playersControllers:
        # Get the evdev number
        
