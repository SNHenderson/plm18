from models.rank import Rank

class Card(object):
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = Rank[self.rank].value

    def __eq__(self, other):
        same_suit = self.suit == other.suit
        same_rank = self.rank == other.rank
        return same_suit and same_rank

    def __hash__(self):
        return hash((self.suit, self.rank))

    def __repr__(self):
        return "<%s %s>" % (self.rank, self.suit)

    def __str__(self):
        return repr(self)
