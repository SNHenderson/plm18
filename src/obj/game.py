from utils.validation import validate
from utils.validation import Validatable

from obj.deck import Deck
from obj.pile import Pile

class Game(Validatable):
    def __init__(self):
        super().__init__()
        self.players = []
        self.is_running = False
        self.win_conditions = []
        self.collections = set()
        self.deck = Deck()

        self.restrict(lambda self: self.deck.is_partitioned_by(self.collections))

    @validate()
    def add_collection(self, collection):
        self.collections.add(collection)

    @validate()
    def add_player(self, player):
        self.players.append(player)

    def collections_for(self, player):
        return [ c for c in self.collections if player.owns(c) ]

    def add_win_condition(self, condition):
        self.win_conditions.append(condition)

    def run(self):
        self.enable_validation()
        game_running = True
        while game_running:
            self.render()
            self.update_game()
            game_running = all([c(self) for c in self.win_conditions])

            game_running = False # TODO: remove

    def render(self):
        # Render: need some abstract way to configure the layout of the game
        other_collections = { c for c in self.collections if isinstance(c, Pile) }
        print("Table:")
        for c in other_collections:
            print(c)
        print()

        print("Players:")
        for p in self.players:
            print(p.name, p.hand)
        print()

    @validate()
    def update_game(self):
        # TODO:
        # get player inputs
        # perform actions
        pass

    def move_card(card, start, end):
        pass