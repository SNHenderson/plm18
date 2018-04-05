from models.game import Game
from models.pile import Pile
from models.player import Player
from models.rank import Rank
from models.suit import Suit
from models.hand import Hand
from models.moves import Move
from models.events import Event
from models.rules import Rule
from models.moves import Positions
from models.collection import Collection
from utils.objs import dict_obj
from collections import OrderedDict

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
        "toprank": "top_rank",
        "topsuit": "top_suit",
        "all": Positions.ANY,
        "top": Positions.LAST
    }

    game = Game(game_data.name, game_data.turn_based)
    game.restrict(lambda self: len(self.collections) == game_data.collections)

    # Players
    players = OrderedDict()
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
    piles = OrderedDict()
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
        return [ replace_keywords(t) for t in toks ]

    rules = OrderedDict()

    for rule in game_data.rules:
        rules[rule.get('name')] = build_rule(rule.get('expr'))
        namespace[rule.get('name')] = rules[rule.get('name')]

    for key, lis in rules.items():
        for value in lis:
            if len(value) > 1:
                if not value[0] == "card" and not value[0] == "move" and not value[0] == "rules":
                    for l in value[1:]: 
                        value[0] = getattr(value[0], l)
                    del value[1:]

    def check_rule(rule_list, move, card):
        loc = []
        if type(card) == Hand:
            return any([check_rule(rule_list, move, c) for c in card])
        for l in rule_list:
            if len(l) > 1:
                if l[0] == "rules":
                    if len(loc) > 0:
                        l1 = loc.pop()
                        loc.append(check_rule(l[1], move, l1))
                    else:
                        loc.append(check_rule(l[1], move, card))
                if l[0] == "card":
                    val = [getattr(card, l[1])]
                    for j in l[2:]: 
                        val = getattr(val, j)
                    loc.append(val[0])
                elif l[0] == "move":
                    val = [getattr(move, l[1])]
                    for j in l[2:]: 
                        val = getattr(val, j)
                    loc.append(val[0])
            elif callable(l[0]):
                loc.append(l[0]())
            elif l[0] == "card":
                loc.append(card)    
            elif l[0] == "=":
                l1 = loc.pop()
                l2 = loc.pop()
                loc.append(l1 == l2)
            elif l[0] == "or":
                l1 = loc.pop()
                l2 = loc.pop()
                loc.append(l1 or l2) 
            elif l[0] == "not":
                l1 = loc.pop()
                loc.append(not l1)
            elif l[0] == "<":
                l1 = loc.pop()
                l2 = loc.pop()
                loc.append(l2 < l1)
            elif l[0] == "and":
                l1 = loc.pop()
                l2 = loc.pop()
                loc.append(l1 and l2)    
            elif l[0] == "any":
                loc = [any(loc)]
            else:
                loc.append(l[0])
        return loc[0]

    def build_move(moves):
        for key, value in moves.items():
            moves[key] = replace_keywords(value.split("."))
        return moves

    moves = []

    for m in game_data.moves:
        m = build_move(m)
        for key, value in m.items():
            if len(value) > 1:
                for l in value[1:]:
                    m[key] = getattr(m[key][0], l)
            elif type(value) is list:
                m[key] = value[0]
        rule = Rule(m.get('how'), check_rule)
        moves.append([m.get('where'), m.get('from'), m.get('to'), m.get('when'), rule.check])
    
    [ game.add_move(Move(*m)) for m in moves ]

    def build_event(events):
        for key, value in events.items():
            toks = [ e.split(".") for e in value.split(" ") ]
            events[key] = [ replace_keywords(t) for t in toks ]
        return events

    events = [build_event(e) for e in game_data.events]

    for event in events:
        for key, lis in event.items():
            for value in lis:
                if len(value) > 1:
                    for l in value[1:]:
                        value[0] = getattr(value[0], l)
                    del value[1:]
    
    def checkEvent(trigger):
        loc = []
        for l in trigger:
            if callable(l[0]):
                loc.append(l[0]())
            elif l[0].isdigit():
                loc.append(int(l[0]))
            elif l[0] == "=":
                l1 = loc.pop()
                l2 = loc.pop()
                loc.append(l1 == l2)
            elif l[0] == "<":
                l1 = loc.pop()
                l2 = loc.pop()
                loc.append(l2 < l1)
            elif l[0] == "or":
                l1 = loc.pop()
                l2 = loc.pop()
                loc.append(l1 or l2)    
            elif l[0] == "and":
                l1 = loc.pop()
                l2 = loc.pop()
                loc.append(l1 and l2)    
            elif l[0] == "not":
                l1 = loc.pop()
                loc.append(not l1)
            elif l[0] == "any":
                loc = [any(loc)]
            else:
                loc.append(l[0])

        return loc[0]

    def doEvent(action):
        loc = []
        for l in action:
            if callable(l[0]) and len(loc) > 0:
                l[0](*loc)
                loc = []
            else:
                loc.append(l[0])
    
    [ game.add_event(Event(lambda : checkEvent(e.get('trigger')), lambda : doEvent(e.get('action')))) for e in events ]    

    def build_win(win_condition):
        toks = [ e.split(".") for e in win_condition.split(" ") ]
        return [ replace_keywords(t) for t in toks ]

    win_condition = build_win(game_data.win_condition)
    for value in win_condition:
        if len(value) > 1:
            for l in value[1:]:
                value[0] = getattr(value[0], l)
            del value[1:]

    def checkWin(win_list):
        loc = []
        for l in win_list:
            if callable(l[0]):
                loc.append(l[0]())
            elif l[0].isdigit():
                loc.append(int(l[0]))
            elif l[0] == "=":
                l1 = loc.pop()
                l2 = loc.pop()
                loc.append(l1 == l2)
            elif l[0] == "or":
                l1 = loc.pop()
                l2 = loc.pop()
                loc.append(l1 or l2)    
            elif l[0] == "not":
                l1 = loc.pop()
                loc.append(not l1)
            elif l[0] == "any":
                loc = [any(loc)]
            else:
                loc.append(l[0])

        return loc[0]

    game.add_win_condition(lambda self: checkWin(win_condition))

    # Distribute cards to the game's collections
    for (collection, count) in zip(collections, counts):
        for _ in range(count):
            collection.add(cards.pop(0))
    assert len(cards) == 0

    return game