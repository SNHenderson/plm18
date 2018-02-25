from obj.game import Game
from obj.pile import Pile
from obj.player import Player

def build_game(game_rules):
    game = Game()
    
    # TODO: Configure game based on the abstract game definition

    return game


# TODO: Remove this once we get the DSL working
def build_speed(game_rules):
    game = Game()
    game.restrict(lambda self: len(self.players) == 2)
    game.restrict(lambda self: len(self.collections) == 8)

    # Game ends when ethier player runs out of cards
    game.add_win_condition(lambda self: any([ sum([len(c.cards) for c in game.collections_for(p)]) == 0 for p in self.players ]))

    p1 = Player("Player1")
    p2 = Player("Player2")

    for p in [p1, p2]:
        p.restrict(lambda self: len(self.collections) == 3)
        p.hand.restrict(lambda self: len(self.hand) <= 5)

    hands = [p1.hand]

    game.add_player(p1)
    game.add_player(p2)

    # Draw piles
    draw1 = Pile(name="d1", facedown=True)
    draw2 = Pile(name="d2", facedown=True)
    p1.add_collection(draw1)
    p2.add_collection(draw2)

    replace1 = Pile(name="r1", facedown=True)
    replace2 = Pile(name="r2", facedown=True)
    p1.add_collection(replace1)
    p2.add_collection(replace2)

    discard1 = Pile(name="discard1", facedown=True)
    discard2 = Pile(name="discard2", facedown=True)

    cards = game.deck.shuffled()
    collections = [p1.hand, p2.hand, draw1, draw2, discard1, discard2, replace1, replace2]
    counts = [5, 5, 15, 15, 1, 1, 5, 5]

    # Register collections with the game
    [ game.add_collection(c) for c in collections ]

    # Distribute cards to the game's collections
    for (collection, count) in zip(collections, counts):
        for _ in range(count):
            collection.add(cards.pop(0))
    assert len(cards) == 0


    return game