from models.game import Game
from models.pile import Pile
from models.player import Player
from models.rank import Rank
from models.suit import Suit
from models.hand import Hand
from models.moves import Move
from models.events import Event
from models.moves import Positions
from utils.objs import dict_obj

from random import shuffle

def build_game(gd):
    game = Game(gd.name, gd.turn_based)
    cards = game.deck.shuffled()

    # First, build the players and map the names to the instances
    namespace = {
        "first": 0,
        "last": -1,
        "any": Positions.ANY
    }

    players = []
    for p in gd.players:

        # Build the players
        players.append(Player(p['name']))
        namespace[p['name']] = players[-1]

        # Populate their hands
        size = p['hand_size']
        players[-1].hand.restrict(lambda self: len(self.hand) <= size)
        [ players[-1].hand.cards.append(cards.pop(0)) for k in range(size) ]

        # Register with the gamerank
        game.add_player(players [-1])

    print(namespace)

    # Second, build the piles and map the names to the instances
    piles = []
    for p in gd.piles:

        # Build the piles
        piles.append(Pile(p['name'], p['facedown']))
        namespace[p['name']] = piles [-1]

        # Populate them
        size = p['size']
        [ piles[-1].cards.append(cards.pop(0)) for k in range(size) ]

        # Register with the game
        game.add_collection(piles [-1])

    print(namespace)

    # At this point, all cards should be distributed
    assert len(cards) == 0

    # Third, build the rules and map the names to the instances
    rules = []

    def replace_keywords(words):
        for i in range(len(words)):
            try:
                words [i] = namespace[words [i]]
            except KeyError:
                continue
        print(words)

    def build_rule(expr):
        # Tokenize
        toks = [ e.split(".") for e in expr.split(" ") ]
        print(toks)


        # Look for back-references, replace them w. actual refs
        keywords = list(namespace.keys())
        for t in toks:
            if any([ k in t for k in keywords ]):
                replace_keywords(t)
        
        # No idea where to go from here ...
        
    # for r in gd.rules:
    #     rules.append(build_rule(r['expr']))
    #     namespace[r['name']] = rules [-1]

    return game

def build_abstract(game_data):
    namespace = {
        "first": "bottom_card",
        "last": "top_card",
        "any": Positions.ANY
    }

    game = Game(game_data.name, game_data.turn_based)
    game.restrict(lambda self: len(self.collections) == game_data.collections)

    # Game ends when either player runs out of cards
    game.add_win_condition(game_data.win_condition)

    # Players
    players = {}
    for p in game_data.players:
        player = Player(p.get('name'))
        player.restrict(lambda self: len(self.collections) == p.get('collection_count'))
        player.hand.restrict(lambda self: len(self.hand) <= p.get('hand_size'))
        player.add_collection(player.hand)
        players[p.get('name')] = player

    for name, player in players.items():
        game.add_player(player)
        namespace[player.name] = player

    # Draw and discard piles
    piles = {}
    for p in game_data.piles:
        pile = Pile(p.get('name'), p.get('facedown'))
        piles[p.get('name')] = pile


    cards = game.deck.shuffled()

    collections = []
    for name, player in players.items():
        collections.append(player.hand)

    for name, pile in piles.items():
        collections.append(pile)
        namespace[pile.name] = pile

    counts = []
    for player in game_data.players:
        counts.append(player.get('hand_size'))

    for pile in game_data.piles:
        counts.append(pile.get('size'))

    # Register collections with the game
    [ game.add_collection(c) for c in collections ]

    def replace_keywords(words):
        return [namespace.get(word) if word in namespace else word for word in words]

    def build_rule(expr):
        # Tokenize
        toks = [ e.split(".") for e in expr.split(" ") ]
        replaced = []
        for t in toks:
            
            replaced.append(replace_keywords(t))
        return replaced

    rules = {}

    for rule in game_data.rules:
        rules[rule.get('name')] = build_rule(rule.get('expr'))
        namespace[rule.get('name')] = rules[rule.get('name')]

    def checkRule(name, card):
        ruleList = rules.get(name)
        loc = []
        for l in ruleList:
            if len(l) > 1:
                if l[0] == "card" :
                    if l[1] == "rank" :
                        loc.append(card.rank)
                    elif l[1] == "suit" :    
                        loc.append(card.suit)
                elif type(l[0]) is Pile :
                    try:
                        func = getattr(l[0], l[1])
                        if l[2] == "rank" :
                            loc.append(func().rank)
                        elif l[2] == "suit" :    
                            loc.append(func().suit)
                    except AttributeError:
                        pass
            else:
                loc.append(l[0])
        print(loc)


    # def appropriate_card(top_card, played_card):
    #     """ Verifies that the card to be played is of same rank or suit as top_card
    #     """
    #     return Rank[top_card.rank].value == Rank[played_card.rank].value or \
    #            Suit[top_card.suit].value == Suit[played_card.suit].value

    # def has_valid_move(pile, hand):
    #     """ Returns true if any card in hand can be discarded onto pile
    #     """
    #     top_card = pile[-1]
    #     return any([appropriate_card(top_card, h) for h in hand])

    # def valid_draw(move, card):
    #     return not has_valid_move(discard, move.end)

    # def valid_discard(move, card):
    #     return appropriate_card(discard[-1], card)

    # def replenish_draw_trigger():
    #     # Replenish the draw pile if empty
    #     return not draw and not len(discard) < 2

    # def replenish_draw_action(draw):
    #     """ Takes all the cards but the top one from the discard pile, shuffles them, and replenishes the
    #     draw pile with this set of cards
    #     """
    #     draw.cards = discard[:-1]
    #     shuffle(draw.cards)
    #     del discard[:-1]
    
    # events = [
    #     # event for replenishing the draw pile
    #     [ replenish_draw_trigger, replenish_draw_action, draw ]
    # ]

    # [ game.add_event(Event(*e)) for e in events ]

    # moves = [
    #     # move for player one playing a card on the first pile
    #     [ Positions.ANY, p1.hand, discard, "q", valid_discard ],

    #     # move for player one drawing a card
    #     [ Positions.LAST, draw, p1.hand, "e", valid_draw ],

    #     # move for player two playing a card on the first pile
    #     [ Positions.ANY, p2.hand, discard, "i", valid_discard ],

    #     # move for player two drawing a card
    #     [ Positions.LAST, draw, p2.hand, "p", valid_draw]
    # ]

    # [ game.add_move(Move(*m)) for m in moves ]

    # Distribute cards to the game's collections
    for (collection, count) in zip(collections, counts):
        for _ in range(count):
            collection.add(cards.pop(0))
    assert len(cards) == 0

    checkRule("validDiscard", piles.get('discard').top_card())

    return game