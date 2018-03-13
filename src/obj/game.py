from utils.validation import Validatable
from utils.validation import validate
from utils.validation import ValidationException

from utils.getch import getch
from utils.objs import dict_obj
from utils.logger import Logger

from obj.deck import Deck
from obj.pile import Pile


class Game(Validatable):
    def __init__(self, name, turn_based, file_name = "logs/log.txt"):
        super().__init__()

        self.name = name
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
    def add_move(self, card, start, end, inp, rule):
        self.moves.append(dict_obj(card = card, start = start, end = end, input = inp, rule = rule))

    def collections_for(self, player):
        return [ c for c in self.collections if player.owns(c) ]

    def add_win_condition(self, condition):
        self.win_conditions.append(condition)

    def run(self):
        self.log.print("Starting new game of %s!" % self.name)
        self.log.print()

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
        def copy_move(m):
            # TODO: Get rid of this when move is a proper class
            return dict_obj(card=m.card, start=m.start, end=m.end, input=m.input, rule=m.rule)
        moves = []

        # Wait for input until a key that corresponds to an actual move is pressed
        while not moves:
            ch = getch()

            # Exit the game on ESC
            if ord(ch) == 27:
                self.log.print("Exiting game")
                self.game_running = False;
                break


            moves = [ copy_move(move) for move in self.moves if move.input == ch ]

        return moves

    def init_and_move(self, move):
        if move.card is None:
            try:
                value = input("Enter card index: ")
                move.card = int(value) - 1
            except (ValueError, EOFError):
                raise ValidationException

            try:
                self.move_card(move)
            except ValidationException:
                move.card = None
                raise

            move.card = value

        else:
            self.move_card(move)

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
        self.log.print("Moved the card!")

    @validate()
    def update_game(self):
        if self.turn_based:
            # Prompt for a valid move from the player so they can complete their turn
            has_moved = False
            while not has_moved:
                current_player = self.players[self.turn]
                self.log.print(current_player.name + "'s turn:")
                try:
                    for move in self.get_input():
                        # If player's input corresponds to a move for the other player, don't allow it
                        if move.start.owner != current_player and move.end.owner != current_player:
                            raise ValidationException
                        self.init_and_move(move)
                    has_moved = True
                except ValidationException:
                    self.log.print("Move was invalid!")

            self.turn = (self.turn + 1) % len(self.players)
        else:
            try:
                [ self.init_and_move(move) for move in self.get_input() ]
            except ValidationException as e:
                self.log.print("Move was invalid!")

        self.log.print()

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
