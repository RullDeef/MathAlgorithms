from matalg.core.atoms import Symbol, MetaSymbol, \
    RegularSymbol, SymbolSequence, Context
from matalg.models.markov import Rule, MarkovModel

def test_MarkovModel():
    context = Context()
    context.add_regular("a")
    context.add_regular("b")
    context.use_alphabet_from_string("abcde")

    print(context)

    left = SymbolSequence()

    sym = context.get_sym("a")
    assert type(sym) is RegularSymbol
    assert str(sym) == "a"
    left.feed(sym)

    sym = context.get_sym("c")
    assert type(sym) is Symbol
    assert str(sym) == "c"
    left.feed(sym)

    print(left.seq)
    assert str(left) == "ac"

    right = SymbolSequence()
    right.feed(context.get_sym("c"))
    right.feed(context.get_sym("a"))

    assert str(right) == "ca"

    rules = [Rule(left, right)]
    model = MarkovModel(context, rules)

    conf = model.init_configuration("aebcbd")
    assert conf is not None
    assert conf.context is context
    assert not conf.is_final
    assert str(conf.string) == "aebcbd"
    
    print("start conf:", repr(conf.string))

    while not conf.is_final:
        conf = model.make_step(conf)
        print("conf:", repr(conf.string))

    print("final conf:", repr(conf.string))
    assert conf.is_final
