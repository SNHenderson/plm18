from utils.objs import dict_obj
 
class Rule(dict_obj):
    def __init__(self, rules_list, func):
        self.rules_list = rules_list
        self.func = func

    def check(self, *params):
        return self.func(self.rules_list, *params)