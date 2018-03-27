from enum import Enum
from utils.validation import ValidationException

class Positions(Enum):
    FIRST = 1
    LAST = 2
    ANY = 3

class Move(object):
    def __init__(self, position, start, end, key, rule):
        self.position = position
        self.start = start
        self.end = end
        self.key = key
        self.rule = rule

class Action(Move):
    def __init__(self, move, card):
        self.move = move
        self.card = card

    def is_valid(self):
        """
        A move from start collection to end is valid if:

        1.) The start collection has the card, and the end doesn't
        2.) The owner of the start collection is moving the card
            to a collection available to them (that they own, or
            is a table collection AKA no owner)
        3.) The move satisfies the rule
        """
        can_move = self.move.start.contains(self.card)
        should_move = self.move.rule(self.move, self.card)

        return can_move and should_move


    def execute(self):
        if not self.is_valid():
            raise ValidationException

        try:
            self.move.start.remove(self.card)
        except IndexError:
            raise ValidationException

        self.move.end.add(self.card)

