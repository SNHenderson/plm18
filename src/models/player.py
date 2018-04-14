from models.hand import Hand

class Player(object):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.hand = Hand(name=name + "'s hand")
        self.collections = { self.hand }

    def add_collection(self, collection):
        self.collections.add(collection)
        collection.set_owner(self)

    def owns(self, collection):
        return collection in self.collections

    def __repr__(self):
        return "<%s:%s>" % (self.name, self.hand)
