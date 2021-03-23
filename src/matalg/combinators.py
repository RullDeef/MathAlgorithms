from matalg.models.abstract import AbstractModel

class AbstractCombinator(AbstractModel):
    def __init__(self):
        super(self)

class ConditionalCombinator(AbstractCombinator):
    def __init__(self):
        super(self)

class CompositionalCombinator(AbstractCombinator):
    def __init__(self):
        super(self)

class CyclicCombinator(AbstractCombinator):
    def __init__(self, loop_bool: bool):
        super(self)
        self.loop_bool = loop_bool

class AcceptCyclicCombinator(CyclicCombinator):
    def __init__(self):
        super(self, True)

class RejectCyclicCombinator(CyclicCombinator):
    def __init__(self):
        super(self, False)
