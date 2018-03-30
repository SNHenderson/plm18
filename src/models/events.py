from utils.objs import dict_obj
 
class Event(dict_obj):
    def __init__(self, trigger, action, *params):
        self.trigger = trigger
        self.action = action
        self.params = params

    def run(self):
        if self.trigger():
            self.action(*self.params)