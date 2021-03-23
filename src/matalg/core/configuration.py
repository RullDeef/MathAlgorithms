from matalg.core.atoms import SymbolSequence, Context
from abc import ABCMeta, abstractmethod

class AbstractConfiguration(metaclass=ABCMeta):
    def __init__(self, context: Context):
        self.__context = context
        self.__final = False

    @property
    def context(self) -> Context:
        return self.__context

    @property
    def is_final(self) -> bool:
        return self.__final

    def make_final(self):
        self.__final = True

    @abstractmethod
    def representation(self) -> str:
        '''returns string representation for current configuration'''

        pass
