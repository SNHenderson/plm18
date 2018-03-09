from utils.validation import *

from utils.getch import getch
from utils.objs import dict_obj
from utils.logger import Logger

from obj.deck import Deck
from obj.pile import Pile


class Game(Validatable):
    def __init__(self, turn_based = False, file_name = "logs/log.txt"):
        super().__init__()
        self.players = []
        self.is_running = False
        self.win_conditions = []
        self.moves = []
        self.collections = set()
        self.deck = Deck()
        self.turn_based = turn_based
        self.game_running = False
        self.log = Logger(file_name)
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
    def add_move(self, card, start, end, inp):
        self.moves.append(dict_obj(card = card, start = start, end = end, input = inp))

    def collections_for(self, player):
        return [ c for c in self.collections if player.owns(c) ]

    def add_win_condition(self, condition):
        self.win_conditions.append(condition)

    def run(self):
        self.enable_validation()
        self.game_running = True
        if self.turn_based:
            self.turn = 0
        while self.game_running:
            self.render()
            self.update_game()
            if all([c(self) for c in self.win_conditions]):
                self.game_running = False;
                self.render()
                self.log.print("Game end!")
        self.log.close()

    def render(self):
        # Render: need some abstract way to configure the layout of the game
        other_collections = { c for c in self.collections if isinstance(c, Pile) }
        self.log.print("Table:")
        for c in other_collections:
            self.log.print(c)
        self.log.print()

        self.log.print("Players:")
        for p in self.players:
            self.log.print(p.name, p.hand)
        self.log.print()

    def get_input(self):
        ch = getch()
        if ord(ch) == 27:
            self.game_running = False;

        moves = [ move for move in self.moves if move.input == ch ]

        return moves

    @checkRule()
    def move_card(self, move):
        try:
            card = move.start[move.card]
            move.start.remove(card)
            move.end.add(card)
            print("Moved the card!")
        except IndexError as e:
            pass

    @validate()
    def update_game(self):        
        if self.turn_based:
            print("Player " + self.players[self.turn].name + "'s turn:")

        # Appropriately handle any attempts to make invalid moves
        try:
            [ self.move_card(move) for move in self.get_input() ]
        except ValidationException:
            print("Move was invalid!")
        if self.turn_based:
            if self.turn + 1 >= len(self.players):
                self.turn = 0
            else:
                self.turn += 1            

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
        return card_in_start and not(card_in_end) and (end.owner == None or end.owner == start.owner)