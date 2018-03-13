from obj.game import Game
from obj.pile import Pile
from obj.player import Player
from obj.rank import Rank
from obj.suit import Suit
from obj.hand import Hand

from random import shuffle

def build_game(game_rules):
    game = Game("Sample", false)

    # TODO: Configure game based on the abstract game definition

    return game

def build_bartok(game_rules):
    game = Game("Bartok", turn_based=True)
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
    p1.add_collection(p1.hand)
    p2.add_collection(p2.hand)

    # Draw and discard piles
    draw = Pile(name="draw", facedown = True)
    discard = Pile("discard", facedown = False)

    cards = game.deck.shuffled()
    collections = [p1.hand, p2.hand, draw, discard]
    counts = [5, 5, 41, 1]

    # Register collections with the game
    [ game.add_collection(c) for c in collections ]

    def replenish_draw(draw):
        """ Takes all the cards but the top one from the discard pile, shuffles them, and replenishes the
        draw pile with this set of cards
        """
        draw.cards = discard[:-1]
        shuffle(draw.cards)
        del discard[:-1]

    def appropriate_card(top_card, played_card):
        """ Verifies that the card to be played is of same rank or suit as top_card
        """
        return Rank[top_card.rank].value == Rank[played_card.rank].value or \
               Suit[top_card.suit].value == Suit[played_card.suit].value


    def has_valid_move(pile, hand):
        """ Returns true if any card in hand can be discarded onto pile
        """
        top_card = pile[-1]
        return any([appropriate_card(top_card, h) for h in hand])

    def valid_draw(move):
        # Replenish the draw pile if empty
        if draw.size() == 0:
            if discard.size() < 2:
                return False

            replenish_draw(move.start)

        # return not has_valid_move(discard, move.end)
        return True

    def valid_discard(move):
        try:
            return game.valid_move(move.start[move.card], move.start, move.end) and \
                   appropriate_card(discard[-1], move.start[move.card])

        # Handle attempts to play a card not currently in hand
        except IndexError:
            return False

    # Add moves for player one playing a card on the first pile
    game.add_move(None, p1.hand, discard, "q", valid_discard)

    # Add move for player one drawing a card
    game.add_move(-1, draw, p1.hand, "e", valid_draw)

    # Add moves for player two playing a card on the first pile
    game.add_move(None, p2.hand, discard, "i", valid_discard)

    # Add move for player two drawing a card
    game.add_move(-1, draw, p2.hand, "p", valid_draw)

    # Distribute cards to the game's collections
    for (collection, count) in zip(collections, counts):
        for _ in range(count):
            collection.add(cards.pop(0))
    assert len(cards) == 0

    return game

# TODO: Remove this once we get the DSL working
def build_speed(game_rules):
    game = Game("Speed", turn_based=False)

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
    draw1 = Pile(name="draw1", facedown=True)
    draw2 = Pile(name="draw2", facedown=True)
    p1.add_collection(draw1)
    p2.add_collection(draw2)

    # Replace piles; used when neither player has a playable card in their hand
    replace1 = Pile(name="replace1", facedown=True)
    replace2 = Pile(name="replace2", facedown=True)

    # Discard piles; used by either player to discard a card from their hand
    discard1 = Pile(name="discard1", facedown=False)
    discard2 = Pile(name="discard2", facedown=False)

    cards = game.deck.shuffled()
    collections = [p1.hand, p2.hand, draw1, draw2, discard1, discard2, replace1, replace2]
    counts = [5, 5, 15, 15, 1, 1, 5, 5]

    # Register collections with the game
    [ game.add_collection(c) for c in collections ]

    def appropriate_rank(top_card_rank, played_card_rank):
        """ Verifies that the card to be played is of 1 rank higher or
            1 rank lower than the top-most card. Allows a KING to be played
            on ACE, and for ACE to be played on KING (wrap-around behavior)
        """
        return played_card_rank == (top_card_rank + 1) or \
                 top_card_rank == 1 and played_card_rank == 13 or \
                 top_card_rank == 13 and played_card_rank == 1 or \
                 played_card_rank == (top_card_rank - 1)


    def has_valid_move(pile, person):
        """ Returns true if any card in hand can be discarded onto pile
        """
        top_card = pile[-1]
        return any([appropriate_rank(Rank[top_card.rank].value, Rank[h.rank].value) for h in person.hand])

    def valid_replacement(move):
        print("Attempt to draw from the replacement piles")

        # Replenish the replace piles if they're depleted
        if replace1.size() == 0:
            replenish_replace()

        """ Returns true if neither player has a card in hand that can be discarded
            into either discard pile
        """
        return all([not has_valid_move(d, p) for d in [discard1, discard2] for p in [p1, p2]])

    def replenish_replace():
        """ Replenishes the replace piles by taking the bottom 5 cards from discard1 and discard2
        """
        replace1.cards += discard1[:5]
        replace2.cards += discard2[:5]
        del discard1[:5]
        del discard2[:5]

    def valid_draw(move):
        try:
            played_card = move.start[move.card]
            is_valid = game.valid_move(played_card, move.start, move.end)

            return move.end.size() < 5

        # This is used to handle the case when a player's draw pile is empty
        except IndexError:
            return False

    def valid_discard(move):
        try:
            played_card = move.start[move.card]
            played_card_rank = Rank[played_card.rank].value
            print("Player is attempting to play card (from %s) of rank %d " % (move.start.name, played_card_rank))

            top_card = move.end[-1]
            top_card_rank = Rank[top_card.rank].value
            print("Top card of selected pile (%s) has rank %d " % (move.end.name, top_card_rank))

            correct_rank = appropriate_rank(top_card_rank, played_card_rank)

            is_valid = game.valid_move(played_card, move.start, move.end)

            return is_valid and correct_rank
        # This is used to handle the case when a player's hand is empty
        except IndexError:
            return False


    # Add move for player one playing a card on the first pile
    game.add_move(None, p1.hand, discard1, "q", valid_discard)

    # Add move for player one playing a card on the second pile
    game.add_move(None, p1.hand, discard2, "w", valid_discard)

    # Add move for player one drawing a card
    game.add_move(-1, draw1, p1.hand, "e", valid_draw)

    # Add moves for player two playing a card on the first pile
    game.add_move(None, p2.hand, discard1, "i", valid_discard)

    # Add moves for player two playing a card on the second pile
    game.add_move(None, p2.hand, discard2, "o", valid_discard)

    # Add move for player one drawing a card
    game.add_move(-1, draw2, p2.hand, "p", valid_draw)

    # Add moves for using the replacement piles
    game.add_move(-1, replace1, discard1, "b", valid_replacement)
    game.add_move(-1, replace2, discard2, "b", valid_replacement)

    # Distribute cards to the game's collections
    for (collection, count) in zip(collections, counts):
        for _ in range(count):
            collection.add(cards.pop(0))
    assert len(cards) == 0

    return game
