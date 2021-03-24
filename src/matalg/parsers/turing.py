import re

from matalg.core.atoms import MetaSymbol, Context
from matalg.models.turing import TuringContext, State, Rule, TuringConfiguration, TuringModel
from matalg.parsers.abstract import AbstractParser


class TuringParser(AbstractParser):
    def parse_context(self, lines) -> TuringContext:
        context = super().parse_context(lines)
        return TuringContext.wrap_context(context)

    def parse_rule(self, context: Context, curr_state: State, states: list, line: str) -> Rule:
        match = re.fullmatch(r"(.*?)\s*->\s*([^ ]+?)\s+(.*?),\s*([LSR])", line)
        look_sym = context.get_sym(match[1]) if len(match[1]) > 0 else MetaSymbol.Space
        repl_sym = context.get_sym(match[3]) if len(match[3]) > 0 else MetaSymbol.Space

        for state in states:
            if state.value == match[2]:
                state_to = state
                break
        else:
            state_to = State(match[2])
            states.append(state_to)

        step = {"L": Rule.Step.LEFT, "S": Rule.Step.STOP, "R": Rule.Step.RIGHT}[match[4]]
        return Rule(curr_state, state_to, look_sym, repl_sym, step)
    
    def parse_marker_rule(self, context: Context, curr_state: State, states: list, line: str) -> Rule:
        match = re.fullmatch(r">>\s*(.*?)\s*,\s*([SR])", line)

        for state in states:
            if state.value == match[1]:
                state_to = state
                break
        else:
            state_to = State(match[1])
            states.append(state_to)

        for state in states:
            if state.value == match[1]:
                state_to = state
                break
        else:
            state_to = State(match[1])
            states.append(state_to)

        step = {"L": Rule.Step.LEFT, "S": Rule.Step.STOP, "R": Rule.Step.RIGHT}[match[2]]
        return Rule(curr_state, state_to, context.marker, context.marker, step)


    def parse_model(self, lines: list, context: Context) -> TuringModel:
        start_state, end_state = State("q0"), State("qf", final=True)
        states = [start_state, end_state]
        rules = []

        state_def_re = re.compile(r".+:")
        marker_rule_re = re.compile(r">>\s*.*?\s*,\s*[SR]")
        rule_re = re.compile(r".*?\s*->\s*.+?\s*,\s*[LSR]")

        curr_state = None

        for line in lines:
            if state_def_re.fullmatch(line):
                curr_state = line[:-1].strip()

                # find corresponding state in states list
                for state in states:
                    if state.value == curr_state:
                        curr_state = state
                        break
                else:
                    curr_state = State(curr_state)
                    states.append(curr_state)

            elif marker_rule_re.fullmatch(line):
                rules.append(self.parse_marker_rule(context, curr_state, states, line))

            elif rule_re.fullmatch(line):
                rules.append(self.parse_rule(context, curr_state, states, line))

        return TuringModel(context, rules, start_state, end_state)
