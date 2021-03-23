from matalg.models.markov import MarkovModel
from matalg.parsers.markov import MarkovParser

def test_MarkovParser():
    parser = MarkovParser()

    source = """
    for a in V
    c in V
    #, $ not in V

    #a -> a#
    # -> $
    c -> #
    ->.
    """

    model = parser.parse_source(source)
    print(model.context)
    assert len(model._MarkovModel__rules) == 4
    assert len(model.context.alphabet) == 1
