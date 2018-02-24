from utils.validation import validate
from utils.validation import Validator

class Game(Validator):
    def __init__(self):
        super().__init__(self)
        self.table = Table()
        self.players = []

    @validate
    def add_player(self, player):
        self.players.append(player)

    def start(start):
        self.enable_validation()
        # TODO: enable validation of the rest of the objects
        # TODO: start running game
