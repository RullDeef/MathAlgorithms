import re

from matalg.core.atoms import Context
from matalg.models.markov import MarkovModel, Rule
from matalg.parsers.abstract import AbstractParser

class MarkovParser(AbstractParser):
    def __parse_rule(self, context: Context, line: str) -> Rule:
        lhs, rhs = line.split("->")

        lhs = context.wrap_string(lhs.strip())
        rhs = context.wrap_string(rhs.strip())

        return Rule(lhs, rhs)

    def __parse_final_rule(self, context: Context, line: str) -> Rule:
        lhs, rhs = line.split("->.")

        lhs = context.wrap_string(lhs.strip())
        rhs = context.wrap_string(rhs.strip())

        return Rule(lhs, rhs, final=True)

    def parse_model(self, lines: list, context: Context) -> MarkovModel:
        rules = []

        rule_re = re.compile(r".*?\s*->\s*.*?")
        final_rule_re = re.compile(r".*?\s*->\.\s*.*?")

        for line in lines:
            if final_rule_re.fullmatch(line):
                rules.append(self.__parse_final_rule(context, line))
            elif rule_re.fullmatch(line):
                rules.append(self.__parse_rule(context, line))

        return MarkovModel(context, rules)
