from utils.validation import validate
from utils.validation import Validatable

class Collection(Validatable):
    def __init__(self, name=None):
        super().__init__()
        self.cards = []
        self.name = name
        self.owner = None

    @validate(undo=lambda self, *cards: [self.cards.remove(c) for c in cards])
    def add(self, *cards):
        self.cards.extend(cards)

    @validate(undo=lambda self, card: self.insert(self._tmp, card))
    def remove(self, card):
        self._tmp = self.cards.index(card) # temporarily store the index in case we need to undo
        self.cards.pop(self._tmp)

    def set_owner(self, player):
        """
        Sets the owner of the collection to a player;
        should only be called in Player.add_collection();
        the assertion enforces this requirement
        """
        assert player.owns(self)
        self.owner = player

    def contains(self, card):
        return card in self.cards

    def size(self):
        return self.__len__()

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, key):
        return self.cards[key]

    def __delitem__(self, key):
        del self.cards[key]

    def __setitem__(self, key, item):
        self.cards[key] = item

    def __repr__(self):
        val = self.name
        if self.cards:
            val += ":" + ",".join(map(str, self.cards))
        return "[" + val + "]"

