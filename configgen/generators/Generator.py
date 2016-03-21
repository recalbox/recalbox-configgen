from abc import ABCMeta, abstractmethod


class Generator(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def generate(self, system, rom, playersControllers):
        pass
    
    #@abstractmethod
    def config_upgrade(self, version):
        print("{} does not support configuration upgrade yet".format(self.__class__.__name__))
        return False
