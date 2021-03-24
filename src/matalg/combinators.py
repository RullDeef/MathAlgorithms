from abc import abstractmethod
from matalg.core.atoms import Context
from matalg.core.configuration import AbstractConfiguration
from matalg.models.abstract import AbstractModel
from matalg.parsers.abstract import AbstractParser


class CombinatorConfiguration(AbstractConfiguration):
    def __init__(self, executor, executor_state, context: Context, conf: AbstractConfiguration):
        super().__init__(context)
        self.__executor = executor
        self.state = executor_state
        self.wrapped = conf

    @property
    def executor(self):
        return self.__executor

    def representation(self) -> str:
        return f"{self.executor}: {self.wrapped.representation()}"

    def is_empty(self) -> bool:
        return self.wrapped.is_empty()


class AbstractCombinator(AbstractModel):
    class BadExecutorException(Exception):
        pass

    def __str__(self) -> str:
        return ""

    @abstractmethod
    def make_step_into(self, conf: CombinatorConfiguration) -> CombinatorConfiguration:
        pass

    @abstractmethod
    def make_step_over(self, conf: CombinatorConfiguration, *, timeout=1) -> CombinatorConfiguration:
        pass


class ConditionalCombinator(AbstractCombinator):
    class States:
        CONDITION   = 0
        ACCEPT      = 1
        REJECT      = 2

    def __init__(self, context: Context, condition: AbstractModel, accept: AbstractModel, reject: AbstractModel):
        super().__init__(context)
        self.__condition = condition
        self.__accept = accept
        self.__reject = reject
        self.__string = None

    def init_configuration(self, string: str) -> CombinatorConfiguration:
        self.__string = string

        super().init_configuration(string)
        conf = self.__condition.init_configuration(string)

        # wrap conf into CombinatorConfiguration
        return CombinatorConfiguration(self, self.States.CONDITION, self.context, conf)

    def make_step_into(self, conf: CombinatorConfiguration) -> CombinatorConfiguration:
        if conf.executor is not self:
            raise AbstractCombinator.BadExecutorException()

        elif not conf.is_final:

            if conf.state == self.States.CONDITION:
                conf.wrapped = self.__condition.make_step_into(conf.wrapped)
                if conf.wrapped.is_final:
                    if conf.is_empty():
                        conf.state = self.States.ACCEPT
                        conf.wrapped = self.__accept.init_configuration(self.__string)
                    else:
                        conf.state = self.States.REJECT
                        conf.wrapped = self.__reject.init_configuration(self.__string)

            elif conf.state == self.States.ACCEPT:
                conf.wrapped = self.__accept.make_step_into(conf.wrapped)
                if conf.wrapped.is_final: conf.make_final()

            elif conf.state == self.States.REJECT:
                conf.wrapped = self.__reject.make_step_into(conf.wrapped)
                if conf.wrapped.is_final: conf.make_final()

        return conf

    def make_step_over(self, conf: CombinatorConfiguration, *, timeout=1) -> CombinatorConfiguration:
        if conf.executor is not self:
            print("bad executor!!!")

        elif conf.is_final:
            print("bad final state (cond comb!)")

        elif conf.state == self.States.CONDITION:
            conf.wrapped = self.__condition.run(conf.wrapped)
            if conf.wrapped.is_final:
                if conf.is_empty():
                    conf.state = self.States.ACCEPT
                    conf.wrapped = self.__accept.init_configuration(self.__string)
                else:
                    conf.state = self.States.REJECT
                    conf.wrapped = self.__reject.init_configuration(self.__string)

        elif conf.state == self.States.ACCEPT:
            conf.wrapped = self.__accept.run(conf.wrapped, timeout=timeout)
            conf.make_final()

        elif conf.state == self.States.REJECT:
            conf.wrapped = self.__reject.run(conf.wrapped, timeout=timeout)
            conf.make_final()
        return conf


class CompositionalCombinator(AbstractCombinator):
    def __init__(self, context: Context):
        super().__init__(context)


class CyclicCombinator(AbstractCombinator):
    def __init__(self, context: Context, loop_bool: bool):
        super().__init__(context)
        self.loop_bool = loop_bool


class AcceptCyclicCombinator(CyclicCombinator):
    def __init__(self, context: Context):
        super().__init__(context, True)


class RejectCyclicCombinator(CyclicCombinator):
    def __init__(self, context: Context):
        super().__init__(context, False)


class CombinatorParser(AbstractParser):
    def parse_model(self, lines: list, context: Context) -> AbstractCombinator:
        return
