import re
from collections import OrderedDict

from normalg.configuration import Configuration
from normalg.context import SymbolSequence, Context
from normalg.rule import RuleTemplate

class MarkovAlgorifm(object):
    def __init__(self, name: str, context: Context, rule_templates: list):
        self.name = name
        self.context = context
        self.rule_templates = rule_templates

    def __repr__(self) -> str:
        res = f"alg {self.name}\n"
        for rule in self.rule_templates:
            res += f"  {repr(rule)}\n"
        return res

    def __str__(self) -> str:
        return self.name

    def start(self, string: str) -> Configuration:
        self.context.use_alphabet(string)
        string = self.context.prepare_string(string)

        self.rules = []
        for template in self.rule_templates:
            self.rules.extend(template.expand(self.context.alphabet))

        return Configuration(string)

    def step(self, conf: Configuration) -> Configuration:
        if not conf.final:
            for rule in self.rules:
                if rule.applyable(conf):
                    return rule.apply(conf)
        return conf

    def run(self, conf: Configuration, callback=lambda conf, stack_trace: None, trace: list=[]) -> Configuration:
        while not conf.final:
            for rule in self.rules:
                if rule.applyable(conf):
                    conf = rule.apply(conf)
                    callback(conf, trace + [self.name])
                    break
        return conf

class Composition(MarkovAlgorifm):
    def __init__(self, name: str, algorifms: list):
        self.name = name
        self.algorifms = algorifms

    def __repr__(self) -> str:
        names = map(lambda alg: alg.name, self.algorifms)
        algos = map(lambda alg: repr(alg), self.algorifms)
        res = f"alg {self.name} is {' * '.join(names)}"
        algos = '\n'.join(algos)
        return f"{res}\n{algos}"

    def __str__(self) -> str:
        names = map(lambda alg: str(alg), self.algorifms)
        return " * ".join(names)

    def start(self, string: str) -> Configuration:
        conf = self.algorifms[0].start(string)
        for alg in self.algorifms[1:]:
            alg.start(string)
        return conf

    def run(self, conf: Configuration, callback=lambda conf, stack_trace: None, trace: list=[]) -> Configuration:
        if not conf.final:
            for alg in self.algorifms:
                conf = alg.run(conf, callback, trace + [self.name])
                conf.final = False
            conf.final = True
        return conf

class Condition(MarkovAlgorifm):
    def __init__(self, cond: MarkovAlgorifm, then: MarkovAlgorifm, _else: MarkovAlgorifm):
        self.cond = cond
        self.then = then
        self._else = _else

    def __repr__(self) -> str:
        c = self.cond.name
        t = self.then.name
        e = self._else.name
        res = f"alg {self.name} is {c} ( {t} | {e} )"
        return f"{res}\n{repr(self.cond)}\n{repr(self.then)}\n{repr(self._else)}"

    def __str__(self) -> str:
        c = str(self.cond)
        t = str(self.then)
        e = str(self._else)
        return f"{c} ({t} | {e})"

    def start(self, string: str) -> Configuration:
        self.cond.start(string)
        self.then.start(string)
        return self._else.start(string)

    def run(self, conf: Configuration, callback=lambda conf, stack_trace: None, trace: list=[]) -> Configuration:
        if not conf.final:
            cond = self.cond.run(conf, callback, trace + [self.name])
            conf = self.then.run(
                conf, callback, trace +
                [self.name]) if cond.empty() else self._else.run(
                    conf, callback, trace + [self.name])
        return conf

class LoopAccept(MarkovAlgorifm):
    def __init__(self, cond: MarkovAlgorifm, body: MarkovAlgorifm):
        self.cond = cond
        self.body = body

    def __repr__(self) -> str:
        c = self.cond.name
        b = self.body.name
        res = f"alg {self.name} is {c} {{ {b} }}"
        return f"{res}\n{repr(self.cond)}\n{repr(self.body)}"

    def __str__(self) -> str:
        c = str(self.cond)
        b = str(self.body)
        return f"{c} {{{b}}}"

    def start(self, string: str) -> Configuration:
        self.cond.start(string)
        return self.body.start(string)

    def run(self, conf: Configuration, callback=lambda conf, stack_trace: None, trace: list=[]) -> Configuration:
        if not conf.final:
            while True:
                if self.cond.run(conf, callback, trace + [self.name]).empty():
                    conf = self.body.run(conf, callback, trace + [self.name])
                else:
                    break
        return conf

class LoopReject(MarkovAlgorifm):
    def __init__(self, name: str, cond: MarkovAlgorifm, body: MarkovAlgorifm):
        self.name = name
        self.cond = cond
        self.body = body

    def __repr__(self) -> str:
        c = self.cond.name
        b = self.body.name
        res = f"alg {self.name} is {c} < {b} >"
        return f"{res}\n{repr(self.cond)}\n{repr(self.body)}"

    def __str__(self) -> str:
        c = str(self.cond)
        b = str(self.body)
        return f"{c} <{b}>"

    def start(self, string: str) -> Configuration:
        self.cond.start(string)
        return self.body.start(string)

    def run(self, conf: Configuration, callback=lambda conf, stack_trace: None, trace: list=[]) -> Configuration:
        if not conf.final:
            while True:
                input()
                if not self.cond.run(conf, callback, trace + [self.name]).empty():
                    conf = self.body.run(conf, callback, trace + [self.name])
                    conf.final = False
                else:
                    break
        return conf

def parse_algorifm(name: str, context: Context, source: list):
    rule_templates = []

    while len(source) != 0:
        line = source.pop(0)

        # break parse at "alg * (is)?" line
        match = re.match(r"^alg\s+([a-zA-Z_0-9]+)(\s+is)?$", line)
        if match is not None:
            source.insert(0, line)
            break

        # parse rule template "* ->(.) *"
        match = re.match(r"^(.*?)\s*->(\.?)\s*(.*?)$", line)
        if match is not None:
            lhs, dot, rhs = match[1], match[2], match[3]
            lhs = context.wrap_string(lhs)
            rhs = context.wrap_string(rhs)
            final = dot == '.'
            rule_templates.append(RuleTemplate(lhs, rhs, final, context))

    return MarkovAlgorifm(name, context, rule_templates)

def parse_context(source: list) -> Context:
    context = Context()
    for line in source:

        # parse "* not in V" meta symbols
        match = re.match(r"^(.+)\s+not\s+in\s+V$", line)
        if match is not None:
            # extract meta symbols
            metas: str = match[1]
            for sym in map(str.strip, metas.split(",")):
                context.add_meta(sym)
            continue

        # parse regular symbols "* in V"
        match = re.match(r"^for\s+(.+)\s+in\s+V$", line)
        if match is not None:
            # extract regular symbols
            regulars: str = match[1]
            for sym in map(str.strip, regulars.split(",")):
                context.add_regular(sym)
            continue

    return context

def parse_algorifms(source: list, context: Context) -> OrderedDict:
    algorifms = OrderedDict()

    while len(source) > 0:
        line = source.pop(0)

        # parse inner algorifm "alg *"
        match = re.match(r"^alg\s+([a-zA-Z_0-9]+)$", line)
        if match is not None:
            name = match[1]
            algorifms[name] = parse_algorifm(name, context, source)

    return algorifms

def parse_combination(tokens: list, context: Context, algorifms: OrderedDict) -> MarkovAlgorifm:
    #print("tokens", tokens)
    algo_stack = []
    op_stack = []
    while len(tokens) > 0:
        algo_inserted = False
        token = tokens.pop(0)
        if token in [")", ">", "}"]:
            break
        elif token == "(":
            algo_stack.append(parse_combination(tokens, context, algorifms))
            #print("appended '(' combo:", [str(a) for a in algo_stack])
            algo_inserted = True
        elif token == "*":
            op_stack.append("*")
            #print("op_stack", op_stack)
            #print("appended '(' combo:", [str(a) for a in algo_stack])
        elif token == "<":
            cond = algo_stack.pop()
            body = parse_combination(tokens, context, algorifms)
            algo_stack.append(LoopReject("", cond, body))
            algo_inserted = True
        elif token == "{":
            cond = algo_stack.pop()
            body = parse_combination(tokens, context, algorifms)
            algo_stack.append(LoopAccept("", cond, body))
            algo_inserted = True
        elif token in algorifms.keys():
            algo_stack.append(algorifms[token])
            algo_inserted = True

        if algo_inserted and len(algo_stack) == 2 and len(op_stack) == 1:
            algo_stack = [Composition("", algo_stack[::-1])]
            op_stack = []

    if len(algo_stack) == 2 and len(op_stack) == 1:
        algo_stack = [Composition("", algo_stack[::-1])]
        op_stack = []

    if len(algo_stack) != 1:
        print("op_stack", op_stack)
        print("stack len is bad =", len(algo_stack), "!", [str(a) for a in algo_stack])
    return algo_stack[0]

def parse(source: str):
    source = map(lambda s: s.split("//")[0].strip(), source.split("\n"))
    source = list(filter(lambda s: len(s) > 0, source))

    context = parse_context(list(source))
    algorifms = parse_algorifms(list(source), context)

    first_algo_name = None

    while len(source) > 0:
        line = source.pop(0)

        # parse algorifm composition "alg * is"
        match = re.match(r"^alg\s+([a-zA-Z_0-9]+)\s+is$", line)
        if match is not None:
            name: str = match[1]
            if first_algo_name is None:
                first_algo_name = name

            # parse next line
            line = re.split(r"(\w+|[*|()<>{}])", source.pop(0))
            tokens = list(filter(lambda l: len(l) > 0, map(str.strip, line)))
            algorifms[name] = parse_combination(tokens, context, algorifms)

    if first_algo_name is None:
        first_algo_name = list(algorifms.keys())[0]
    return algorifms[first_algo_name]
