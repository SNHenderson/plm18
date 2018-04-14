from itertools import product
from itertools import chain
from random import shuffle

from models.card import Card
from models.suit import Suit
from models.rank import Rank

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

