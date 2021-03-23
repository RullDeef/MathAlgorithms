from matalg.core.atoms import Context
from matalg.core.configuration import AbstractConfiguration
from abc import abstractmethod, ABCMeta

import time

class AbstractModel(metaclass=ABCMeta):
    def __init__(self, context: Context):
        self.__context = context

    @property
    def context(self) -> Context:
        return self.__context

    @abstractmethod
    def init_configuration(self, string: str) -> AbstractConfiguration:
        '''makes initial configuration from given string'''

        pass

    @abstractmethod
    def make_step(self, conf: AbstractConfiguration) -> AbstractConfiguration:
        '''makes single step, creating new configuration'''

        pass

    def run(self, conf: AbstractConfiguration, *, timeout=1) -> AbstractConfiguration:
        start_time = time.time()
        while not conf.is_final and time.time() - start_time < timeout:
            conf = self.make_step(conf)
        if time.time() - start_time >= timeout:
            raise TimeoutError()
        return conf
