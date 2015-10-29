#!/usr/bin/env python

class Command:
    def __init__(self, videomode, array, env=dict()):
        self.videomode = videomode
        self.array = array
        self.env = env
