import os

from models.pile import Pile
from utils.logger import Logger
from views.base import BaseView

class LogView(BaseView):
    def __init__(self, file_name):
        self.logger = Logger(os.path.join("logs", file_name))
        self.log = self.logger.log

    def start_game(self, model):
            self.clear_screen()
            self.log("Starting new game of %s!" % model.name)
            self.log()

    def render(self, model):
        self.clear_screen()
        # Render: need some abstract way to configure the layout of the game
        other_collections = { c for c in model.collections if isinstance(c, Pile) }
        self.log("Table:")
        for c in other_collections:
            self.log(c)
        self.log()

        self.log("Players:")
        for p in model.players:
            self.log(p.name, p.hand)
        self.log()

    def move_card(self, model):
        self.log("Moved the card!")

    def invalid_move(self, model):
        self.log("Move was invalid!")

    def display_turn(self, model):
        current_player = model.players[model.turn]
        self.log(current_player.name + "'s turn:")

    def end_game(self, model):
            self.log("Game end!")
            self.logger.close()
