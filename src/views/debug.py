from models.pile import Pile
from utils.logger import Logger
from views.base import BaseView

class DebugView(BaseView):

    def start_game(self, model):
            self.clear_screen()
            self.display("Starting new game of %s!" % model.name)
            self.display()

    def render(self, model):
        self.display()
        # Render: need some abstract way to configure the layout of the game
        other_collections = { c for c in model.collections if isinstance(c, Pile) }
        self.display("Table:")
        for c in other_collections:
            self.display(c)
        self.display()

        self.display("Players:")
        for p in model.players:
            self.display(p.name, p.hand)
        self.display()

    def move_card(self, model):
        self.display("Moved the card!")

    def invalid_move(self, model):
        self.display("Move was invalid!")

    def display_turn(self, model):
        self.display(model.current_player().name + "'s turn:")

    def end_game(self, model):
            self.display("Game end!")
