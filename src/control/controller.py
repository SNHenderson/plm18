from utils.validation import Validatable
from utils.validation import validate
from utils.validation import ValidationException

from utils.getch import getch
from utils.objs import dict_obj
from utils.logger import Logger

from models.deck import Deck
from models.pile import Pile
from models.game import Game

class Controller(Validatable):
    def __init__(self, game, view):
        super().__init__()
        self.game = game
        self.view = view
        self.game_running = False

    def run(self):
        self.view.start_game(self.game)
        self.enable_validation()
        self.game_running = True
        if self.game.turn_based:
            self.game.turn = 0
        while self.game_running:
            self.view.render(self.game)
            self.update_game()
            if(self.game.win()):
                self.game_running = False
                self.view.render(self.game)
                self.view.end_game(self.game)

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
                self.view.end_game(self.game)
                self.game_running = False;
                break

            moves = [ copy_move(move) for move in self.game.moves if move.input == ch ]

        return moves

    def init_and_move(self, move):
        if move.card is None:
            try:
                value = input("Enter card index: ")
                move.card = int(value) - 1
            except (ValueError, EOFError, KeyboardInterrupt):
                raise ValidationException

            try:
                self.game.move_card(move)
            except ValidationException:
                move.card = None
                raise

            move.card = value
        else:
            self.game.move_card(move)
            self.view.move_card(self.game)

    @validate()
    def update_game(self):
        if self.game.turn_based:
            # Prompt for a valid move from the player so they can complete their turn
            has_moved = False
            while not has_moved:
                self.view.display_turn(self.game)
                try:
                    for move in self.get_input():
                        # If player's input corresponds to a move for the other player, don't allow it
                        if self.game.valid_turn(move):
                            raise ValidationException
                        self.init_and_move(move)
                    has_moved = True
                except ValidationException:
                    self.view.invalid_move(self.game)

            self.game.update_turn()

        else:
            try:
                [ self.init_and_move(move) for move in self.get_input() ]
            except ValidationException as e:
                self.view.invalid_move(self.game)
