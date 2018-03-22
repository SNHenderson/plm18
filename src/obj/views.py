from utils.logger import Logger
from obj.pile import Pile
import os

class log_view():
    def __init__(self, file_name = "logs/log.txt"):
        self.log = Logger(file_name)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def start_game(self, model):
            self.clear_screen()
            self.log.print("Starting new game of %s!" % model.name)
            self.log.print()

    def render(self, model):
        self.clear_screen()
        # Render: need some abstract way to configure the layout of the game
        other_collections = { c for c in model.collections if isinstance(c, Pile) }
        self.log.print("Table:")
        for c in other_collections:
            self.log.print(c)
        self.log.print()

        self.log.print("Players:")
        for p in model.players:
            self.log.print(p.name, p.hand)
        self.log.print()

    def move_card(self, model):
        self.log.print("Moved the card!")

    def invalid_move(self, model):
        self.log.print("Move was invalid!")

    def display_turn(self, model):
        current_player = model.players[model.turn]
        self.log.print(current_player.name + "'s turn:")    

    def end_game(self, model):
            self.log.print("Game end!")

class view():
    def __init__(self):
        pass

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def start_game(self, model):
            self.print("Starting new game of %s!" % model.name)
            self.print()

    def render(self, model):
        self.clear_screen()
        # Render: need some abstract way to configure the layout of the game
        other_collections = { c for c in model.collections if isinstance(c, Pile) }
        self.print("Table:")
        for c in other_collections:
            self.print(c)
        self.print()

        self.print("Players:")
        for p in model.players:
            self.print(p.name, p.hand)
        self.print()

    def move_card(self, model):
        self.print("Moved the card!")

    def invalid_move(self, model):
        self.print("Move was invalid!")

    def display_turn(self, model):
        current_player = model.players[model.turn]
        self.print(current_player.name + "'s turn:")    

    def end_game(self, model):
            self.print("Game end!")