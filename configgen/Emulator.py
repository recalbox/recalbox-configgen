class Emulator():

    def __init__(self, name, emulator, core='', videomode='CEA 4 HDMI', shaders='', ratio='auto', smooth='1', rewind='0', configfile=None):
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