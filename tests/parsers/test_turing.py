from matalg.models.turing import TuringModel
from matalg.parsers.turing import TuringParser


def test_TuringParser():
    source = """
    a, b in V
    # not in V

    q0:
        >> q0 , R
        a -> q0 #, R
        b -> q0 b, R
        -> q1 , L
    
    q1:
        b -> q1 b, L
        # -> q1 #, L
        >> qf , S
    """

    parser = TuringParser()
    model = parser.parse_source(source)

    rules = [str(r) for r in model._TuringModel__rules]
    print(*rules, sep="\n")

    conf = model.init_configuration("abbab")
    print(conf)

    i = 0
    while not conf.is_final and i < 20:
        conf = model.make_step_into(conf)
        print(conf)
        i += 1
