from models.collection import Collection

class Pile(Collection):

    def __init__(self, name, facedown):
        super().__init__(name)
        self.facedown = facedown

    def __str__(self):
        top = "[X]" if self.facedown else str(self.top_card())
        return "[%s:%s(%d)]" % (self.name, top, len(self.cards))

    def rank(self):
        return self.cards[-1].rank

    def suit(self):
        return self.cards[-1].suit    

    def top_card(self):
        return self.cards[-1]

    def bottom_card(self):
        return self.cards[0]    

    def facedown_cards(self):
        return self.cards[:-1]  

    def replenish(self, pile):
        self.cards = pile[:-1]
        del pile[:-1]