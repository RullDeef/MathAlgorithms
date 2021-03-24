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

        self.context.use_alphabet_from_string(string)
        return self.context.prepare_string(string) # TODO: wrong return type

    @abstractmethod
    def make_step_into(self, conf: AbstractConfiguration) -> AbstractConfiguration:
        '''makes single step, creating new configuration'''

        pass

    def make_step_over(self, conf: AbstractConfiguration, *, timeout=1) -> AbstractConfiguration:
        return self.make_step_into(conf)

    def run(self, conf: AbstractConfiguration, *, timeout=1) -> AbstractConfiguration:
        start_time = time.time()
        while not conf.is_final and time.time() - start_time < timeout:
            conf = self.make_step_over(conf, timeout=timeout)
        if time.time() - start_time >= timeout:
            raise TimeoutError()
        return conf
