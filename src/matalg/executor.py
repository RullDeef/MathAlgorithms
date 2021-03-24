import sys, time, argparse
from matalg.parsers.markov import MarkovParser
from matalg.parsers.turing import TuringParser

class ErrorCode:
    BAD_TIMEOUT_VALUE   = -3
    BAD_MODEL           = -2
    HELP_SHOWN          = -1
    SUCCESS             = 0
    TIMEOUT_EXCEED      = 1

def main(argv=None) -> int:
    arg_parser = argparse.ArgumentParser("matalg", description="Executes algorithm models.")
    arg_parser.add_argument("-f", "--file", help="algorithm source file", nargs=1)
    arg_parser.add_argument("-t", "--trace", help="trace execution by steps", action="store_true")
    arg_parser.add_argument("-i", "--timeout", help="set timeout [default=1 sec]", nargs=1, type=float)
    arg_parser.add_argument("-T", help="parse as turing machine", action="store_true")
    arg_parser.add_argument("-M", help="parse as markov algorifm", action="store_true")
    arg_parser.add_argument("input_string", metavar="input", type=str, nargs="?", help="input string")

    if argv is None: argv = sys.argv[1:]
    namespace = arg_parser.parse_args(argv)

    if namespace.file is None:
        arg_parser.print_help()
        return ErrorCode.HELP_SHOWN

    if namespace.T and namespace.M or (not namespace.T and not namespace.M):
        print("Choose either Turing or Markov model.")
        return ErrorCode.BAD_MODEL

    if namespace.timeout is not None and namespace.timeout[0] <= 0:
        print("Bad timeout value")
        return ErrorCode.BAD_TIMEOUT_VALUE

    timeout = 1.0 if namespace.timeout is None else namespace.timeout[0]
    source = open(namespace.file[0], "r").read()
    algo = (MarkovParser() if namespace.M else TuringParser()).parse_source(source)

    string = input() if namespace.input_string is None else namespace.input_string
    conf = algo.init_configuration(string)

    if namespace.trace:
        print("start: ", conf.representation())
        start_time = time.time()
        while time.time() - start_time < timeout:
            conf = algo.make_step_into(conf)
            if conf.is_final:
                break
            print("next:  ", conf.representation())
        else:
            print("timeout exceed")
            return ErrorCode.TIMEOUT_EXCEED
        print("result:", conf.representation())
    else:
        try:
            conf = algo.run(conf, timeout=timeout)
            print(conf)
        except TimeoutError:
            print("timeout exceed")
            return ErrorCode.TIMEOUT_EXCEED

    return ErrorCode.SUCCESS
