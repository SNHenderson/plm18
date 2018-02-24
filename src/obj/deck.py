from itertools import product
from random import suffle

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
        return shuffle(list(self.cards))
