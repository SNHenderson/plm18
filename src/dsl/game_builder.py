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

    # Game ends when either player runs out of cards
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

    discard1 = Pile(name="discard1", facedown=False)
    discard2 = Pile(name="discard2", facedown=False)

    cards = game.deck.shuffled()
    collections = [p1.hand, p2.hand, draw1, draw2, discard1, discard2, replace1, replace2]
    counts = [5, 5, 15, 15, 1, 1, 5, 5]

    # Register collections with the game
    [ game.add_collection(c) for c in collections ]

    # Add moves for player one playing a card on the first pile - playing a card auto-draws
    game.add_move(0, p1.hand, discard1, "q")
    game.add_move(1, p1.hand, discard1, "w")
    game.add_move(2, p1.hand, discard1, "e")
    game.add_move(3, p1.hand, discard1, "r")
    game.add_move(4, p1.hand, discard1, "t")

    # Add moves for player one playing a card on the second pile - playing a card auto-draws
    game.add_move(0, p1.hand, discard2, "a")
    game.add_move(1, p1.hand, discard2, "s")
    game.add_move(2, p1.hand, discard2, "d")
    game.add_move(3, p1.hand, discard2, "f")
    game.add_move(4, p1.hand, discard2, "g")

    # Add move for player one drawing a card
    game.add_move(-1, draw1, p1.hand, "z")

    # Add moves for player two playing a card on the first pile - playing a card auto-draws
    game.add_move(0, p2.hand, discard1, "y")
    game.add_move(1, p2.hand, discard1, "u")
    game.add_move(2, p2.hand, discard1, "i")
    game.add_move(3, p2.hand, discard1, "o")
    game.add_move(4, p2.hand, discard1, "p")

    # Add moves for player two playing a card on the second pile - playing a card auto-draws
    game.add_move(0, p2.hand, discard2, "h")
    game.add_move(1, p2.hand, discard2, "j")
    game.add_move(2, p2.hand, discard2, "k")
    game.add_move(3, p2.hand, discard2, "l")
    game.add_move(4, p2.hand, discard2, ";")

    # Add move for player one drawing a card
    game.add_move(-1, draw2, p2.hand, "n")

    # Add moves for using the replacement piles
    game.add_move(-1, replace1, discard1, "b")
    game.add_move(-1, replace2, discard2, "b")

    # Distribute cards to the game's collections
    for (collection, count) in zip(collections, counts):
        for _ in range(count):
            collection.add(cards.pop(0))
    assert len(cards) == 0

    return game