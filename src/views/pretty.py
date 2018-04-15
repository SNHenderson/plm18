from models.pile import Pile
from utils import card_display
from views.base import BaseView
import time

class PrettyView(BaseView):
    def start_game(self, model):
            self.display("Starting new game of %s!" % model.name)
            self.display()

    def render(self, model):
        self.clear_screen()
        # Render: need some abstract way to configure the layout of the game
        other_collections = { c for c in model.collections if isinstance(c, Pile) }
        self.display("Table:")
        facedowns = []
        faceups = []
        for c in other_collections:
            if c.facedown:
                facedowns.append("%s(%d): \n%s" % (c.name, len(c.cards), card_display.ascii_version_of_hidden_card()))
            else:
                faceups.append("%s(%d): \n%s" % (c.name, len(c.cards), card_display.ascii_version_of_card(c.top_card())))
        self.display(card_display.join_lines(sorted(facedowns)))
        self.display(card_display.join_lines(sorted(faceups)))
        self.display()

        self.display("Players:")
        if model.turn_based:
            p = model.players[model.turn]
            self.display("%s:\n%s" % (p.hand.name, card_display.ascii_version_of_card(*p.hand.cards)))
        else:
            for p in model.players:
                self.display("%s:\n%s" % (p.hand.name, card_display.ascii_version_of_card(*p.hand.cards)))
        self.display()

    def move_card(self, model):
        self.render(model)
        self.display("Moved the card!")
        time.sleep(1)

    def invalid_move(self, model):
        self.display("Move was invalid!")

    def display_turn(self, model):
        current_player = model.players[model.turn]
        self.display(current_player.name + "'s turn:")

    def end_game(self, model):
        self.display("Game end!")
