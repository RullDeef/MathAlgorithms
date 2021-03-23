from itertools import product

class Symbol(object):
    class_symbol = "S"

    def __init__(self, value: str):
        self.value = value

    def __repr__(self) -> str:
        return f"{self.class_symbol}{id(self) % 1000}({self.value})"

    def __str__(self) -> str:
        return self.value

class RegularSymbol(Symbol):
    class_symbol = "R"

class MetaSymbol(Symbol):
    class_symbol = "M"

class SymbolSequence(object):
    def __init__(self):
        self.seq = list()

    def __repr__(self) -> str:
        return "".join(map(repr, self.seq))

    def __str__(self) -> str:
        return "".join(map(str, self.seq))

    def __len__(self) -> int:
        return len(self.seq)

    def __getitem__(self, i: int):
        return self.seq[i]

    def __setitem__(self, i: int, sym: Symbol):
        if not isinstance(sym, Symbol):
            print("bad set item! Sym has unexpected type")
        self.seq[i] = sym

    def clone(self) -> 'SymbolSequence':
        copy = SymbolSequence()
        copy.seq = list(self.seq)
        return copy

    def feed(self, sym: Symbol):
        if not isinstance(sym, (Symbol, RegularSymbol, MetaSymbol)):
            print("error. Sym has unexpected type")
        else:
            self.seq.append(sym)

    def has_subseq(self, subseq: 'SymbolSequence') -> bool:
        sublen = len(subseq)
        for i in range(len(self) - sublen + 1):
            for j in range(sublen):
                if self[i + j] is not subseq[j]:
                    break
            else:
                return True
        return False

    def replace(self, subseq: 'SymbolSequence', replacement: 'SymbolSequence'):
        sublen = len(subseq)
        for i in range(len(self) - sublen + 1):
            for j in range(sublen):
                if self[i + j] is not subseq[j]:
                    break
            else:
                self.seq[i:i + sublen] = replacement.seq
                return

    def bind_symbol(self, reg: RegularSymbol, sym: Symbol):
        for i in range(len(self)):
            if self.seq[i] == reg:
                self.seq[i] = sym

class Context(object):
    def __init__(self):
        self.alphabet = list()
        self.meta_symbols = set()
        self.regular_symbols = list()

    def __repr__(self) -> str:
        regulars = " ".join(repr(a) for a in self.regular_symbols)
        meta = " ".join(repr(m) for m in self.meta_symbols)
        alpha = " ".join(repr(a) for a in self.alphabet)
        return f"Context({{{regulars}}}, {{{meta}}}, [{alpha}])"

    def __str__(self) -> str:
        regulars = " ".join(str(a) for a in self.regular_symbols)
        meta = " ".join(str(m) for m in self.meta_symbols)
        alpha = "".join(str(a) for a in self.alphabet)
        return f"(R{{{regulars}}}, M{{{meta}}}, [{alpha}])"

    def add_sym(self, sym: str):
        if sym in map(str, self.alphabet):
            print("duplicate of symbol in context")
        else:
            self.alphabet.append(Symbol(sym))

    def add_regular(self, sym: str):
        if sym in map(str, self.regular_symbols):
            print("duplicate of regular symbol in context")
        else:
            self.regular_symbols.append(RegularSymbol(sym))

    def add_meta(self, sym: str):
        if sym in map(str, self.meta_symbols):
            print("duplicate of meta symbol in context")
        else:
            self.meta_symbols.add(MetaSymbol(sym))

    def get_sym(self, sym: str) -> Symbol:
        for s in self.meta_symbols:
            if s.value == sym:
                return s

        for s in self.regular_symbols:
            if s.value == sym:
                return s

        for s in self.alphabet:
            if s.value == sym:
                return s

        print("strange sym!", sym)
        return Symbol(sym)

    def use_alphabet_from_string(self, string: str):
        for c in string:
            if c not in list(map(str, self.alphabet)):
                self.alphabet.append(Symbol(c))
        return self.alphabet

    # translates string using regular and meta symbols
    # for lhs and rhs of rule templates
    def wrap_string(self, string: str) -> SymbolSequence:
        seq = SymbolSequence()
        for c in string:
            seq.feed(self.get_sym(c))
        return seq

    # converts string to symbol objects using alphabet
    def prepare_string(self, string: str) -> SymbolSequence:
        seq = SymbolSequence()
        for char in string:
            for s in self.alphabet:
                if s.value == char:
                    seq.feed(s)
                    break
            else:
                print("bad input character at prepare_string")
                seq.feed(Symbol(char))
        return seq

    # (a, a, a) (a, a, b) (a, b, a) (a, b, b) ...
    def __iterate_over_regulars(self, amount=0):
        if amount == 1:
            for sym in self.alphabet:
                yield sym,
        elif amount > 1:
            for sym in self.alphabet:
                for other in self.__iterate_over_regulars(amount - 1):
                    yield sym, *other

    def map_regulars(self, regulars: list):
        for symbols in self.__iterate_over_regulars(len(regulars)):
            yield zip(regulars, symbols)
