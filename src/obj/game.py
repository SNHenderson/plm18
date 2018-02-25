from utils.validation import validate
from utils.validation import Validatable

from obj.table import Table
from obj.deck import Deck

class Game(Validatable):
    def __init__(self):
        super().__init__()
        self.players = []
        self.is_running = False
        self.win_conditions = []
        self.collections = set()
        self.table = Table()
        self.deck = Deck()

        self.restrict(lambda self: self.deck.is_partitioned_by(self.collections))

    @validate()
    def add_collection(self, collection):
        self.collections.add(collection)

    @validate()
    def add_player(self, player):
        self.players.append(player)

    def collections_for(player):
        return [ c for c in self.collections if player.owns(c) ]

    def add_win_condition(self, condition):
        self.win_conditions.append(condition)

    def run(start):
        self.enable_validation()
        game_running = True
        while game_running:
            self.update_game()
            game_running = all([c() for c in self.win_conditions()])

    @validate()
    def update_game():
        # TODO:
        # render game
        # get player inputs
        # perform actions
        pass

    def move_card(card, start, end):
        pass