import sys, argparse
from normalg.algorifm import parse

def main():
    arg_parser = argparse.ArgumentParser("nalg", description="Executes normal algorifms.")
    arg_parser.add_argument("-f", "--file",
        help="algorifm source file")
    arg_parser.add_argument("input_string", metavar="input", type=str, nargs="?",
        help="input string")

    namespace = arg_parser.parse_args(sys.argv[1:])

    if namespace.file is None:
        arg_parser.print_help()
        return

    source = open(namespace.file, "r").read()
    algo = parse(source)

    string = input() if namespace.input_string is None else namespace.input_string

    conf = algo.start(string)
    print("start conf:", conf)

    while algo.step(conf)[0] is not False:
        conf = algo.step(conf)[1]
        print("next  conf:", conf)

    conf = algo.step(conf)[1]
    print("final conf:", conf)
