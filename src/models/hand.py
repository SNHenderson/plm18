from models.collection import Collection

class Hand(Collection):

    def swap(self, a, b):
        a_index = self.cards.index(a)
        b_index = self.cards.index(b)
        self.cards[a_index] = b
        self.cards[b_index] = a

    def __str__(self):
        # TODO
        return repr(self)