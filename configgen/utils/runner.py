#!/usr/bin/env python
import subprocess
import os
import time

import videoMode

proc = None

# Set a specific video mode
def runCommand(command):
    global proc
    if command.videomode != 'default':
        videoMode.setVideoMode(command.videomode)
        time.sleep(0.5)
    command.env.update(os.environ)
    proc = subprocess.Popen(command.array, stdout=subprocess.PIPE, env=command.env)
    exitcode = -1
    try:
        exitcode = proc.wait()
    except:
        print("emulator exited")

    if command.videomode != 'default':
        videoMode.setPreffered()

    return exitcode
