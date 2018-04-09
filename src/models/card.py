from models.rank import Rank

class Card(object):
    # TODO: maybe make this immutable?

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = Rank[self.rank].value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __eq__(self, other):
        same_suit = self.suit == other.suit
        same_rank = self.rank == other.rank
        return same_suit and same_rank

    def __hash__(self):
        return hash((self.suit, self.rank))

    def __repr__(self):
        return "[%s %s]" % (self.rank, self.suit)

    def __str__(self):
        # TODO: The way we want to display the card during the game should go here
        return repr(self)
