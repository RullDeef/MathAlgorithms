class Symbol(object):
    def __init__(self, sym: str):
        self.value = sym

    def __repr__(self) -> str:
        return f"S({self.value})"

class RegularSymbol(Symbol):
    def __repr__(self) -> str:
        return f"R({self.value})"

class MetaSymbol(Symbol):
    def __repr__(self) -> str:
        return f"M({self.value})"

class SymbolSequence(object):
    def __init__(self):
        self.seq = []

    def __str__(self) -> str:
        return "".join(map(str, self.seq))

    def __len__(self) -> int:
        return len(self.seq)

    def __getitem__(self, i: int):
        return self.seq[i]
    
    def __setitem__(self, i: int, sym: 'Symbol'):
        if not isinstance(sym, Symbol):
            print("bad set item! Sym has unexpected type")
        self.seq[i] = sym

    def clone(self) -> 'SymbolSequence':
        copy = SymbolSequence()
        copy.seq = list(self.seq)
        return copy

    def feed(self, sym: 'Symbol'):
        if not isinstance(sym, Symbol):
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
                self.seq[i:i+sublen] = replacement.seq
                return

class Context(object):
    def __init__(self):
        self.meta_symbols = set()
        self.regular_symbols = list()
        self.alphabet = list()

    def __repr__(self) -> str:
        regulars = " ".join(repr(a) for a in self.regular_symbols)
        meta = " ".join(repr(m) for m in self.meta_symbols)
        return f"Context({{{regulars}}}, {{{meta}}})"

    def add_regular(self, sym: str):
        self.regular_symbols.append(Symbol(sym))

    def add_meta(self, sym: str):
        self.meta_symbols.add(MetaSymbol(sym))

    def get_sym(self, sym: str) -> 'Symbol':
        for s in self.meta_symbols:
            if s.value == sym:
                return s

        for s in self.regular_symbols:
            if s.value == sym:
                return s

        for s in self.alphabet:
            if s.value == sym:
                return sym

        return Symbol(sym)

    def use_alphabet(self, alphabet: str):
        self.alphabet = [Symbol(c) for c in alphabet]
        return self.alphabet

    # translates string using regular and meta symbols
    # for lhs and rhs of rule templates
    def wrap_string(self, string: str) -> 'SymbolSequence':
        seq = SymbolSequence()
        for c in string:
            seq.feed(self.get_sym(c))
        return seq

    # converts string to symbol objects using alphabet
    def prepare_string(self, string: str) -> 'SymbolSequence':
        seq = SymbolSequence()
        for char in string:
            sym = Symbol(char)
            for s in self.alphabet:
                if s.value == char:
                    sym = s
                    break
            seq.feed(sym)
        return seq
