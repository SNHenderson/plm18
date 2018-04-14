class Rule(object):
    def __init__(self, check_function):
        self.check_function = check_function

    def check(self, action):
        return self.check_function(action)

