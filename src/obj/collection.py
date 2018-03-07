from utils.validation import validate
from utils.validation import Validatable

class Collection(Validatable):
    def __init__(self, name=None):
        super().__init__()
        self.cards = [] # TODO: an ordered set would be better
        self.name = name

    @validate(undo=lambda self, *cards: [self.cards.remove(c) for c in cards])
    def add(self, *cards):
        self.cards.extend(cards)

    @validate(undo=lambda self, card: self.insert(self._tmp, card))
    def remove(self, card):
        self._tmp = self.cards.index(card) # temporarily store the index in case we need to undo
        self.cards.pop(self._tmp)

    def __getitem__(self, key):
        return self.cards[key]

    def __repr__(self):
        return "[" + self.name + ":" + ",".join(map(str, self.cards)) + "]"