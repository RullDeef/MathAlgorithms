from matalg.core.atoms import Symbol, MetaSymbol, SymbolSequence, Context
from matalg.core.configuration import AbstractConfiguration
from matalg.models.abstract import AbstractModel


class TuringContext(Context):
    def __init__(self):
        super().__init__()
        self.marker = MetaSymbol.Marker
        self.space = MetaSymbol.Space

    def prepare_string(self, string: str) -> SymbolSequence:
        seq = SymbolSequence()
        seq.push_back(self.marker)
        for char in string:
            for s in self.alphabet:
                if s.value == char:
                    seq.push_back(s)
                    break
            else:
                print("bad input character at prepare_string")
                seq.push_back(Symbol(char))
        seq.push_back(self.space)
        return seq

    @staticmethod
    def wrap_context(context: Context):
        tur_con = TuringContext()
        tur_con.alphabet = context.alphabet
        tur_con.meta_symbols = context.meta_symbols
        tur_con.regular_symbols = context.regular_symbols
        return tur_con


class State:
    def __init__(self, value: str, final=False):
        self.value = value
        self.__final = final

    def __str__(self) -> str:
        return self.value

    @property
    def is_final(self) -> bool:
        return self.__final


class TuringConfiguration(AbstractConfiguration):
    def __init__(self, state: State, left: SymbolSequence, right: SymbolSequence, context: TuringContext):
        super().__init__(context)
        self.__state = state
        self.__left = left
        self.__right = right
    
    def __str__(self) -> str:
        s = ""
        for sym in self.__left.seq + self.__right.seq:
            if sym is not MetaSymbol.Marker and sym is not MetaSymbol.Space:
                s += str(sym)
        return s

    @property
    def is_final(self) -> bool:
        return self.__state.is_final

    def is_empty(self) -> bool:
        return len(self.left) + len(self.right) == 2 # only marker and space symbols

    @property
    def state(self) -> State:
        return self.__state

    @property
    def left(self) -> SymbolSequence:
        return self.__left

    @property
    def right(self) -> SymbolSequence:
        return self.__right

    def representation(self) -> str:
        look = self.__right.pop_front()
        bad_look = look is None
        rep = f"{self.__left}[{'' if bad_look else look}]{self.__right}"
        self.__right.push_front(look)
        return f"{self.__state}: {rep}"


class Rule:
    class Step:
        LEFT    = 0
        STOP    = 1
        RIGHT   = 2

    def __init__(self, state_from: State, state_to: State, look_sym: Symbol, repl_sym: Symbol, step: 'Rule.Step'):
        self.state_from = state_from
        self.state_to = state_to
        self.look_sym = look_sym
        self.repl_sym = repl_sym
        self.step = step

    def __str__(self) -> str:
        qs = str(self.state_from)
        qf = str(self.state_to)
        sym = str(self.look_sym)
        repl = str(self.repl_sym)
        step = "LSR"[self.step]

        if self.look_sym is MetaSymbol.Marker:
            return f"{qs} >> {qf} , {step}"
        else:
            return f"{qs} {sym} -> {qf} {repl}, {step}"

    def applicable(self, conf: TuringConfiguration) -> bool:
        if self.state_from is conf.state:
            # if len(conf.left) == 0 and self.look_sym is MetaSymbol.Marker:
            #     return True
            # if len(conf.right) == 1 and self.look_sym is MetaSymbol.Space:
            #     return True
            return self.look_sym == conf.right[0]
        return False

    def apply(self, conf: TuringConfiguration) -> TuringConfiguration:
        if not conf.is_final:
            context = conf.context
            left, right = conf.left.clone(), conf.right.clone()
            right.pop_front()
            right.push_front(self.repl_sym)
            if self.step == Rule.Step.LEFT:     right.push_front(left.pop_back())
            elif self.step == Rule.Step.RIGHT:  left.push_back(right.pop_front())
            while len(right) > 0 and right.seq[-1] is MetaSymbol.Space: right.pop_back()
            right.push_back(MetaSymbol.Space)
            conf = TuringConfiguration(self.state_to, left, right, context)
        return conf


class TuringModel(AbstractModel):
    def __init__(self, context: TuringContext, rules: list, start_state: State, end_state: State):
        super().__init__(context)
        self.__rules = rules
        self.__start_state = start_state
        self.__end_state = end_state

    def init_configuration(self, string: str) -> TuringConfiguration:
        string = super().init_configuration(string)
        # string.push_front(self.context.get_sym("(*)"))
        return TuringConfiguration(self.__start_state, SymbolSequence(), string, self.context)

    def make_step_into(self, conf: TuringConfiguration) -> TuringConfiguration:
        if not conf.is_final:
            for rule in self.__rules:
                if rule.applicable(conf):
                    return rule.apply(conf)
        return conf
