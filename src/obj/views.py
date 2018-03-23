from utils.logger import Logger
from obj.pile import Pile
import utils.card_display as card_display
import os, sys, codecs

class base_view():
    def __init__(self):
        pass

    def start_game(self, model):
        raise NotImplementedError()

    def render(self, model):
        raise NotImplementedError()

    def move_card(self, model):
        raise NotImplementedError()

    def invalid_move(self, model):
        raise NotImplementedError()

    def display_turn(self, model):
        raise NotImplementedError()

    def end_game(self, model):
        raise NotImplementedError()        

class log_view(base_view):
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

class view(base_view):
    def __init__(self):
        pass
        #sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

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

class pretty_view(base_view):
    def __init__(self):
        pass
        #sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

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