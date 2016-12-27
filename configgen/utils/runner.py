#!/usr/bin/env python
import subprocess
import os
import time
import sys

import videoMode

proc = None

# Set a specific video mode
def runCommand(command):
    global proc

    if command.videomode != 'default':
        videoMode.setVideoMode(command.videomode)
        if command.delay is not None:
            time.sleep(command.delay)

    command.env.update(os.environ)
    proc = subprocess.Popen(command.array, env=command.env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    exitcode = -1
    try:
        out, err = proc.communicate()
        exitcode = proc.returncode
        sys.stdout.write(out)
        sys.stderr.write(err)
    except:
        print("emulator exited")

    if command.videomode != 'default':
        videoMode.setPreffered()

    return exitcode
