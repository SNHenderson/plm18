class Card(object):
    # TODO: maybe make this immutable?

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

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
