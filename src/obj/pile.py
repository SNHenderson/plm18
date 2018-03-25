from obj.collection import Collection

class Pile(Collection):

    def __init__(self, name, facedown):
        super().__init__(name)
        self.facedown = facedown

    def __str__(self):
        top = "[X]" if self.facedown else str(self.top_card())
        return "[%s:%s(%d)]" % (self.name, top, len(self.cards))

    def top_card(self):
    	return self.cards[-1]