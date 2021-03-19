class Configuration(object):
    def __init__(self, string: list, rules: list):
        self.string = string
        self.rules = rules

    def __repr__(self) -> str:
        res = " ".join(repr(c) for c in self.string)
        rules = "\n".join(repr(r) for r in self.rules)
        return f"conf: {res}\nrules:\n{rules}"

    def __str__(self) -> str:
        return "".join(c.value for c in self.string)
