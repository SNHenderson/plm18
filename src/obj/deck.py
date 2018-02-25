from itertools import product
from itertools import chain
from random import shuffle

from obj.card import Card
from obj.suit import Suit
from obj.rank import Rank

class Deck(object):
    def __init__(self):
        suits = Suit.__members__
        ranks = Rank.__members__
        cards = { Card(s, r) for (s, r) in product(suits, ranks) }
        self.cards = frozenset(cards)

    def __repr__(self):
        return repr(self.cards)

    def shuffled(self):
        cards = list(self.cards)
        shuffle(cards)
        return cards

    def is_partitioned_by(self, collections):
        cards = [ c for col in collections for c in col.cards ]
        return len(cards) == len(self.cards) and len(self.cards - set(cards)) == 0
