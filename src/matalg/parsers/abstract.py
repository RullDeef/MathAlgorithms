import re

from abc import ABCMeta, abstractmethod
from matalg.core.atoms import Context
from matalg.models.abstract import AbstractModel


class ContextException(Exception):
    '''cannot parse context for given source string'''

    pass


class ContextParser:
    def __parse_meta(self, context: Context, line: str):
        syms = line.split("not")[0].split(",")
        for sym in syms:
            sym = sym.strip()
            if len(sym) == 0: raise ContextException
            context.add_meta(sym.strip())

    def __parse_reg(self, context: Context, line: str):
        syms = line.split("for")[1].split("in")[0].split(",")
        for sym in syms:
            sym = sym.strip()
            if len(sym) == 0: raise ContextException
            context.add_regular(sym)

    def __parse_sym(self, context: Context, line: str):
        syms = line.split("in")[0].split(",")
        for sym in syms:
            sym = sym.strip()
            if len(sym) == 0: raise ContextException
            context.add_sym(sym)

    def parse_context(self, lines: list) -> Context:
        context = Context()

        meta_re = re.compile(r".+?\s+not\s+in\s+.+?")
        reg_re = re.compile(r"for\s+.+?\s+in\s+.+?")
        sym_re = re.compile(r".+?\s+in\s+.+?")

        for line in lines:
            if meta_re.fullmatch(line):
                self.__parse_meta(context, line)
            elif reg_re.fullmatch(line):
                self.__parse_reg(context, line)
            elif sym_re.fullmatch(line):
                self.__parse_sym(context, line)

        return context


class AbstractParser(ContextParser, metaclass=ABCMeta):
    line_comment_start = "//"

    def linearize(self, source: str) -> list:
        def transformer(s: str):
            s = s.split(self.line_comment_start)[0]
            return s.strip()

        token_lines = map(transformer, source.splitlines())
        token_lines = filter(lambda s: len(s) > 0, token_lines)
        return list(token_lines)

    @abstractmethod
    def parse_model(self, lines: list, context: Context) -> AbstractModel:
        '''creates new model from given source string'''

        pass

    def parse_source(self, source: str) -> AbstractModel:
        lines = self.linearize(source)
        context = self.parse_context(list(lines))
        return self.parse_model(lines, context)
