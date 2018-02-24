from utils.validation import validate
from utils.validation import Validatable
from obj.hand import Hand

class Player(Validatable):
    def __init__(self, name):
        super().__init__(self)
        self.hand = Hand()
        self.name = name

