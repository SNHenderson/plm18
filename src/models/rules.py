class Rule(object):
    def __init__(self, rules_list, func):
        self.rules_list = rules_list
        self.func = func

    def check(self, *params):
        return self.func(self.rules_list, *params)
