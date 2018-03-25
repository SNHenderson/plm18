from utils.validation import Validatable
from utils.validation import validate
from utils.validation import ValidationException

from utils.getch import getch
from utils.objs import dict_obj
from utils.logger import Logger

from obj.deck import Deck
from obj.pile import Pile

class Game(Validatable):
    def __init__(self, name, turn_based):
        super().__init__()
        self.name = name
        self.players = []
        self.win_conditions = []
        self.moves = []
        self.collections = set()
        self.deck = Deck()
        self.turn_based = turn_based
        if turn_based:
            self.turn = 0
        else:
            self.turn = -1

        self.restrict(lambda self: self.deck.is_partitioned_by(self.collections))

    @validate()
    def add_collection(self, collection):
        self.collections.add(collection)

    @validate()
    def add_player(self, player):
        self.players.append(player)

    @validate()
    def add_move(self, card, start, end, inp, rule):
        self.moves.append(dict_obj(card = card, start = start, end = end, input = inp, rule = rule))

    def collections_for(self, player):
        return [ c for c in self.collections if player.owns(c) ]

    def add_win_condition(self, condition):
        self.win_conditions.append(condition)

    def win(self):
        return all([c(self) for c in self.win_conditions])

    def update_turn(self):
        self.turn = (self.turn + 1) % len(self.players)

    def valid_turn(self, move):
        current_player = self.players[self.turn]
        return move.start.owner != current_player and move.end.owner != current_player

    def move_card(self, move):
        allowed = move.rule(move)
        if not allowed:
            raise ValidationException

        card = move.start[move.card]
        try:
            move.start.remove(card)
        except IndexError:
            raise ValidationException
        move.end.add(card)

    def valid_move(self, card, start, end):
        """ Universal defn. of a valid card transfer from 1 collection
            to another

        A move from start collection to end is valid if:

        1.) The start collection has the card, and the end doesn't
        2.) The owner of the start collection is moving the card
            to a collection available to them (that they own, or
            is a table collection AKA no owner)
        """
        card_in_start = start.contains_card(card)
        card_in_end = end.contains_card(card)
        return card_in_start and (not card_in_end) and (end.owner == None or end.owner == start.owner)
