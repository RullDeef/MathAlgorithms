from matalg.core.atoms import Context, SymbolSequence, RegularSymbol
from matalg.core.configuration import AbstractConfiguration
from matalg.models.abstract import AbstractModel

class MarkovConfiguration(AbstractConfiguration):
    def __init__(self, string: SymbolSequence, context: Context):
        super().__init__(context)
        self.__string = string

    @property
    def string(self) -> SymbolSequence:
        return self.__string

    def representation(self) -> str:
        return str(self.__string)

    def is_empty(self) -> bool:
        return len(self.__string) == 0


# represents particular substitution
class Rule:
    def __init__(self, lhs: SymbolSequence, rhs: SymbolSequence, final=False):
        self.lhs = lhs
        self.rhs = rhs
        self.final = final

    def __repr__(self):
        lhs, rhs = repr(self.lhs), repr(self.rhs)
        return f"{lhs} ->{'.' if self.final else ''} {rhs}"

    def __str__(self):
        return f"{self.lhs} ->{'.' if self.final else ''} {self.rhs}"

    def __get_regular_syms(self) -> int:
        regulars = list()

        for sym in self.lhs.seq:
            if isinstance(sym, RegularSymbol) and sym not in regulars:
                regulars.append(sym)

        for sym in self.rhs.seq:
            if isinstance(sym, RegularSymbol) and sym not in regulars:
                regulars.append(sym)

        return regulars

    def __expanded(self, context: Context) -> (SymbolSequence, SymbolSequence):
        '''gather all regular symbols in current rule'''

        regs = self.__get_regular_syms()
        if len(regs) == 0:
            yield self.lhs, self.rhs
        else:
            for mapping in context.map_regulars(regs):
                lhs, rhs = self.lhs.clone(), self.rhs.clone()
                for reg, sym in mapping:
                    lhs.bind_symbol(reg, sym)
                    rhs.bind_symbol(reg, sym)
                yield lhs, rhs

    def applicable(self, conf: MarkovConfiguration) -> bool:
        '''checks if it can be applied to given configuration'''

        string, context = conf.string, conf.context
        for lhs, rhs in self.__expanded(context):
            if conf.string.has_subseq(lhs):
                return True
        return False

    def apply(self, conf: MarkovConfiguration) -> MarkovConfiguration:
        if not conf.is_final:
            string, context = conf.string, conf.context
            for lhs, rhs in self.__expanded(context):
                if string.has_subseq(lhs):
                    string.replace(lhs, rhs)
                    break
            conf = MarkovConfiguration(string, context)
            if self.final:
                conf.make_final()
        return conf


class MarkovModel(AbstractModel):
    def __init__(self, context: Context, rules: list):
        super().__init__(context)
        self.__rules = rules

    def init_configuration(self, string: str) -> MarkovConfiguration:
        string = super().init_configuration(string)
        return MarkovConfiguration(string, self.context)

    def make_step_into(self, conf: MarkovConfiguration) -> MarkovConfiguration:
        if not conf.is_final:
            for rule in self.__rules:
                if rule.applicable(conf):
                    conf = rule.apply(conf)
                    break
            else:
                # natural ending
                conf = MarkovConfiguration(conf.string, conf.context)
                conf.make_final()
        return conf
