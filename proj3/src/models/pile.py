from models.collection import Collection

class Pile(Collection):

    def __init__(self, name, facedown):
        super().__init__(name)
        self.facedown = facedown

    def __str__(self):
        if self.cards:
            top = "[X]" if self.facedown else str(self.top_card())
        else:
            top = "[?]"
        return "<%s:%s(%d)>" % (self.name, top, len(self.cards))

    def value(self):
        if self.top_card():
            return self.top_card().value
        else:
            return -1

    def rank(self):
        return self.top_card().rank

    def suit(self):
        return self.top_card().suit

    def top_card(self):
        if self.cards:
            return self.cards[-1]

    def replenish(self, source, count):
        count = int(count)
        self.cards = source[:count] + self.cards
        del source[:count]