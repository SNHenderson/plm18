from utils.objs import dict_obj
 
class Event(dict_obj):
    def __init__(self, trigger, action):
        self.trigger = trigger
        self.action = action

    def run(self):
        if self.trigger():
            self.action()