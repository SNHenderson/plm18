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

    def valid_move(card, start, end):
        """ Verifies whether a move is valid. 

        A move from start collection to end is valid if:

        1.) The start collection has the card, and the end doesn't
        2.) The owner of the start collection is moving the card 
            to a collection available to them (that they own, or 
            is a table collection AKA no owner)
        """
        card_in_start = start.contains_card(card)
        card_in_end = end.contains_card(card)
        return card_in_start and not(card_in_end) and (end.owner == None or end.owner == start.owner)

    def move_card(card, start, end):
        """ Move a card from the start collection to end collection
        """
        if valid_move(card, start, end):
            start.remove(card)
            end.add(card)
