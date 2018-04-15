import os
from utils.logger import Logger

class BaseView():
    def __init__(self, log_file = None):
        if log_file:
            self.logger = Logger(os.path.join("logs", log_file))
            self.log = self.logger.log
        else:
            self.log = None

    def display(self, *args):
        print(*args)
        if self.log:
            self.log(*args)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

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

