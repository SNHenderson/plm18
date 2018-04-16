from models.pile import Pile
from utils import card_display
from views.base import BaseView
import time

class PrettyView(BaseView):
    def start_game(self, model):
            self.display("Starting new game of %s!" % model.game_name)
            self.display()

    def render(self, model):
        self.clear_screen()
        # Render: need some abstract way to configure the layout of the game
        other_collections = { c for c in model.collections if isinstance(c, Pile) }
        self.display("Table:")
        facedowns = []
        faceups = []
        for c in other_collections:
            if c.size() > 0:
                if c.facedown:
                    facedowns.append("%s(%d): \n%s" % (c.name, len(c.cards), card_display.ascii_version_of_hidden_card()))
                else:
                    faceups.append("%s(%d): \n%s" % (c.name, len(c.cards), card_display.ascii_version_of_card(c.top_card())))
        self.display(card_display.join_lines(sorted(facedowns)))
        self.display(card_display.join_lines(sorted(faceups)))
        self.display()

        self.display("Players:")
        if model.turn_based:
            p = model.current_player()
            if p.hand.size() > 0:
                self.display("%s:\n%s" % (p.hand.name, card_display.ascii_version_of_card(*p.hand.cards)))
        else:
            for p in model.players:
                if p.hand.size() > 0:
                    self.display("%s:\n%s" % (p.hand.name, card_display.ascii_version_of_card(*p.hand.cards)))
        self.display()

    def move_card(self, model):
        self.render(model)
        time.sleep(0.5)

    def invalid_move(self, model):
        self.display("Move was invalid!")

    def display_turn(self, model):
        self.display(model.current_player().name + "'s turn:")

    def end_game(self, model):
        if model.turn_based:
            for p in model.players:
                    if p.hand.size() > 0:
                        self.display("%s:\n%s" % (p.hand.name, card_display.ascii_version_of_card(*p.hand.cards)))
        self.display("Game end!")
