from utils.getch import getch
from models.deck import Deck

class Game(object):
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

    def add_collection(self, collection):
        self.collections.add(collection)

    def add_player(self, player):
        self.players.append(player)

    def add_move(self, move):
        self.moves.append(move)

    def add_event(self, event):
        self.events.append(event)

    def collections_for(self, player):
        return [ c for c in self.collections if player.owns(c) ]

    def add_win_condition(self, condition):
        self.win_conditions.append(condition)

    def win(self):
        return all([c() for c in self.win_conditions])

    def update_turn(self):
        self.turn = (self.turn + 1) % len(self.players)

    def valid_turn(self, move):
        current_player = self.players[self.turn]
        return move.start.owner is current_player or move.end.owner is current_player

    def replenish(self, dest, source, count):
        count = len(source) - 1 if count == "many" else count
        source.replenish(dest, count)

    def shuffle(self, collection):
        collection.shuffle()

