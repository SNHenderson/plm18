from models.pile import Pile
from views.base import BaseView

class View(BaseView):
    def start_game(self, model):
        print("Starting new game of %s!" % model.name)
        print()

    def render(self, model):
        self.clear_screen()
        # Render: need some abstract way to configure the layout of the game
        other_collections = { c for c in model.collections if isinstance(c, Pile) }
        print("Table:")
        for c in other_collections:
            print(c)
        print()

        print("Players:")
        for p in model.players:
            print(p.name, p.hand)
        print()

    def move_card(self, model):
        print("Moved the card!")

    def invalid_move(self, model):
        print("Move was invalid!")

    def display_turn(self, model):
        current_player = model.players[model.turn]
        print(current_player.name + "'s turn:")

    def end_game(self, model):
            print("Game end!")

