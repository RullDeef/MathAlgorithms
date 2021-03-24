from matalg.parsers.markov import MarkovParser

from matalg.combinators import ConditionalCombinator

def test_ConditionalCombinator():
    context_source = """
        for a, b, c in V
        #, $ not in V
    """

    source_1 = """
        // del first, move 2nd to the end

        $ab -> b$a
        $ ->.
        a -> $
        ->.
    """

    source_2 = """
        // del first, move 2nd & 3rd to the end

        #abc -> c#ab
        # ->.
        a -> #
        ->.
    """

    source_3 = """
        // is even length condition

        ab ->
        ->.
    """

    parser = MarkovParser()

    context = parser.parse_context(parser.linearize(context_source))

    model_1 = parser.parse_model(parser.linearize(source_1), context)
    model_2 = parser.parse_model(parser.linearize(source_2), context)
    model_3 = parser.parse_model(parser.linearize(source_3), context)

    model = ConditionalCombinator(context, model_3, model_1, model_2)

    conf = model.init_configuration("abcdace")
    print(conf.representation())

    while not conf.is_final:
        conf = model.make_step_into(conf)
        print(conf.representation())
