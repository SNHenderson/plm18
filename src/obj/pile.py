from obj.collection import Collection

class Pile(Collection):

    def __init__(self, name, facedown):
        super().__init__(name)
        self.facedown = facedown

    def __str__(self):
        top = "[X]" if self.facedown else str(self.cards[-1])
        return "[%s:%s]" % (self.name, top)
