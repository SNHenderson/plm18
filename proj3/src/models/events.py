class Event(object):
    def __init__(self, trigger, action):
        self.trigger = trigger
        self.action = action

    def run(self):
        if self.trigger():
            self.action()