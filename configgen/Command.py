#!/usr/bin/env python

class Command:
    def __init__(self, videomode, array, env=dict(), delay = None):
        self.videomode = videomode
        self.array = array
        self.env = env
        self.delay = delay
