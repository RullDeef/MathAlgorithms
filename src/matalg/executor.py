import sys, argparse
from matalg.parsers.markov import MarkovParser

def main():
    arg_parser = argparse.ArgumentParser("matalg", description="Executes algorithm models.")
    arg_parser.add_argument("-f", "--file", help="algorithm source file", nargs=1)
    arg_parser.add_argument("-t", "--trace", help="trace execution by steps", action=argparse.BooleanOptionalAction)
    arg_parser.add_argument("input_string", metavar="input", type=str, nargs="?", help="input string")

    namespace = arg_parser.parse_args(sys.argv[1:])

    if namespace.file is None:
        arg_parser.print_help()
        return

    source = open(namespace.file[0], "r").read()
    algo = MarkovParser().parse_source(source)

    string = input() if namespace.input_string is None else namespace.input_string
    conf = algo.init_configuration(string)

    if namespace.trace:
        print("start: ", conf)
        while True:
            conf = algo.make_step(conf)
            if conf.is_final:
                break
            print("next:  ", conf)
        print("result:", conf)
    else:
        try:
            conf = algo.run(conf)
        except TimeoutError:
            print("timeout exceed")
