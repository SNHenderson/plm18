from utils.validation import Validatable
from utils.validation import validate
from utils.validation import ValidationException
from utils.getch import getch
from models.moves import Action
from models.moves import Positions

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
            if self.game.win():
                self.game_running = False
                self.view.render(self.game)
                self.view.end_game(self.game)

    def get_input(self):
        moves = []

        # Wait for input until a key that corresponds to an actual move is pressed
        while not moves:
            ch = getch()

            # Exit the game on ESC
            if ord(ch) == 27:
                self.view.end_game(self.game)
                self.game_running = False;
                break

            moves = [ move for move in self.game.moves if move.key == ch ]

        return moves

    def get_action(self, move):
        if move.position is Positions.ANY:
            try:
                value = input("Enter card index: ")
                index = int(value) - 1
                if index < 0:
                    raise ValidationException
            except (ValueError, EOFError, KeyboardInterrupt):
                raise ValidationException
        elif move.position is Positions.FIRST:
            index = 0
        elif move.position is Positions.LAST:
            index = -1

        if not move.start or len(move.start) <= index:
            raise ValidationException

        return Action(move, move.start[index])

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
                        self.get_action(move).execute()
                        self.view.move_card(self.game)
                    has_moved = True
                except ValidationException:
                    self.view.invalid_move(self.game)

            self.game.update_turn()

        else:
            try:
                [ self.get_action(move).execute() for move in self.get_input() ]
            except ValidationException as e:
                self.view.invalid_move(self.game)

        # Check and run any events:
        [ event.run() for event in self.game.events ]

