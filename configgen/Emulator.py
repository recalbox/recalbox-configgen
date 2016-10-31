import recalboxFiles
import xml.etree.ElementTree as ET

class Emulator():

    def __init__(self, name, emulator, core='', videomode='CEA 4 HDMI', shaders='', ratio='auto', smooth='1', rewind='0', configfile=None, showFPS=None):
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
        self.config['showFPS'] = showFPS
        
            
    def getDrawFPS(self):
        esConfig = ET.parse(recalboxFiles.esSettings)
        value = esConfig.find("./bool[@name='DrawFramerate']").attrib["value"]
        if value not in ['false', 'true']:
            value = 'false'
        self.config['showFPS'] = value
        
    def lateInit(self):
        if self.config['showFPS'] is None or self.config['showFPS'] not in ['false', 'true']:
            self.getDrawFPS()
