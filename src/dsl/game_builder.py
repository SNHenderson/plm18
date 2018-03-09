from obj.game import Game
from obj.pile import Pile
from obj.player import Player
from obj.rank import Rank
from obj.hand import Hand

def build_game(game_rules):
    game = Game()
    
    # TODO: Configure game based on the abstract game definition

    return game

def build_bartok(game_rules):
    game = Game(True)
    game.restrict(lambda self: len(self.collections) == 4)

    # Game ends when either player runs out of cards
    game.add_win_condition(lambda self: any([ sum([len(c.cards) for c in game.collections_for(p)]) == 0 for p in self.players ]))

    # Players
    p1 = Player("Player1")
    p2 = Player("Player2")

    for p in [p1, p2]:
        p.restrict(lambda self: len(self.collections) == 1)
        p.hand.restrict(lambda self: len(self.hand) <= 5)

    game.add_player(p1)
    game.add_player(p2)

    # Draw and discard piles
    draw = Pile(name="d", facedown = True)

    discard = Pile("discard", facedown = False)

    cards = game.deck.shuffled()
    collections = [p1.hand, p2.hand, draw, discard]
    counts = [5, 5, 41, 1]

    # Register collections with the game
    [ game.add_collection(c) for c in collections ]

    # Add moves for player one playing a card on the first pile - playing a card auto-draws
    game.add_move(0, p1.hand, discard, "q")
    game.add_move(1, p1.hand, discard, "w")
    game.add_move(2, p1.hand, discard, "e")
    game.add_move(3, p1.hand, discard, "r")
    game.add_move(4, p1.hand, discard, "t")

    # Add move for player one drawing a card
    game.add_move(-1, draw, p1.hand, "a")

    # Add moves for player two playing a card on the first pile - playing a card auto-draws
    game.add_move(0, p2.hand, discard, "y")
    game.add_move(1, p2.hand, discard, "u")
    game.add_move(2, p2.hand, discard, "i")
    game.add_move(3, p2.hand, discard, "o")
    game.add_move(4, p2.hand, discard, "p")

    # Add move for player one drawing a card
    game.add_move(-1, draw, p2.hand, "h")

    # Distribute cards to the game's collections
    for (collection, count) in zip(collections, counts):
        for _ in range(count):
            collection.add(cards.pop(0))
    assert len(cards) == 0

    return game

# TODO: Remove this once we get the DSL working
def build_speed(game_rules):
    game = Game()

    # There are only 2 players, and 8 total collections in game
    game.restrict(lambda self: len(self.players) == 2)
    game.restrict(lambda self: len(self.collections) == 8)

    # Game ends when either player runs out of cards
    game.add_win_condition(lambda self: any([ sum([len(c.cards) for c in game.collections_for(p)]) == 0 for p in self.players ]))

    # Players
    p1 = Player("Player1")
    p2 = Player("Player2")

    # Each player owns 3 collections, and their hand can have at most 5 cards
    for p in [p1, p2]:
        p.restrict(lambda self: len(self.collections) == 3)
        p.hand.restrict(lambda self: len(self.hand) <= 5)

    p1.add_collection(p1.hand)
    p2.add_collection(p2.hand)   

    game.add_player(p1)
    game.add_player(p2)

    # Draw, replacement and discard piles
    draw1 = Pile(name="d1", facedown=True)
    draw2 = Pile(name="d2", facedown=True)
    p1.add_collection(draw1)
    p2.add_collection(draw2)

    # Replace piles; used when neither player has a playable card in their hand
    replace1 = Pile(name="r1", facedown=True)
    replace2 = Pile(name="r2", facedown=True)

    # Discard piles; used by either player to discard a card from their hand
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

    def appropriate_rank(top_card_rank, played_card_rank):
        """ Verifies that the card to be played is of 1 rank higher or
            1 rank lower than the top-most card. Allows a KING to be played
            on ACE, and for ACE to be played on KING (wrap-around behavior)
        """
        return played_card_rank == (top_card_rank + 1) or \
                 top_card_rank == 1 and played_card_rank == 13 or \
                 top_card_rank == 13 and played_card_rank == 1 or \
                 played_card_rank == (top_card_rank - 1)


    def has_valid_move(pile, hand):
        """ Returns true if any card in hand can be discarded onto pile
        """
        top_card = pile[-1]
        return any([appropriate_rank(Rank[top_card.rank].value, Rank[h.rank].value) for h in hand])

    def valid_replacement():
        """ Returns true if neither player has a card in hand that can be discarded
            into either discard pile
        """
        return not(has_valid_move(discard1, p1.hand) or 
                   has_valid_move(discard2, p1.hand) or
                   has_valid_move(discard1, p2.hand) or
                   has_valid_move(discard2, p2.hand)) or \
                   replace1.size() != replace2.size()

    def replenish_replace():
        """ Replenishes the replace piles by taking the bottom `size` cards from discard1 and discard2
        """
        size = counts[collections.index("replace1")]
        replace1 = [discard1.cards[k] for k in range(size)]
        replace2 = [discard2.cards[k] for k in range(size)]

    def valid_play(move):
        """ Determines if the given move is 'allowed'

         - For discarding a card from a players hand, this verifies the rank 
           is of appropriate value (see appropriate_rank())

         - For drawing from the replacement piles, this verifies that neither player
           can make a valid move (see valid_replacement() and has_valid_move()). This also 
           handles replenshing the replacement piles (by taking from bottom of discard piles)

         Always ensures that the move is a "valid move" in the universal sense, see
         game.valid_move()

         NOTE: This is hacky b/c currently, discarding a card and drawing from their draw
         pile is tied together (autodraw). Drawing from a draw pile is automatically valid
         as long as they are playing a card, so if the end collection of a card is the player's
         hand, it's assumed to be a drawing move.
        """
        is_replacement = move.start == replace1 or move.start == replace2
        if is_replacement:
            print("Attempt to draw from the replacement piles")

            # Replenish the replace piles if they're depleted
            if replace1.size() == 0:
                replenish_replace()

            return valid_replacement()

        try:
            played_card = move.start[move.card]
            played_card_rank = Rank[played_card.rank].value
            print("Player is attempting to play card (from %s) of rank %d " % (move.start.name, played_card_rank))

            top_card = move.end[-1]
            top_card_rank = Rank[top_card.rank].value
            print("Top card of selected pile (%s) has rank %d " % (move.end.name, top_card_rank))

            correct_rank = appropriate_rank(top_card_rank, played_card_rank)

            is_valid = game.valid_move(played_card, move.start, move.end)

            # The isinstance(move.end, Hand) checks if this is a drawing move => automatically valid
            return is_valid and (isinstance(move.end, Hand) or correct_rank)
        
        # This is used to handle the case when a players draw pile is empty
        except IndexError:
            return False

    # Register the set of rules associated with moving a card w. the game
    game.add_rule("move_card", valid_play)


    # Distribute cards to the game's collections
    for (collection, count) in zip(collections, counts):
        for _ in range(count):
            collection.add(cards.pop(0))
    assert len(cards) == 0

    return game