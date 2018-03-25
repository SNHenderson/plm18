import os

class BaseView():
    def __init__(self):
        pass

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

