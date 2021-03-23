from matalg.core.atoms import Symbol, MetaSymbol, \
    RegularSymbol, SymbolSequence, Context

def test_Symbol():
    pass

def test_MetaSymbol():
    pass

def test_RegularSymbol():
    pass

def test_SymbolSequence():
    s = SymbolSequence()
    assert len(s) == 0
    sym1 = Symbol("a")
    sym2 = RegularSymbol("b")
    sym3 = MetaSymbol("C")

    s.feed(sym1)
    s.feed(sym2)
    s.feed(sym3)
    assert len(s) == 3
    assert str(s) == "abC"

def test_Context():
    c = Context()
    c.use_alphabet_from_string("abcdef")

    regs = [RegularSymbol(s) for s in ""]
    mapping = [list(z) for z in c.map_regulars(regs)]
    assert len(mapping) == 0

    regs = [RegularSymbol(s) for s in "RST"]
    mapping = [list(z) for z in c.map_regulars(regs)]
    assert len(mapping) == 216
