from normalg.context import Context, SymbolSequence
from normalg.configuration import Configuration

# represents particular substitution
class Rule(object):
    def __init__(self, lhs: SymbolSequence, rhs: SymbolSequence, final=False):
        self.lhs = lhs
        self.rhs = rhs
        self.final = final

    def __repr__(self):
        lhs, rhs = repr(self.lhs), repr(self.rhs)
        return f"{lhs} ->{'.' if self.final else ''} {rhs}"

    def __str__(self):
        return f"{self.lhs} ->{'.' if self.final else ''} {self.rhs}"

    # checks if it can be applied to given sequence string
    def applyable_seq(self, string: SymbolSequence) -> bool:
        return string.has_subseq(self.lhs)

    def applyable(self, conf: Configuration) -> bool:
        return conf.string.has_subseq(self.lhs)

    def apply(self, conf: Configuration) -> Configuration:
        if not conf.final:
            conf = conf.clone()
            conf.string.replace(self.lhs, self.rhs)
            conf.final = self.final
        return conf

class RuleTemplate(object):
    def __init__(self,
            lhs: 'SymbolSequence',
            rhs: 'SymbolSequence',
            final: bool,
            context: 'Context'):
        self.lhs = lhs
        self.rhs = rhs
        self.final = final
        self.context = context

    def __repr__(self) -> str:
        lhs, rhs = repr(self.lhs), repr(self.rhs)
        return f"{lhs} ->{'.' if self.final else ''} {rhs}"

    def has_regular_symbols(self) -> bool:
        for sym in self.lhs:
            if sym in self.context.regular_symbols:
                return True
        return False

    def get_first_reg_sym(self) -> 'Symbol':
        for sym in self.lhs:
            if sym in self.context.regular_symbols:
                return sym
        print("bad regular symbol!")
        return None

    # returns simple rules list for given alphabet symbols(=objects!)
    def expand(self, alphabet: list):
        rules = []
        if not self.has_regular_symbols():
            rules.append(Rule(self.lhs, self.rhs, self.final))
        else:
            reg_sym = self.get_first_reg_sym()
            for sym in alphabet:
                lhs, rhs = self.lhs.clone(), self.rhs.clone()
                for i, elem in enumerate(lhs):
                    if elem is reg_sym: lhs[i] = sym
                for i, elem in enumerate(rhs):
                    if elem is reg_sym: rhs[i] = sym
                expanded_rule = RuleTemplate(lhs, rhs, self.final, self.context)
                rules.extend(expanded_rule.expand(alphabet))
        return rules
