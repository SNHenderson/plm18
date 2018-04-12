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
        return self.top_card().value

    def rank(self):
        return self.top_card().rank

    def suit(self):
        return self.top_card().suit

    def end(self):
        return self.top_card()

    def top_card(self):
        if self.cards:
            return self.cards[-1]

    def bottom_card(self):
        if self.cards:
            return self.cards[0]    

    def replenish(self, pile, count):
        count = int(count)
        self.cards = pile[:count]
        del pile[:count]
