import re

from normalg.configuration import Configuration
from normalg.context import Context
from normalg.rule import RuleTemplate

class MarkovAlgorifm(object):
    def __init__(self, context, rule_templates):
        self.context = context
        self.rule_templates = rule_templates

    def start(self, string: str):
        alphabet = "".join(sorted(list(set(string))))
        alphabet = self.context.use_alphabet(alphabet)
        string = self.context.prepare_string(string)

        rules = []
        for rule_template in self.rule_templates:
            rules.extend(rule_template.expand(alphabet))

        return Configuration(string, rules)

    # @staticmethod
    def step(self, conf: Configuration):
        for rule in conf.rules:
            if rule.applyable(conf.string):
                next_string = rule.apply(conf.string)
                return (not rule.final, Configuration(next_string, conf.rules))
        return (False, conf)

def parse(source: str):
    context = Context()
    rule_templates = []

    for line in source.split("\n"):
        # exclude comments
        line = line.split("//")[0]

        # parse "* not in V" meta symbols
        match = re.match(r"^\s*(.+)\s+not\s+in\s+V\s*$", line)
        if match is not None:
            # extract meta symbols
            metas: str = match[1]
            for sym in map(str.strip, metas.split(",")):
                context.add_meta(sym)
            continue

        # parse regular symbols "* in V"
        match = re.match(r"^\s*(.+)\s+in\s+V\s*$", line)
        if match is not None:
            # extract regular symbols
            regulars: str = match[1]
            for sym in map(str.strip, regulars.split(",")):
                context.add_regular(sym)
            continue

        # parse rule template "* ->(.) *"
        match = re.match(r"^\s*(.*?)\s*->(\.?)\s*(.*?)\s*$", line)
        if match is not None:
            lhs, dot, rhs = match[1], match[2], match[3]
            lhs = context.wrap_string(lhs)
            rhs = context.wrap_string(rhs)
            final = dot == '.'
            rule_templates.append(RuleTemplate(lhs, rhs, final, context))

    return MarkovAlgorifm(context, rule_templates)
