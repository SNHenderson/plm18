from models.collection import Collection

class Pile(Collection):

    def __init__(self, name, facedown):
        super().__init__(name)
        self.facedown = facedown

    def __str__(self):
        return self.name

    def top_card(self):
    	return self.cards[-1]