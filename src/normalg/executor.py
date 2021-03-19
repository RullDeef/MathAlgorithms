import sys, argparse
from normalg.algorifm import parse

def main():
    arg_parser = argparse.ArgumentParser("nalg",
        description="Executes normal algorifms.")
    arg_parser.add_argument("-f", "--file",
        help="algorifm source file", nargs=1)
    arg_parser.add_argument("-t", "--trace",
        help="trace execution by steps", action=argparse.BooleanOptionalAction)
    arg_parser.add_argument("input_string", metavar="input", type=str, nargs="?",
        help="input string")

    namespace = arg_parser.parse_args(sys.argv[1:])

    if namespace.file is None:
        arg_parser.print_help()
        return

    source = open(namespace.file[0], "r").read()
    algo = parse(source)

    string = input() if namespace.input_string is None else namespace.input_string
    conf = algo.start(string)

    if namespace.trace:
        print("start: ", conf)

    prev_trace = []
    def callback(conf, trace, _hook=[prev_trace]):
        if _hook[0] != trace:
            print(*trace, sep=": ")
            _hook[0] = list(trace)
        print(f"    {conf}")

    if namespace.trace:
        conf = algo.run(conf, callback)
        print("result:", conf)
    else:
        conf = algo.run(conf)
        print(conf)
