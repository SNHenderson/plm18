from models.pile import Pile
from utils import card_display
from views.base import BaseView

class PrettyView(BaseView):
    def start_game(self, model):
            print("Starting new game of %s!" % model.name)
            print()

    def render(self, model):
        self.clear_screen()
        # Render: need some abstract way to configure the layout of the game
        other_collections = { c for c in model.collections if isinstance(c, Pile) }
        print("Table:")
        facedowns = []
        faceups = []
        for c in other_collections:
            if c.facedown:
                facedowns.append("%s(%d): \n%s" % (c.name, len(c.cards), card_display.ascii_version_of_hidden_card()))
            else:
                faceups.append("%s(%d): \n%s" % (c.name, len(c.cards), card_display.ascii_version_of_card(c.top_card())))
        print(card_display.join_lines(sorted(facedowns)))
        print(card_display.join_lines(sorted(faceups)))
        print()

        print("Players:")
        for p in model.players:
            print("%s:\n%s" % (p.hand.name, card_display.ascii_version_of_card(*p.hand.cards)))
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
