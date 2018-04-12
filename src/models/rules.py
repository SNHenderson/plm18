class Rule(object):
    def __init__(self, rule, func):
        self.rule_expression = rule
        self.func = func

    def check(self, *params):
        return self.func(self.rule_expression, *params)
