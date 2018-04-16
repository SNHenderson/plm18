from utils.getch import getch
from models.deck import Deck

class Game(object):
    def __init__(self, game_name, turn_based):
        super().__init__()
        self.game_name = game_name
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

    def current_player(self):
        return self.players[self.turn]

    def valid_turn(self, move):
        return move.start.owner is self.current_player() or move.end.owner is self.current_player()

    def replenish(self, dest, source, count):
        if count == "many":
            count = source.size() - 1
        elif count == "full":
            count = source.size()
        dest.replenish(source, count)

    def shuffle(self, collection):
        collection.shuffle()