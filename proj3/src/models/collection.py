from random import shuffle

class Collection(object):
    def __init__(self, name=None):
        self.cards = []
        self.name = name
        self.owner = None

    def add(self, *cards):
        self.cards.extend(cards)

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
        return len(self)

    def shuffle(self):
        shuffle(self.cards)

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
        return "<" + val + ">"

    def replenish(self, source, count):
        count = int(count)
        self.cards = source[:count] + self.cards
        del source[:count]

