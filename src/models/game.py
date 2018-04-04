from utils.validation import Validatable
from utils.validation import validate
from utils.validation import ValidationException

from utils.getch import getch
from utils.logger import Logger

from models.deck import Deck
from models.pile import Pile


class Game(Validatable):
    def __init__(self, name, turn_based):
        super().__init__()
        self.name = name
        self.players = []
        self.win_conditions = []
        self.moves = []
        self.events = []
        self.collections = set()
        self.deck = Deck()
        self.turn_based = turn_based
        if turn_based:
            self.turn = 0

        self.restrict(lambda self: self.deck.is_partitioned_by(self.collections))

    @validate()
    def add_collection(self, collection):
        self.collections.add(collection)

    @validate()
    def add_player(self, player):
        self.players.append(player)

    @validate()
    def add_move(self, move):
        self.moves.append(move)

    @validate()
    def add_event(self, event):
        self.events.append(event)    

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