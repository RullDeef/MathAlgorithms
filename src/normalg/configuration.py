from normalg.context import SymbolSequence

class Configuration(object):
    def __init__(self, string: SymbolSequence):
        self.string = string
        self.final = False

    def __repr__(self) -> str:
        return f"Conf({repr(self.string)})"

    def __str__(self) -> str:
        return str(self.string)
    
    def empty(self) -> bool:
        return len(self.string) == 0

    def clone(self) -> 'Configuration':
        new_conf = Configuration(self.string.clone())
        new_conf.final = self.final
        return new_conf
