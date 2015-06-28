import generators


class Emulator():
    def __init__(self, name, core, emulator):
        self.__init__(name, '4', core, '', 'auto', '1', '0', emulator=emulator)

    def __init__(self, name, videomode, core, shaders, ratio, smooth, rewind, configfile=None, emulator="libretro"):
        self.name = name
        self.config = dict()
        self.config['videomode'] = videomode
        self.config['core'] = core
        self.config['emulator'] = emulator
        self.config['shaders'] = shaders
        self.config['ratio'] = ratio
        self.config['smooth'] = smooth
        self.config['rewind'] = rewind
        self.config['configfile'] = configfile