from abc import ABCMeta, abstractmethod


class Generator(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def generate(self, system, rom, playersControllers):
        pass
